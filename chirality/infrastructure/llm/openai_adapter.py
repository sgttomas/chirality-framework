"""
OpenAI Responses API Client for Chirality Framework

Single wrapper for OpenAI Responses API calls.
Enforces JSON output format and global configuration.
"""

import os
import time
import json
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

    def _normalize_usage_fields(self, response: Any) -> Dict[str, int]:
        """
        Normalize usage fields from OpenAI response to consistent format.

        Provides robust extraction with fallbacks for different response structures.
        Always returns the 4 fields expected by BudgetTracker: prompt_tokens,
        completion_tokens, cached_tokens, total_tokens.

        Args:
            response: OpenAI API response object

        Returns:
            Dict with normalized usage fields, all integers >= 0
        """
        # Default values (safe fallbacks)
        prompt_tokens = 0
        completion_tokens = 0
        cached_tokens = 0
        total_tokens = 0

        # Extract from response.usage if available
        usage = getattr(response, "usage", None)
        if usage:
            # Primary token counts
            prompt_tokens = getattr(usage, "input_tokens", 0)
            if prompt_tokens == 0:  # Fallback naming
                prompt_tokens = getattr(usage, "prompt_tokens", 0)

            completion_tokens = getattr(usage, "output_tokens", 0)
            if completion_tokens == 0:  # Fallback naming
                completion_tokens = getattr(usage, "completion_tokens", 0)

            # Cached tokens from input_token_details
            input_details = getattr(usage, "input_token_details", None)
            if input_details:
                cached_tokens = getattr(input_details, "cached_tokens", 0)

            # Total (prefer provided total, fallback to sum)
            total_tokens = getattr(usage, "total_tokens", 0)
            if total_tokens == 0:
                total_tokens = prompt_tokens + completion_tokens

        # Ensure all values are non-negative integers
        return {
            "prompt_tokens": max(0, int(prompt_tokens)),
            "completion_tokens": max(0, int(completion_tokens)),
            "cached_tokens": max(0, int(cached_tokens)),
            "total_tokens": max(0, int(total_tokens)),
        }

    def call_responses(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_only: bool = True,
        top_p: Optional[float] = None,
        verbosity: Optional[str] = None,
        reasoning_effort: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Call OpenAI Responses API with messages.

        CRITICAL: Uses Responses API, not Chat Completions API.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override
            json_only: If True, enforce JSON response format
            top_p: Optional top_p override (note: OpenAI uses top_p, not top_k)
            verbosity: GPT-5 verbosity ("low", "medium", "high")
            reasoning_effort: GPT-5 reasoning effort ("minimal", "medium")

        Returns:
            Tuple of (response_dict, metadata_dict)

        Raises:
            ValueError: If response is not valid JSON
            Exception: For API errors
        """
        config = get_config()
        start_time = time.time()

        # Use provided values or defaults
        temp = temperature if temperature is not None else config.temperature
        max_tok = max_tokens if max_tokens is not None else config.max_tokens
        top_p_val = top_p if top_p is not None else config.top_p

        try:
            # CRITICAL: Use responses.create with input= parameter (not prompt=)
            # Convert messages to Responses API input format
            input_messages = []
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                input_messages.append(
                    {"role": role, "content": [{"type": "text", "text": content}]}
                )

            # Build API parameters
            api_params = {
                "model": config.model,
                "input": input_messages,
                "temperature": temp,
                "top_p": top_p_val,
                "max_output_tokens": max_tok,
                "seed": config.seed,
            }

            # Add GPT-5 specific parameters if provided
            if verbosity is not None and verbosity in ["low", "medium", "high"]:
                api_params["verbosity"] = verbosity

            if reasoning_effort is not None and reasoning_effort in ["minimal", "medium"]:
                api_params["reasoning_effort"] = reasoning_effort

            # Add JSON format if requested
            if json_only:
                api_params["response_format"] = {"type": "json_object"}

            response = self.client.responses.create(**api_params)

            # Extract JSON content safely from Responses API structure
            try:
                # Try different response structures that Responses API might use
                if hasattr(response, "output_text"):
                    content = response.output_text
                elif hasattr(response, "output") and response.output:
                    content = response.output[0].content[0].text
                elif hasattr(response, "choices") and response.choices:
                    content = response.choices[0].text or ""
                else:
                    raise ValueError("Could not extract content from Responses API response")

                # Parse JSON response
                import json

                response_dict = json.loads(content)

            except (json.JSONDecodeError, AttributeError, IndexError) as e:
                # Provide truncated response for debugging
                content_preview = (
                    str(content)[:200] + "..." if len(str(content)) > 200 else str(content)
                )
                raise ValueError(
                    f"Invalid JSON response: {e}\\nResponse preview: {content_preview}"
                )

            # Build metadata with normalized usage extraction
            latency_ms = int((time.time() - start_time) * 1000)
            usage_fields = self._normalize_usage_fields(response)

            metadata = {
                "model": getattr(response, "model", config.model),
                "temperature": temp,
                "top_p": top_p_val,
                "max_tokens": max_tok,
                "json_only": json_only,
                "latency_ms": latency_ms,
                "usage": getattr(response, "usage", None),
                "created_at": int(time.time()),
                "response_format": "json_object" if json_only else "text",
                **usage_fields,  # Merge normalized usage fields
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


def call_responses_api(
    messages: List[Dict[str, str]],
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    json_only: bool = True,  # Default to JSON for new architecture
    top_p: Optional[float] = None,
    verbosity: Optional[str] = None,
    reasoning_effort: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Convenience function for calling Responses API.

    Args:
        messages: List of message dicts
        temperature: Optional temperature override
        max_tokens: Optional max_tokens override
        json_only: If True, enforce JSON response format (default)
        top_p: Optional top_p override (note: OpenAI uses top_p, not top_k)
        verbosity: GPT-5 verbosity setting
        reasoning_effort: GPT-5 reasoning effort setting

    Returns:
        Tuple of (response_dict, metadata_dict)
    """
    client = get_client()
    return client.call_responses(
        messages, temperature, max_tokens, json_only, top_p, verbosity, reasoning_effort
    )
