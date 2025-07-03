#!/bin/bash

# Entrypoint script for the FastAPI application

set -e

echo "Starting FastAPI CRM application..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -c "
import time
import psycopg2
import os

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        if 'postgresql' in os.getenv('DATABASE_URL', ''):
            # Extract connection details from DATABASE_URL
            db_url = os.getenv('DATABASE_URL')
            # Simple parsing for postgresql://user:pass@host:port/db
            if db_url.startswith('postgresql://'):
                conn_str = db_url.replace('postgresql://', '').split('/')
                auth_host = conn_str[0].split('@')
                auth = auth_host[0].split(':')
                host_port = auth_host[1].split(':')
                
                conn = psycopg2.connect(
                    host=host_port[0],
                    port=int(host_port[1]) if len(host_port) > 1 else 5432,
                    database=conn_str[1],
                    user=auth[0],
                    password=auth[1]
                )
                conn.close()
                print('Database is ready!')
                break
        else:
            print('Using SQLite database')
            break
    except Exception as e:
        retry_count += 1
        print(f'Database not ready, retrying... ({retry_count}/{max_retries})')
        time.sleep(2)

if retry_count >= max_retries:
    print('Failed to connect to database after maximum retries')
    exit(1)
"

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Create initial admin user if needed
echo "Checking for initial admin user..."
python -c "
from app.db.database import SessionLocal
from app.crud.user import get_user_by_username, create_user
from app.schemas.user import UserCreate
import os

db = SessionLocal()
try:
    admin_user = get_user_by_username(db, 'admin')
    if not admin_user:
        print('Creating initial admin user...')
        admin_create = UserCreate(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_admin=True
        )
        create_user(db, admin_create)
        print('Admin user created!')
        print('Username: admin')
        print('Password: admin123')
        print('Please change the password after first login!')
    else:
        print('Admin user already exists')
except Exception as e:
    print(f'Error with admin user setup: {e}')
finally:
    db.close()
"

echo "Application setup completed!"

# Execute the main command
exec "$@"