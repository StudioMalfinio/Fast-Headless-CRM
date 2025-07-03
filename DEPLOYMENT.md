# Fast Headless CRM Deployment Guide

This guide covers deploying the Fast Headless CRM application using Docker and Traefik for different environments.

## Prerequisites

- Docker and Docker Compose installed
- Domain name pointed to your server (for staging/production)
- Basic knowledge of Docker and environment variables

## Architecture

The application uses:
- **FastAPI** - Python web framework
- **PostgreSQL** - Database
- **Traefik** - Reverse proxy and load balancer
- **Redis** - Caching (production only)
- **Alembic** - Database migrations

## Environment Setup

### Development

For local development with hot reload:

```bash
# Copy environment file
cp .env.dev .env

# Start services
docker-compose -f docker-compose.dev.yml up --build

# Access application
# API: http://localhost
# Traefik Dashboard: http://localhost:8080
# Database: localhost:5432
```

### Staging

For staging environment with SSL:

```bash
# Copy and configure environment
cp .env.staging .env
# Edit .env file with your staging domain and credentials

# Generate password hash for Traefik dashboard
echo $(htpasswd -nb admin your_password)

# Start services
docker-compose -f docker-compose.staging.yml up -d --build

# Access application
# API: https://staging.yourapp.com
# Traefik Dashboard: https://traefik.staging.yourapp.com
```

### Production

For production environment:

```bash
# Copy and configure environment
cp .env.prod .env
# Edit .env file with your production domain and strong credentials

# Generate secure password hash for Traefik
echo $(htpasswd -nb admin your_secure_password)

# Start services
docker-compose -f docker-compose.prod.yml up -d --build

# Access application
# API: https://yourapp.com
# Traefik Dashboard: https://traefik.yourapp.com
```

## Environment Variables

### Required Variables

Update these in your `.env` file:

```bash
# Domain settings
DOMAIN=yourapp.com
LETSENCRYPT_EMAIL=admin@yourapp.com

# Database
DB_PASSWORD=your_secure_db_password

# Application security
SECRET_KEY=your_very_long_random_secret_key

# Traefik dashboard auth (generate with htpasswd)
TRAEFIK_AUTH=admin:$2y$10$hashed_password
```

### Generating Secure Values

```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate password hash for Traefik
echo $(htpasswd -nb admin your_password)
```

## Database Management

### Initial Setup

The application automatically:
1. Runs database migrations on startup
2. Creates an initial admin user (username: `admin`, password: `admin123`)

### Manual Migration

```bash
# Run migrations manually
docker-compose exec app ./scripts/migrate.sh

# Create initial admin user
docker-compose exec app ./scripts/init-db.sh
```

### Database Backups

```bash
# Backup database
docker-compose exec db pg_dump -U crm_user crm_prod > backup.sql

# Restore database
docker-compose exec -T db psql -U crm_user crm_prod < backup.sql
```

## Traefik Configuration

### Features Enabled

- **Automatic SSL** - Let's Encrypt certificates
- **HTTP to HTTPS redirect** - All traffic redirected to HTTPS
- **Rate limiting** - 100 requests per minute (production)
- **Load balancing** - Multiple app instances
- **Dashboard** - Web UI for monitoring

### Dashboard Access

- Development: http://localhost:8080
- Staging: https://traefik.staging.yourapp.com
- Production: https://traefik.yourapp.com

Protected with basic auth (admin/password from TRAEFIK_AUTH).

## Monitoring and Logs

### View Logs

```bash
# Application logs
docker-compose logs app

# All services logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f app
```

### Health Checks

The application includes health checks:

```bash
# Check application health
curl https://yourapp.com/health

# Check Traefik health
curl https://traefik.yourapp.com/ping
```

## Scaling

### Scale Application

```bash
# Scale to 3 app instances
docker-compose up -d --scale app=3
```

Traefik automatically load balances between instances.

## Security Considerations

### Production Security

1. **Change default passwords** - Update admin user password after first login
2. **Strong secrets** - Use long, random SECRET_KEY and DB_PASSWORD
3. **CORS configuration** - Restrict CORS_ORIGINS to your domains
4. **Regular updates** - Keep Docker images updated
5. **Firewall** - Only expose ports 80, 443, and 22

### SSL Certificates

Let's Encrypt certificates are automatically:
- Generated on first startup
- Renewed before expiration
- Stored in Docker volume `traefik_letsencrypt`

## Troubleshooting

### Common Issues

1. **SSL Certificate Issues**
   ```bash
   # Check certificate status
   docker-compose logs traefik | grep acme
   
   # Restart Traefik to retry
   docker-compose restart traefik
   ```

2. **Database Connection Issues**
   ```bash
   # Check database logs
   docker-compose logs db
   
   # Verify database is running
   docker-compose ps db
   ```

3. **Application Won't Start**
   ```bash
   # Check application logs
   docker-compose logs app
   
   # Rebuild image
   docker-compose build --no-cache app
   ```

### Reset Environment

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v

# Rebuild and start
docker-compose up --build
```

## API Documentation

Once deployed, access the interactive API documentation:

- Swagger UI: `https://yourapp.com/docs`
- ReDoc: `https://yourapp.com/redoc`

## Default Credentials

**Initial Admin User:**
- Username: `admin`
- Password: `admin123`

**Important:** Change this password immediately after first login!

## Support

For issues and questions:
1. Check application logs
2. Verify environment variables
3. Ensure domain DNS is properly configured
4. Check Traefik dashboard for routing issues