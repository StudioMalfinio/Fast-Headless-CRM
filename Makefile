# Fast Headless CRM - Development Commands

.PHONY: help dev staging prod build clean logs migrate init-db backup restore

# Default target
help:
	@echo "Available commands:"
	@echo "  dev        - Start development environment"
	@echo "  staging    - Start staging environment"
	@echo "  prod       - Start production environment"
	@echo "  build      - Build Docker images"
	@echo "  clean      - Stop and remove all containers"
	@echo "  logs       - Show application logs"
	@echo "  migrate    - Run database migrations"
	@echo "  init-db    - Initialize database with admin user"
	@echo "  backup     - Backup database"
	@echo "  restore    - Restore database from backup"

# Development environment
dev:
	cp .env.dev .env
	docker-compose -f docker-compose.dev.yml up --build

# Staging environment
staging:
	cp .env.staging .env
	docker-compose -f docker-compose.staging.yml up -d --build

# Production environment
prod:
	cp .env.prod .env
	docker-compose -f docker-compose.prod.yml up -d --build

# Build images
build:
	docker-compose build

# Clean up
clean:
	docker-compose down -v
	docker system prune -f

# Show logs
logs:
	docker-compose logs -f app

# Run migrations
migrate:
	docker-compose exec app ./scripts/migrate.sh

# Initialize database
init-db:
	docker-compose exec app ./scripts/init-db.sh

# Backup database
backup:
	docker-compose exec db pg_dump -U crm_user -d crm_prod > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database (usage: make restore FILE=backup.sql)
restore:
	docker-compose exec -T db psql -U crm_user -d crm_prod < $(FILE)

# Install dependencies locally
install:
	poetry install

# Run tests locally
test:
	poetry run pytest

# Generate migration
migration:
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

# Apply migrations locally
migrate-local:
	poetry run alembic upgrade head

# Run development server locally
dev-local:
	poetry run uvicorn main:app --reload