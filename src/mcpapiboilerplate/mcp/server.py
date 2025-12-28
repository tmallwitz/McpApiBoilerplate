from fastmcp import FastMCP

mcp = FastMCP("McpApiBoilerplate")


def _get_info() -> str:
    """Return basic info about this MCP server."""
    return "McpApiBoilerplate MCP Server v0.1.0"


def _get_config() -> str:
    """Application configuration resource."""
    return '{"name": "McpApiBoilerplate", "version": "0.1.0"}'


@mcp.tool()
def get_info() -> str:
    """Return basic info about this MCP server."""
    return _get_info()


@mcp.resource("config://app")
def get_config() -> str:
    """Application configuration resource."""
    return _get_config()


def run() -> None:
    mcp.run()


if __name__ == "__main__":
    run()
