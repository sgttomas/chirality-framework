"""
LLM Infrastructure Module

Contains LLM client adapters, mock resolvers, and configuration
for external language model integrations.
"""

from .openai_adapter import LLMClient, call_responses_api
from .resolver import CellResolver
from .mock_resolvers import EchoResolver
from .config import get_config, LLMConfig

__all__ = [
    "LLMClient",
    "call_responses_api", 
    "CellResolver",
    "EchoResolver",
    "get_config",
    "LLMConfig",
]