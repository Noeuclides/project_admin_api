# Projects Administrator API

API REST for users to create projects with its associate tasks.

## Requirements
To run the docker container make sure to configurate docker and docker compose on your local machine.

Otherwise you have to set on your local machine:
- Python3.7 or greater.

- psql.

- The python package manager [pipenv](https://pipenv-es.readthedocs.io/es/latest/).


## Installation
Only if you are not going to use docker:


Install the dependencies:

```bash
pipenv install
```

Configure psql database:

```bash
psql postgres -f create_db.sql
```

## Usage
If docker:

- Only run:
```bash
docker-compose up --build
```
Make sure that the migrations have been run.


Else:

- Run the migrate command:

```bash
pipenv run migrate
```

- Run the server and go to the home page
```bash
pipenv run server
```

- To register a superuser run:
```bash
pipenv run createsuperuser
```

Note: The migrate, server, createsuperuser commands are configured in the Pipfile.


You can test the api on postman with this link:
https://www.getpostman.com/collections/26c3685cdd6b6e93c6cc

Make sure to set the environment variables host, admin_refresh and operator_refresh.

Documentation can be seen on postman or on the /redoc/ or /swagger/ endpoints.
