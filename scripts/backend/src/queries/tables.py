# coding=utf-8
from sqlalchemy import Column, String , Integer, DateTime, Boolean,ForeignKey
from .queries import Entity, Base
from datetime import datetime


class User_table(Entity, Base):
    __tablename__ = 'users'

    name = Column(String)
    password = Column(String)
    active_state = Column(Boolean)
    created_at = Column(DateTime)

    def __init__(self, name, active_state, password):
        Entity.__init__(self)
        self.name= name
        self.active_state = active_state
        self.password= password
        self.created_at = datetime.now()



class Access_table(Entity, Base):
    __tablename__ = 'access'

    name = Column(String)

    def __init__(self, name):
        Entity.__init__(self)
        self.name= name

class Groups_table(Entity, Base):
    __tablename__ = 'groups'

    name = Column(String)
    description = Column(String)

    def __init__(self, name, description):
        Entity.__init__(self)
        self.name= name
        self.description = description

# class UserSec_table(Entity, Base):
#     __tablename__ = 'usersecurity'

#     user_id = Column('user_id',Integer, ForeignKey('user.id'))
#     group_id = Column('group_id',Integer, ForeignKey('group.id'))
#     access_id = Column('access_id', Integer, ForeignKey('access.id'))

#     def __init__(self, name, description):
#         Entity.__init__(self)
#         self.name= name
#         self.description = description