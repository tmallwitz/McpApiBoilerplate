"""Tests for MCP tools."""

from mcpapiboilerplate.mcp.server import _get_info, _get_config


def test_get_info():
    """Test that get_info returns expected server info."""
    result = _get_info()
    assert "McpApiBoilerplate" in result
    assert "v0.1.0" in result


def test_get_config():
    """Test that get_config returns valid JSON config."""
    import json

    result = _get_config()
    config = json.loads(result)
    assert config["name"] == "McpApiBoilerplate"
    assert config["version"] == "0.1.0"
