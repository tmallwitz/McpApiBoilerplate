"""Tests for health endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test that health endpoint returns ok status."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
