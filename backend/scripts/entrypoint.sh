#!/bin/sh
# Exit immediately if any command fails
set -e

echo "Running database migrations..."
uv run alembic upgrade head

echo "Starting FastAPI server..."
exec "$@"
