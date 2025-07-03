from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import contacts, companies, deals, auth, pipelines
from app.models.base import Base
from app.db.database import engine
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
import uvicorn

# Setup logging
setup_logging()
logger = get_logger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast Headless CRM",
    description="A headless CRM API built with FastAPI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(deals.router, prefix="/api/deals", tags=["deals"])
app.include_router(pipelines.router, prefix="/api/pipelines", tags=["pipelines"])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Fast Headless CRM API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)