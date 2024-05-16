

# async FastAPI + PostgreSQL app

- [async FastAPI + PostgreSQL app](#async-fastapi--postgresql-app)
  - [Libraries + Tools](#libraries--tools)
  - [Quickstart](#quickstart)
    - [1. Create repository from a template](#1-create-repository-from-a-template)
    - [2. Install dependecies with Poetry](#2-install-dependecies-with-poetry)
    - [3. Setup database and migrations](#3-setup-database-and-migrations)
    - [4. Now you can run app](#4-now-you-can-run-app)
    - [5. Activate pre-commit](#5-activate-pre-commit)
    - [6. Running tests](#6-running-tests)
  - [About](#about)
  - [License](#license)


## Libraries + Tools

- [x] FastAPI +Pydantic for API implementation and basic GUI testing
- [x] FastAPI-mail for async mail
- [x] SQLAlchemy 2.0 for orm
- [x] [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations setup
- [x] Docker for PostgreSQL 16 database
- [x] [Poetry](https://python-poetry.org/docs/), `mypy`, `pre-commit` hooks with 


## About

This project is for a take home project that required FastAPI to set up a backend app to make API calls, send e-mails, and make database queries.
based off a [minimal version](https://github.com/rafsaf/minimal-fastapi-postgres-template)  of the [full stack fast api template](https://github.com/tiangolo/full-stack-fastapi-template)
Email is disabled by default but the fucntionality is there, need to attach unsecured e-mail acc to .env file.

## Endpoints
AUTH - need auth
/auth/access-token
Login Access Token

/auth/refresh-token
Refresh Token

/auth/register
Register New Attorney

/users/updatelead
Update Lead State

USERS - non auth calls

/users/filelead
File New Lead

/users/getpendingleads
Get Pending Leads

/users/getreachedleads
Get Reached Out Leads

/users/getattorneys
Get Attorneys

/users/getprospects
Get Prospects

## Quickstart

### 1. Clone Repo

```bash
git clone https://github.com/Brandon-mg/Python_API_Project.git
```

### 2. Install dependecies 

```bash
cd your_project_name

### Poetry install (python3.12)
poetry install
```

### 3. Setup database and migrations

```bash
### Setup database
docker-compose up -d

### Run Alembic migrations
alembic upgrade head
```

### 4. Now you can run app

```bash
### And this is it:
uvicorn app.main:app --reload

```

### 5. Running tests

go to `http://127.0.0.1:8000/` and use the GUI to run basic API tests and see outputs easier

<br>

## Step by step example - POST and GET endpoints

you can use FastAPIs in built dev dashboard to test all endpoints except the email and the file upload
for file upload you can use an app like Bruno or Postman and post a multipart form with 'name', 'email', and 'file'
or use the test python scripts to run everything at once

### 1. Create Attorney account


### 2. File Lead and Prospect


### 3. Check PENDING and REACHED_OUT leads


### 4. Check and Update Lead Status


## License

The code is under MIT License. It's here for archival purposes, The template sped up a lot of the basic infra but almost all the api requests and responses had to be altered for this project.