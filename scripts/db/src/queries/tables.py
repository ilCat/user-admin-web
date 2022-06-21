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

# asociation_table = Table('asociation_table',
#                          Base.metadata,
#                          Column('user_id', Integer, ForeignKey(
#                              'users.id'), primary_key=True),
#                          Column('group_id', Integer, ForeignKey(
#                              'groups.id'), primary_key=True),
#                          Column('access_id', Integer, ForeignKey(
#                             'access.id'), primary_key=True)
#                          )
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
    members = relationship('User_table',secondary=asociation_table , back_populates='group')

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
    created_at = Column(DateTime)
    # group_id = Column(Integer, ForeignKey('groups.id'))
    group = relationship('Groups_table',secondary=asociation_table, back_populates='members')
    # groupsUser = relationship('Groups_table', backref='usersGroup')
    # accessUser = relationship('Access_table',secondary=asociation_table, back_populates='usersAccess')

    def __init__(self, name, active_state, password):
        self.name = name
        self.active_state = active_state
        self.password = password
        self.created_at = datetime.now()


# class Access_table(Base):
#     __tablename__ = 'access'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     usersAccess = relationship('User_table', secondary=asociation_table)

#     def __init__(self, name):
#         # Entity.__init__(self)
#         self.name = name


# class Groups_table(Base):
#     __tablename__ = 'groups'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id')),
#     usersGroup = relationship('User_table', secondary=asociation_table)

#     def __init__(self, name, description):
#         # Entity.__init__(self)
#         self.name = name
#         self.description = description

