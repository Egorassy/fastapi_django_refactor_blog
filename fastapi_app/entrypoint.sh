#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until PGPASSWORD="$POSTGRES_PASSWORD" pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" >/dev/null 2>&1; do
  sleep 1
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting application..."
exec "$@"