# user-admin-web

to build and run DB local

$ sudo -i -u postgres

$ psql

to build and run DB  in docker

$ sudo docker run --name db-test -p 8000:8000 -e POSTGRES_DB=db-test -e POSTGRES_PASSWORD=admin -d postgres

