# coding=utf-8
from queries.tables import User_table, Access_table, Groups_table, Session, engine, Base

# if needed, generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check existing data
users = session.query(User_table).all()
access = session.query(Access_table).all()
grops = session.query(Groups_table).all()

if len(users) == 0:
    first_user = User_table("Alexis", True, 'CatCat22')
    session.add(first_user)
    session.commit()
    session.close()


accessRoles = ["Read", "Write", "Administrator", "Owner"]

for rol in accessRoles:
    rol_i = Access_table(rol)
    session.add(rol_i)
    session.commit()
session.close()

securityGroups  = {"Operator": ["Employee with basic information level",1], 
    "TeamLeader": ["Leader of a operators group",3], 
    "Mechanic": ["Technician with middle infomation level",2], 
    "Electric": ["Technician with middle infomation level",2],
    "ProjectLeader": ["Leader of project with high information level",3],
    "Mannager": ["Leader with the highest information level",4]}

for title, description in securityGroups.items():
    group_i = Groups_table(title, description[0],description[1])
    session.add(group_i)
    session.commit()
session.close()

addGroup = session.query(User_table)[0]
group4 = session.query(Groups_table)[3]
group2 = session.query(Groups_table)[1]
addGroup.group.append(group4)
session.commit()
addGroup.group.append(group2)
session.commit()
session.close()



users = session.query(User_table).all()
print("users : ")
for user in users:
    print(
        f'({user.id}) {user.name} - Estado activo:{user.active_state} - DT: {user.created_at} - Nose : {user.group }')


asking = session.query(Groups_table).join(Groups_table.accessLevel).join(Groups_table.members).filter(User_table.name == 'Alexis')
print("user : ", asking.all())



