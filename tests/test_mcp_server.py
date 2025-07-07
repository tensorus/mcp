import json
import sys
import pytest
import httpx
from typing import Optional

from tensorus_mcp import mcp_server
from tensorus_mcp.mcp_server import MCP_AVAILABLE
from tensorus_mcp.config import settings

pytestmark = pytest.mark.skipif(
    not MCP_AVAILABLE, reason="MCP dependencies (fastmcp, mcp) not available"
)


class DummyResponse:
    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data

    def raise_for_status(self):
        pass


def make_mock_client(
    monkeypatch,
    method,
    url,
    payload,
    response,
    *,
    expected_params=None,
    expected_headers: Optional[dict] = None,
    expected_timeout: float = mcp_server.HTTP_TIMEOUT,
):
    class MockAsyncClient:
        def __init__(self, *, timeout=None, **kwargs):
            assert timeout == expected_timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        async def post(
            self, u, json=None, params=None, headers=None
        ):
            assert u == url
            assert json == payload
            if expected_params is not None:
                assert params == expected_params
            if expected_headers is not None:
                assert headers == expected_headers
            return DummyResponse(response)

    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)


def test_create_empty_mcp_server():
    """Test that we can create an empty MCP server."""
    server = mcp_server.create_server()
    assert server is not None


def test_settings_import():
    """Test that we can import and use settings."""
    assert settings is not None
    assert hasattr(settings, 'tensorus_api_base_url')
EOF < /dev/null
