FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy application code
COPY . .

# Copy and make scripts executable
COPY scripts/ ./scripts/
RUN chmod +x scripts/*.sh

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 8000

# Use entrypoint script
ENTRYPOINT ["./scripts/entrypoint.sh"]

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]