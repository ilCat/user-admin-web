# coding=utf-8
from flask_cors import CORS
from flask import Flask, jsonify, request
from queries.queries import Session, engine, Base
from queries.tables import User_table, Access_table, Groups_table

# if needed, generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check existing data
users = session.query(User_table).all()
access = session.query(Access_table).all()
grops = session.query(Groups_table).all()

if len(users) == 0:
    first_user = User_table("Alexis",True, 'CatCat22') 
    session.add(first_user)
    session.commit()
    session.close()



accessRoles = ["Read", "Write", "Administrator", "Owner"]

for rol in accessRoles:
    rol_i = Access_table(rol)
    session.add(rol_i)
    session.commit()
session.close()


users = session.query(User_table).all()
print("users : ")
for user in users:
    print(f'({user.id}) {user.name} - Estado:{user.active_state} - DT: {user.created_at}')

