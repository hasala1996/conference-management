#!/bin/bash

set -e

echo "Waiting for the PostgreSQL service to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Applying Alembic migrations..."
alembic upgrade heads

echo "Running seed_data.py..."
python /app/seed_data.py

echo "Starting the application..."
exec uvicorn fast_api.fast_api_app:create_app --factory --host 0.0.0.0 --port 8001
