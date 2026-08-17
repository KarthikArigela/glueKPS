from contextlib import asynccontextmanager
from importlib.metadata import version, PackageNotFoundError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import engine, get_session

try:
    APP_VERSION = version("Gluekps-backend")
except PackageNotFoundError:
    APP_VERSION = "0.1.0"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown
    await engine.dispose()

app = FastAPI(
    title=settings.APP_NAME,
    version=APP_VERSION,
    docs_url="/docs" if settings.ENV == "development" else None,
    redoc_url="/redoc" if settings.ENV == "development" else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev mode; tighten for production later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", name="Health Check", status_code=status.HTTP_200_OK)
async def health_check():
    """Liveness probe: verifies the API server is up."""
    return {"status": "ok", "app": settings.APP_NAME, "version": APP_VERSION}

@app.get("/health/db", name="DB Health Check", status_code=status.HTTP_200_OK)
async def health_db_check(session: AsyncSession = Depends(get_session)):
    """Readiness probe: verifies database connection is active."""
    try:
        result = await session.execute(text("SELECT 1;"))
        result.scalar()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )    