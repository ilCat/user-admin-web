# coding=utf-8
from flask import Flask, jsonify, request
from db.queries.tables import (User_table, UserSchema, Access_table,
                               AccessSchema,  Groups_table, GroupSchema, Session, engine, Base,)


app = Flask(__name__)

# if needed, generate database schema
Base.metadata.create_all(engine)


# Get list of users
@app.route('/users')
def getUsers():
    session = Session()
    user_objects = session.query(User_table).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    users = schema.dump(user_objects)
    session.close()

    # collecting names and serializing as JSON
    nameList = {}
    for i in users:
        nameList[i['id']] = i['name']
    return jsonify(nameList)


# Get desolate user information
@app.route('/users/<string:user_name>')
def getUserInformation(user_name):
    session = Session()
    user_object = session.query(User_table).filter(
        User_table.name == user_name).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    user = schema.dump(user_object)

    # serializing as JSON
    session.close()
    return jsonify(user)


# Add new user
@app.route('/user', methods=['POST'])
def add_user():
    # mount user object
    posted_user = UserSchema(only=('name', 'password', 'active_state'))\
        .load(request.get_json())

    user = User_table(**posted_user)

    session = Session()
    session.add(user)
    session.commit()

    # return created user
    new_user = UserSchema().dump(user)
    session.close()
    return jsonify(new_user), 201


# Add user to a group
@app.route('/groups', methods=['POST'])
def add_user_group():
    # mount user object
    posted = {'name_user': request.json['name_user'],
              'name_group': request.json['name_group']
              }
    session = Session()
    user_objet = session.query(User_table).filter(
        User_table.name == posted['name_user'])[0]

    group_objet = session.query(Groups_table).filter(
        Groups_table.name == posted['name_group'])[0]

    user_objet.group.append(group_objet)
    session.commit()

    # return created user
    user_to_group = {"user": user_objet.name,
                     "group": group_objet.name}
    session.close()
    return jsonify(user_to_group), 202


# Get groups of a User
@app.route('/groups/<string:userName>')
def getUserGroups(userName):
    session = Session()
    user_object = session.query(Groups_table).join(
        Groups_table.members).filter(User_table.name == userName)

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    user = schema.dump(user_object)

    # serializing as JSON
    session.close()
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True, port=4000)
