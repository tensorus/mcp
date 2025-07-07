"""Configuration settings for Tensorus MCP server and client."""

import os
from typing import Optional, List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class MCPSettings(BaseSettings):
    """Configuration settings for Tensorus MCP components."""
    
    # API connection settings
    API_BASE_URL: str = "https://tensorus-core.hf.space"
    HTTP_TIMEOUT: float = 10.0
    
    # Authentication settings
    AUTH_ENABLED: bool = True
    API_KEYS: str = ""  # Comma-separated API keys
    VALID_API_KEYS: Union[List[str], str] = []  # Backward compatibility
    API_KEY_HEADER_NAME: str = "Authorization"  # Standard Bearer token header
    
    # MCP Server settings
    DEMO_MODE: bool = False
    
    model_config = SettingsConfigDict(env_prefix="TENSORUS_", case_sensitive=False)

    @field_validator("VALID_API_KEYS", mode="before")
    def split_valid_api_keys(cls, v):
        if isinstance(v, str):
            try:
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except Exception:
                pass
            return [key.strip() for key in v.split(',') if key.strip()]
        return v
    
    @field_validator("API_KEYS", mode="before")
    def validate_api_keys(cls, v):
        """Validate and format API keys from environment"""
        if not v:
            return ""
        
        # Split and validate each key
        keys = [key.strip() for key in v.split(',') if key.strip()]
        return ','.join(keys)
    
    @property
    def valid_api_keys(self) -> List[str]:
        """Get list of valid API keys from both new and legacy sources"""
        keys = []
        
        # Primary source: new API_KEYS field
        if self.API_KEYS:
            keys.extend([key.strip() for key in self.API_KEYS.split(',') if key.strip()])
        
        # Fallback: legacy VALID_API_KEYS field
        if self.VALID_API_KEYS:
            if isinstance(self.VALID_API_KEYS, list):
                keys.extend(self.VALID_API_KEYS)
            elif isinstance(self.VALID_API_KEYS, str):
                keys.extend([key.strip() for key in self.VALID_API_KEYS.split(',') if key.strip()])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_keys = []
        for key in keys:
            if key not in seen:
                seen.add(key)
                unique_keys.append(key)
        
        return unique_keys


# Global settings instance
settings = MCPSettings()

# Environment variable helpers
API_BASE_URL_ENV_VAR = "TENSORUS_API_BASE_URL"
API_BASE_URL = os.environ.get(API_BASE_URL_ENV_VAR, settings.API_BASE_URL)
HTTP_TIMEOUT = float(os.environ.get("TENSORUS_HTTP_TIMEOUT", settings.HTTP_TIMEOUT))