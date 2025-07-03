#!/bin/bash

# Database initialization script

echo "Initializing database..."

# Create initial admin user
echo "Creating initial admin user..."
python -c "
from app.db.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
import os

db = SessionLocal()
admin_user = UserCreate(
    username='admin',
    email='admin@example.com',
    password='admin123',
    is_admin=True
)

try:
    create_user(db, admin_user)
    print('Admin user created successfully!')
    print('Username: admin')
    print('Password: admin123')
    print('Please change the password after first login!')
except Exception as e:
    print(f'Error creating admin user: {e}')
finally:
    db.close()
"

echo "Database initialization completed!"