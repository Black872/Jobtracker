# JobTracker M1 Implementation Plan

## Scope

M1 establishes the FastAPI backend, PostgreSQL persistence, vacancy model, database
migrations, and CRUD REST API. It does not include frontend work or later roadmap
features.

## Architecture

The backend uses a small layered design:

```text
HTTP request -> FastAPI router -> vacancy service -> SQLAlchemy session -> PostgreSQL
```

- Routers own HTTP validation, response models, and status codes.
- Services own vacancy operations and business rules.
- SQLAlchemy models own persistence mapping.
- Pydantic schemas define API contracts independently from persistence models.
- Alembic migrations are the only authority for database schema changes.

The implementation uses synchronous SQLAlchemy, UUID primary keys, hard deletion,
and no status-history table. `status_changed_at` supports the current-status duration
calculation without expanding M1 into historical reporting.

## API Contract

The versioned API provides create, retrieve, update, delete, and paginated list
operations under `/api/v1/vacancies`. The list endpoint supports sorting from its
first version:

```text
GET /api/v1/vacancies?sort=created_at&order=desc&limit=50&offset=0
```

M1 supports `created_at` as the initial sort field and `asc` or `desc` as the order.
Enum query parameters make unsupported values explicit validation errors while
allowing additional sort fields to be added without changing the contract.

## Backend Quality Tooling

- **Ruff:** Recommended for linting, import sorting, and formatting. It is fast and
  replaces the overlapping Black plus isort toolchain for this project.
- **Mypy:** Recommended with the SQLAlchemy plugin to check application boundaries
  that linting cannot verify. Strict mode is enabled, with narrowly scoped settings
  if a third-party package lacks typing.
- **Black:** Not included. It is mature, but running it alongside Ruff's compatible
  formatter duplicates configuration and pre-commit work without improving M1.
- **Pre-commit:** Recommended as a thin local runner for Ruff and Mypy. It prevents
  avoidable quality drift for a single developer without requiring CI.

Pytest covers API behavior, validation, persistence, sorting, and calculated fields.

## Files

```text
backend/
  app/{api,core,db,models,schemas,services}/
  alembic/versions/
  tests/
  alembic.ini
  pyproject.toml
  .env.example
  .pre-commit-config.yaml
  README.md
database/README.md
README.md
```

## Alternatives

- Async SQLAlchemy provides more I/O concurrency but adds session and test
  complexity that the single-user MVP does not need.
- SQLModel reduces duplication but couples transport and persistence models.
- Integer IDs are smaller, while UUIDs better support future import and distributed
  creation workflows.
- PostgreSQL native enums offer strong enforcement but are harder to evolve; string
  columns with check constraints keep migrations straightforward.
- Soft deletion and status history improve auditability but complicate all queries
  and are not current requirements.

## Risks

- Calendar-day calculations require consistent UTC semantics.
- A single `status_changed_at` cannot reconstruct historical transitions.
- Manual schema changes can cause migration drift; Alembic must remain authoritative.
- Application and database validation can diverge, so critical invariants are
  enforced in both layers where practical.
- PostgreSQL-specific behavior cannot be validated accurately with SQLite; database
  integration tests require a separately supplied PostgreSQL test database.

## Delivery Order

1. Establish configuration, packaging, and application startup.
2. Add SQLAlchemy session management and the vacancy model.
3. Add schemas, services, CRUD routes, pagination, and sorting.
4. Add and validate the initial Alembic migration.
5. Add tests and documentation.
6. Run Ruff, Mypy, and Pytest locally.
