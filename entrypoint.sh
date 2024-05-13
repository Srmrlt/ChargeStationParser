#!/bin/sh
set -e

echo "Waiting for the database to be available..."
while ! nc -z database 5432; do
  sleep 1
done
echo "Database is available."

echo "Applying migrations..."
alembic upgrade head

echo "Starting the application..."
exec "$@"
