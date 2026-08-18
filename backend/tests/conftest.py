import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.database import engine, async_session_maker

@pytest.fixture
def anyio_backend():
    return 'asyncio'
    
@pytest.fixture(autouse=True)
async def reset_engine():
    """Ensure engine pool is clean for each test loop."""
    yield
    await engine.dispose()

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session