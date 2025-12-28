"""Pytest configuration and fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from mcpapiboilerplate.api.main import app


@pytest.fixture
async def client():
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
