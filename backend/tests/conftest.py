import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import engine

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