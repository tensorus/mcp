"""Tensorus MCP: Model Context Protocol integration for Tensorus tensor database.

This package provides both server and client implementations for connecting
AI agents and LLMs to Tensorus via the Model Context Protocol.
"""

__version__ = "1.0.0"
__author__ = "Tensorus Team"
__email__ = "ai@tensorus.com"

from .client import TensorusMCPClient, DEFAULT_MCP_URL
from .server import create_mcp_app

__all__ = ["TensorusMCPClient", "create_mcp_app", "DEFAULT_MCP_URL"]