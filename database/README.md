# Database

JobTracker uses PostgreSQL. Database schema changes are owned exclusively by the
Alembic migrations in `backend/alembic/versions`; do not maintain duplicate schema
SQL in this directory.
