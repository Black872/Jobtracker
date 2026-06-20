# JobTracker Backend

## Requirements

- Python 3.12+
- A separately managed PostgreSQL database

M1 intentionally does not provide infrastructure or container configuration.

## Setup

From `backend/`, create and activate a virtual environment, then install the project:

```powershell
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Update `JOBTRACKER_DATABASE_URL`, apply migrations, and start the API:

```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

Interactive API documentation is available at `/docs`.

## Quality Checks

```powershell
ruff check .
ruff format --check .
mypy app
pytest
pre-commit install
```

Ruff provides both linting and formatting, so Black is intentionally not installed.
Tests use an in-memory database for fast API feedback by default. Set
`JOBTRACKER_TEST_DATABASE_URL` to a dedicated PostgreSQL test database to exercise
the same database engine used in production. The test suite creates and removes its
own vacancy tables, so this URL must never reference a development or production
database.

## API

Vacancy operations are available under `/api/v1/vacancies`. Lists are paginated and
support the stable sorting contract:

```text
GET /api/v1/vacancies?sort=created_at&order=desc&limit=50&offset=0
```

The health endpoint is available at `/health`.
