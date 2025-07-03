#!/bin/bash

# Database migration script

echo "Starting database migration..."

# Wait for database to be ready
echo "Waiting for database..."
sleep 5

# Run migrations
echo "Running Alembic migrations..."
alembic upgrade head

echo "Migration completed successfully!"