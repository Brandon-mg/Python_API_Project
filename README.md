

# async FastAPI + PostgreSQL app

- [async FastAPI + PostgreSQL app](#async-fastapi--postgresql-app)
  - [Libraries + Tools](#libraries--tools)
  - [About](#about)
  - [Endpoints](#endpoints)
  - [Quickstart](#quickstart)
    - [1. Clone Repo](#1-clone-repo)
    - [2. Install dependecies](#2-install-dependecies)
    - [3. Setup database and Alembic migrations](#3-setup-database-and-alembic-migrations)
    - [4. Run Uvicorn](#4-run-uvicorn)
    - [5. Running tests](#5-running-tests)
  - [Step by step example - POST and GET endpoints](#step-by-step-example---post-and-get-endpoints)
    - [1. Create Attorney account](#1-create-attorney-account)
    - [2. File Lead and Prospect](#2-file-lead-and-prospect)
    - [3. Check PENDING and REACHED_OUT leads](#3-check-pending-and-reached_out-leads)
    - [4. Check and Update Lead Status](#4-check-and-update-lead-status)
    - [5. Get Attorney and Prospect ids](#5-get-attorney-and-prospect-ids)
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
Email is disabled by default. To enable you need to enable the flag in app/core/send_mail.py and put in the credentials for an unsecured (no 2fa, access to less secure apps) e-mail acc.

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

### Poetry install
poetry install
```

### 3. Setup database and Alembic migrations

```bash
### Setup database
docker-compose up -d

### Run Alembic
alembic upgrade head
```

### 4. Run Uvicorn

```bash
### And this is it:
uvicorn app.main:app --reload

```

### 5. Running Tests

go to `http://127.0.0.1:8000/` and use the GUI to run basic API tests and see outputs easier
for file upload you can try [Bruno](https://www.usebruno.com/) or [Postman](https://www.postman.com/downloads/) or use the test_file_upload.py

<br>

## Step by step example - POST and GET endpoints

you can use FastAPIs in built dev dashboard to test all endpoints except the email and the file upload
for file upload you can use an app like Bruno or Postman and post a multipart form with 'name', 'email', and 'file'
or use the test python scripts to run everything at once

### 1. Create Attorney account

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "email": "user@example.com",
  "password": "string"
}'
```

returns
```bash
{
  "attorney_id": "41862d97-1533-4e12-a8ed-0e030259f168",
  "email": "user@example.com"
}
```

check list of attorneys using 
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/getattorneys' \
  -H 'accept: application/json' \
  -d ''
```

returns
```bash
{
  "ids": [
    "41862d97-1533-4e12-a8ed-0e030259f168"
  ]
}
```

### 2. File Lead and Prospect
you'll need to use a multipart post app like [Bruno](https://www.usebruno.com/) or [Postman](https://www.postman.com/downloads/)

You can also run the test_file_upload.py and edit the values in it 

The file uploaded can be found at app/resume

returns
```bash
{
  "prospect_id": "dc548bb3-fcac-4f8e-bd7c-4001f5955fb7",
  "attorney_id": "41862d97-1533-4e12-a8ed-0e030259f168",
  "email": "user123@example.com",
  "lead_id": "a430f9ec-908d-4b51-9948-03684762576c"
}
```
### 3. Check PENDING and REACHED_OUT leads
Check leads in PENDING state
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/getpendingleads' \
  -H 'accept: application/json' \
  -d ''
```

returns

```bash
{
  "ids": [
    "a430f9ec-908d-4b51-9948-03684762576c",
    "6cce44f8-f6c9-4e27-a898-ad48354fc34f"
  ]
}
```

Check leads in REACHED_OUT state
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/getreachedleads' \
  -H 'accept: application/json' \
  -d ''
```

should return empty if no leads were updated


### 4. Check and Update Lead Status
Update a lead to reached out,needs valid email, password, and lead id
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/updatelead' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "password": "string",
  "lead_id": "a430f9ec-908d-4b51-9948-03684762576c"
}'
```

returns
```bash
{
  "prospect_id": "dc548bb3-fcac-4f8e-bd7c-4001f5955fb7",
  "attorney_id": "41862d97-1533-4e12-a8ed-0e030259f168",
  "lead_id": "a430f9ec-908d-4b51-9948-03684762576c",
  "state": "REACHED_OUT"
}
```

Should be able to run 
Check leads in REACHED_OUT state
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/getreachedleads' \
  -H 'accept: application/json' \
  -d ''
```

to get the updated lead now
```bash
{
  "ids": [
    "a430f9ec-908d-4b51-9948-03684762576c"
  ]
}
```


### 5. Get Attorney and Prospect ids

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/getattorneys' \
  -H 'accept: application/json' \
  -d ''

curl -X 'POST' \
  'http://127.0.0.1:8000/users/getprospects' \
  -H 'accept: application/json' \
  -d ''
```

## License

The code is under MIT License. It's here for archival purposes, The template sped up a lot of the basic infra but almost all the api requests and responses had to be altered for this project.