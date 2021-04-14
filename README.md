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
And go to http://127.0.0.1:8000 on the browser.

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


