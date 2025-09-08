"""
OpenAI Responses API Client for Chirality Framework

Single wrapper for OpenAI Responses API calls.
Enforces JSON output format and global configuration.
"""

import os
import time
from typing import Dict, Any, List, Tuple, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from .config import get_config


class LLMClient:
    """
    Wrapper for OpenAI Responses API.

    Enforces use of Responses API (not Chat Completions) and JSON output format.
    Uses global configuration from llm_config.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize client.

        Args:
            api_key: OpenAI API key. Uses OPENAI_API_KEY env var if None.
        """
        if OpenAI is None:
            raise ImportError("OpenAI package required. Install with: pip install openai")

        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required")

        self.client = OpenAI(api_key=api_key)

    def call_responses(
        self, messages: List[Dict[str, str]]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Call OpenAI Responses API with messages.

        CRITICAL: Uses Responses API, not Chat Completions API.

        Args:
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Tuple of (response_dict, metadata_dict)

        Raises:
            ValueError: If response is not valid JSON
            Exception: For API errors
        """
        config = get_config()
        start_time = time.time()

        try:
            # CRITICAL: Use responses.create with input= parameter (not prompt=)
            # Convert messages to Responses API input format
            input_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                input_messages.append({
                    "role": role,
                    "content": [{"type": "text", "text": content}]
                })
            
            response = self.client.responses.create(
                model=config.model,
                input=input_messages,
                temperature=config.temperature,
                top_p=config.top_p,
                max_output_tokens=config.max_tokens,  # Correct parameter name
                seed=config.seed,
                response_format={"type": "json_object"},  # Correct format
            )

            # Extract JSON content safely from Responses API structure
            try:
                # Try different response structures that Responses API might use
                if hasattr(response, 'output_text'):
                    content = response.output_text
                elif hasattr(response, 'output') and response.output:
                    content = response.output[0].content[0].text
                elif hasattr(response, 'choices') and response.choices:
                    content = response.choices[0].text or ""
                else:
                    raise ValueError("Could not extract content from Responses API response")
                
                # Parse JSON response
                import json
                response_dict = json.loads(content)
                
            except (json.JSONDecodeError, AttributeError, IndexError) as e:
                # Provide truncated response for debugging
                content_preview = str(content)[:200] + "..." if len(str(content)) > 200 else str(content)
                raise ValueError(f"Invalid JSON response: {e}\\nResponse preview: {content_preview}")

            # Build metadata
            latency_ms = int((time.time() - start_time) * 1000)
            metadata = {
                "model": getattr(response, "model", config.model),
                "latency_ms": latency_ms,
                "usage": getattr(response, "usage", None),
                "created_at": int(time.time()),
                "response_format": "json_object",
            }

            return response_dict, metadata

        except Exception as e:
            # Add timing info to error metadata
            latency_ms = int((time.time() - start_time) * 1000)
            error_metadata = {
                "error": str(e),
                "latency_ms": latency_ms,
                "created_at": int(time.time()),
            }
            raise Exception(f"LLM API call failed: {e}") from e


# Global client instance
_client: Optional[LLMClient] = None


def get_client() -> LLMClient:
    """Get global LLM client instance."""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client


def call_responses_api(messages: List[Dict[str, str]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Convenience function for calling Responses API.

    Args:
        messages: List of message dicts

    Returns:
        Tuple of (response_dict, metadata_dict)
    """
    client = get_client()
    return client.call_responses(messages)