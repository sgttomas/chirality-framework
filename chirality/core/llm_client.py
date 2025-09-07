"""
Import shim for backward compatibility.

This module re-exports from the new location to maintain compatibility
while we migrate the codebase.

TODO: Remove this shim once all imports are updated to use
      chirality.infrastructure.llm.openai_adapter directly.
"""

# Re-export everything from new location
from ..infrastructure.llm.openai_adapter import *  # noqa: F401, F403

# This allows existing code to continue using:
#   from chirality.core.llm_client import LLMClient
# While the actual implementation is in:
#   chirality.infrastructure.llm.openai_adapter