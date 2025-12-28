# AI Handoff Document

This document provides instructions for AI assistants (Claude Code, Codex, Cursor, etc.) on how to extend the McpApiBoilerplate project.

## Project Overview

| Component | Framework | Entry Point |
|-----------|-----------|-------------|
| REST API | FastAPI | `src/mcpapiboilerplate/api/main.py` |
| MCP Server | FastMCP | `src/mcpapiboilerplate/mcp/server.py` |
| Tests | pytest + pytest-asyncio | `tests/` |
| Package Manager | UV | `pyproject.toml` |

---

## Adding a New API Endpoint

### Step 1: Create Route File

Create a new file in `src/mcpapiboilerplate/api/routes/`:

```python
# src/mcpapiboilerplate/api/routes/users.py
"""User routes."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])


class User(BaseModel):
    id: int
    name: str
    email: str


@router.get("/{user_id}")
async def get_user(user_id: int) -> User:
    """Get user by ID."""
    return User(id=user_id, name="John Doe", email="john@example.com")


@router.post("/")
async def create_user(user: User) -> User:
    """Create a new user."""
    return user
```

### Step 2: Register Router in Main App

Edit `src/mcpapiboilerplate/api/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mcpapiboilerplate.api.routes import users  # Add import

app = FastAPI(title="McpApiBoilerplate", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)  # Add router


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


def run() -> None:
    uvicorn.run("mcpapiboilerplate.api.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run()
```

### Step 3: Add API Tests

Create test file in `tests/test_api/`:

```python
# tests/test_api/test_users.py
"""Tests for user endpoints."""

import pytest


@pytest.mark.asyncio
async def test_get_user(client):
    """Test getting a user by ID."""
    response = await client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data


@pytest.mark.asyncio
async def test_create_user(client):
    """Test creating a new user."""
    user_data = {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data
```

---

## Adding a New MCP Tool

### Step 1: Add Tool to Server

Edit `src/mcpapiboilerplate/mcp/server.py`:

```python
from fastmcp import FastMCP

mcp = FastMCP("McpApiBoilerplate")


# Internal function for testing
def _calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b


# MCP tool wrapper
@mcp.tool()
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    return _calculate_sum(a, b)


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
```

### Tool Pattern Explanation

The project uses a pattern with internal `_function` and wrapper `function`:

- `_function()` - Internal implementation, directly callable for testing
- `function()` - MCP-decorated wrapper, exposed to MCP clients

This pattern exists because FastMCP decorators transform functions into `FunctionTool` objects that aren't directly callable in tests.

### Step 2: Add MCP Tool Tests

Edit `tests/test_mcp/test_tools.py`:

```python
"""Tests for MCP tools."""

from mcpapiboilerplate.mcp.server import _calculate_sum


def test_calculate_sum():
    """Test calculate_sum tool."""
    result = _calculate_sum(2, 3)
    assert result == 5


def test_calculate_sum_negative():
    """Test calculate_sum with negative numbers."""
    result = _calculate_sum(-1, 5)
    assert result == 4
```

---

## Adding a New MCP Resource

### Step 1: Add Resource to Server

Edit `src/mcpapiboilerplate/mcp/server.py`:

```python
from fastmcp import FastMCP
import json

mcp = FastMCP("McpApiBoilerplate")


def _get_status() -> str:
    """Get current system status."""
    return json.dumps({
        "status": "operational",
        "uptime": "99.9%",
        "version": "0.1.0"
    })


@mcp.resource("status://system")
def get_status() -> str:
    """System status resource.

    Returns current operational status of the system.
    """
    return _get_status()


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
```

### Resource URI Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| `config://` | `config://app` | Configuration data |
| `status://` | `status://system` | System status |
| `data://` | `data://users` | Data collections |
| `file://` | `file://logs` | File-based resources |

### Step 2: Add Resource Tests

```python
"""Tests for MCP resources."""

import json
from mcpapiboilerplate.mcp.server import _get_status


def test_get_status():
    """Test system status resource."""
    result = _get_status()
    status = json.loads(result)
    assert status["status"] == "operational"
    assert "version" in status
```

---

## Pydantic Models for Shared Types

Place shared models in `src/mcpapiboilerplate/shared/`:

```python
# src/mcpapiboilerplate/shared/models.py
"""Shared Pydantic models."""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
```

Import in both API and MCP:

```python
from mcpapiboilerplate.shared.models import User
```

---

## Validation Checklist

After making changes, run these commands:

```bash
# Install/sync dependencies
uv sync

# Run tests
uv run pytest -v

# Lint code
uv run ruff check src/

# Format code
uv run ruff format src/

# Start API server (manual test)
uv run mcpapi-serve

# Start MCP server (manual test)
uv run mcpapi-mcp
```

---

## File Location Reference

| Purpose | Location |
|---------|----------|
| API routes | `src/mcpapiboilerplate/api/routes/*.py` |
| API models | `src/mcpapiboilerplate/api/models/*.py` |
| MCP server | `src/mcpapiboilerplate/mcp/server.py` |
| MCP tools | `src/mcpapiboilerplate/mcp/tools/*.py` |
| Shared code | `src/mcpapiboilerplate/shared/*.py` |
| API tests | `tests/test_api/*.py` |
| MCP tests | `tests/test_mcp/*.py` |
| Test fixtures | `tests/conftest.py` |

---

## Common Patterns

### Async API Endpoint

```python
@router.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    # Use async/await for I/O operations
    item = await fetch_item_from_db(item_id)
    return item
```

### MCP Tool with Complex Return

```python
@mcp.tool()
def search_items(query: str, limit: int = 10) -> str:
    """Search for items.

    Args:
        query: Search query string
        limit: Maximum results to return (default: 10)

    Returns:
        JSON string with search results
    """
    results = perform_search(query, limit)
    return json.dumps(results)
```

### Error Handling in API

```python
from fastapi import HTTPException

@router.get("/items/{item_id}")
async def get_item(item_id: int) -> Item:
    item = await fetch_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```

---

## Version Updates

When adding features, update:

1. `src/mcpapiboilerplate/__init__.py` - `__version__`
2. `pyproject.toml` - `version`
3. `CHANGELOG.md` - Add entry under `[Unreleased]`

---

*Last updated: 2025-12-28*
