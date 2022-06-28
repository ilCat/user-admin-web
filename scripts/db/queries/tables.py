# coding=utf-8
from sqlalchemy import (create_engine, Column, String,
                        Integer, DateTime, Boolean, ForeignKey, Table)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from marshmallow import Schema, fields
import pytz



db_url = 'localhost:5432'
db_name = 'testdb'
db_user = 'postgres'
db_password = 'admin'
# engine = create_engine(
#     f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
engine = create_engine(
    'postgresql://pjfgdlvudnmmdw:cd5f063c62668a2bd8d6099d04ad021c308aaf1f3c9a29125be9a43010233ce4@ec2-34-200-35-222.compute-1.amazonaws.com:5432/d1fcp3k1egdjsf')
Session = sessionmaker(bind=engine)

Base = declarative_base()


asociation_table = Table('asociation_table',
                         Base.metadata,
                         Column('user_id', Integer, ForeignKey(
                             'users.id')),
                         Column('group_id', Integer, ForeignKey(
                             'groups.id'))
                         )


class Access_table(Base):
    __tablename__ = 'access'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    securityGroup = relationship('Groups_table', back_populates='accessLevel')

    def __init__(self, name):
        self.name = name


class Groups_table(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    access_id = Column(Integer, ForeignKey('access.id'))
    accessLevel = relationship('Access_table', back_populates='securityGroup')
    members = relationship(
        'User_table', secondary=asociation_table, back_populates='group')

    def __init__(self, name, description, access_id):
        self.name = name
        self.description = description
        self.access_id = access_id


class User_table(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String)
    active_state = Column(Boolean)
    created_at = Column(DateTime(timezone=True)) # %Y-%m-%dT%H:%M:%S
    group = relationship(
        'Groups_table', secondary=asociation_table, back_populates='members')

    def __init__(self, name, active_state, password):
        self.name = name
        self.active_state = active_state
        self.password = password
        self.created_at = datetime.now(pytz.timezone('America/Argentina/San_Luis'))


class AccessSchema(Schema):
    id = fields.Integer()
    name = fields.Str()


class GroupSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    description = fields.Str()
    access_id = fields.Integer()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    password = fields.Str()
    active_state = fields.Bool()
    created_at = fields.DateTime()
