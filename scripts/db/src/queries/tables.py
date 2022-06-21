# coding=utf-8
from sqlalchemy import create_engine,Column, String, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


db_url = 'localhost:5432'
db_name = 'testdb'
db_user = 'postgres'
db_password = 'admin'
engine = create_engine(
    f'postgresql://{db_user}:{db_password}@{db_url}/{db_name}')
Session = sessionmaker(bind=engine)

Base = declarative_base()

asociation_table = Table('asociation_table',
                         Base.metadata,
                         Column('user_id', Integer, ForeignKey(
                             'users.id'), primary_key=True),
                         Column('group_id', Integer, ForeignKey(
                             'groups.id'), primary_key=True),
                         Column('access_id', Integer, ForeignKey(
                             'access.id'), primary_key=True)
                         )


class User_table(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    active_state = Column(Boolean)
    created_at = Column(DateTime)
    # groupsUser = relationship('Groups_table',secondary=asociation_table, back_populates='usersGroup')
    # accessUser = relationship('Access_table',secondary=asociation_table, back_populates='usersAccess')

    def __init__(self, name, active_state, password):
        # Entity.__init__(self)
        self.name = name
        self.active_state = active_state
        self.password = password
        self.created_at = datetime.now()


class Access_table(Base):
    __tablename__ = 'access'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    usersAccess = relationship('User_table', secondary=asociation_table)

    def __init__(self, name):
        # Entity.__init__(self)
        self.name = name


class Groups_table(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    usersGroup = relationship('User_table', secondary=asociation_table)

    def __init__(self, name, description):
        # Entity.__init__(self)
        self.name = name
        self.description = description

