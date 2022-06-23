# coding=utf-8
from flask import Flask, jsonify, request, render_template, redirect, session
from db.queries.tables import (User_table, UserSchema, Access_table,
                               AccessSchema,  Groups_table, GroupSchema, Session, engine, Base,)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# if needed, generate database schema
Base.metadata.create_all(engine)


@app.route('/')
def home():
    return render_template('index.html')



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
    return render_template("userList.html", nameList=nameList)


# Get desolate user information
@app.route('/users/<string:user_name>')
def getUserInformation(user_name):
    session = Session()
    user_object = session.query(User_table).filter(
        User_table.name == user_name).all()

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    user= schema.dump(user_object)

    user_object = session.query(Groups_table).join(
        Groups_table.members).filter(User_table.name == user_name)

    # transforming into JSON-serializable objects
    schema = UserSchema(many=True)
    user2 = schema.dump(user_object)

    # serializing as JSON
    session.close()

    return render_template("userInformation.html", user=[user[0],user2]) # jsonify(user_sch)


# Add new user
@app.route('/user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('addUser.html')

    if request.method == 'POST':

        # posted_user = UserSchema(only=('name', 'password', 'active_state')).load(request.get_json())
        req = {'name': request.form['name'],
               'password': request.form['password'],
               'active_state': request.form['active_state']}

        posted_user = UserSchema(
            only=('name', 'password', 'active_state')).load(req)

        user = User_table(**posted_user)

        session = Session()
        session.add(user)
        session.commit()

        # return created user
        new_user = UserSchema().dump(user)
        session.close()
        return redirect('/users')  # jsonify(new_user), 201


# Add user to a group
@app.route('/groups', methods=['GET','POST'])
def add_user_group():

    if request.method =='GET':
        session = Session()
        # groupsList = session.execute("select name from groups")
        groups = session.query(Groups_table).all()
        schema = GroupSchema(many=True)
        groupsList = schema.dump(groups)
        users = session.query(User_table).all()
        schemaU = UserSchema(many=True)
        usersList = schemaU.dump(users)
        data = [usersList, groupsList]

        return render_template('userNewGroup.html',data=data)


    if request.method == 'POST':
            
        posted = {'name_user': request.form['name_user'],
                'name_group': request.form['name_group']
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
        return redirect("/users") # jsonify(user_to_group), 202


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
