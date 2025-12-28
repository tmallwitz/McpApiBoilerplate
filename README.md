# McpApiBoilerplate

A Python boilerplate project combining a REST API (FastAPI) and MCP server (FastMCP) in a single, well-structured repository.

## Features

- **FastAPI** REST API with health endpoint
- **FastMCP** MCP server with tools and resources
- **UV** package manager for fast, reliable dependency management
- **Pydantic** for data validation
- **pytest** with async support for testing
- **ruff** for linting and formatting

## Requirements

- Python 3.12+
- [UV](https://docs.astral.sh/uv/) package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/tmallwitz/McpApiBoilerplate.git
cd McpApiBoilerplate

# Install dependencies
uv sync
```

## Usage

### REST API

Start the FastAPI server:

```bash
uv run mcpapi-serve
```

The API will be available at http://localhost:8000

**Endpoints:**

- `GET /health` - Health check endpoint, returns `{"status": "ok"}`
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### MCP Server

Start the MCP server (stdio transport):

```bash
uv run mcpapi-mcp
```

**Tools:**

- `get_info` - Returns basic info about the MCP server

**Resources:**

- `config://app` - Application configuration resource

## Development

### AI-Assisted Development

For AI assistants (Claude Code, Codex, Cursor, etc.), see **[HANDOFF.md](HANDOFF.md)** for detailed instructions on:

- Adding new API endpoints
- Adding new MCP tools and resources
- Testing patterns and conventions
- File location reference

### Running Tests

```bash
uv run pytest
```

### Linting

```bash
uv run ruff check src/
```

### Formatting

```bash
uv run ruff format src/
```

## Project Structure

```
McpApiBoilerplate/
├── pyproject.toml
├── uv.lock
├── CHANGELOG.md
├── HANDOFF.md
├── README.md
├── .gitignore
├── .python-version
├── src/
│   └── mcpapiboilerplate/
│       ├── __init__.py
│       ├── py.typed
│       ├── api/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   └── health.py
│       │   └── models/
│       │       └── __init__.py
│       ├── mcp/
│       │   ├── __init__.py
│       │   ├── server.py
│       │   └── tools/
│       │       ├── __init__.py
│       │       └── example.py
│       └── shared/
│           └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_api/
    │   ├── __init__.py
    │   └── test_health.py
    └── test_mcp/
        ├── __init__.py
        └── test_tools.py
```

## License

MIT License - see LICENSE file for details.
