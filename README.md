# user-admin-web

Web service of users, roles and groups.

Link: https://user-admin-web.herokuapp.com/

The main idea of this project is to debelop a web aplication able to managing users and security groups with their access levels with the next structure:

User tags: 
* Name or Alias (unique)
* Password
* Creation date
* Status (Active or Inactive)

Group tags:
* Name
* Decription 
* Security Access level

Access level:
* 1 = Reader
* 2 = Writer
* 3 = Administrator
* 4 = Owner

Default Structure:

Group 1 : Operator -> Employee with basic information level(Reader)

Group 2 : Team Leader -> Leader of a operators group(Administrator)

Group 3 : Mechanic -> Technician with middle infomation level(Writer)

Group 4 : Electric -> Technician with middle infomation level(Writer)

Group 5 : Project Leader -> Leader of project with high information level(Administrator)

Group 6 : Manager -> Leader with the highest information level(Owner)

# Contents

- db : database creation and query using python, SQLAlchemy and postgreSQL

- backend :  app.py using python Flask

- front end :  templates html usin bootstrap

# Requirements

- postgresql

- requeriment.txt

# Deploy local

To deploy local use locDeploy branch

Create database:  
+ db_name = 'testdb'
+ db_user = 'postgres'
+ db_password = 'admin'
 
 Run scripts/db/main.py file to fill some data in the database. 
 
 Run booststrap.sh file
 
# Vulnerabilities

Lack of error handling in cases of missing data or invalid data, e.g.: 
* Duplicate user names
* Forget to assign state
* Choosing a invalid group
