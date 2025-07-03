from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./crm.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

class DevelopmentSettings(Settings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./crm_dev.db"

class StagingSettings(Settings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://crm_user:crm_password@db:5432/crm_staging"
    CORS_ORIGINS: list = ["https://staging.yourapp.com"]

class ProductionSettings(Settings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://crm_user:crm_password@db:5432/crm_prod"
    CORS_ORIGINS: list = ["https://yourapp.com"]
    LOG_LEVEL: str = "WARNING"

def get_settings():
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "staging":
        return StagingSettings()
    elif environment == "production":
        return ProductionSettings()
    else:
        return DevelopmentSettings()

settings = get_settings()