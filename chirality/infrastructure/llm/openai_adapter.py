"""
OpenAI Responses API Client for Chirality Framework

Single wrapper for OpenAI Responses API calls.
Enforces JSON output format and global configuration.
"""

import os
import time
import random
from typing import Dict, Any, List, Tuple, Optional

try:
    from openai import OpenAI
    from openai import RateLimitError, APITimeoutError, APIConnectionError, APIError
except ImportError:
    OpenAI = None
    RateLimitError = Exception
    APITimeoutError = Exception  
    APIConnectionError = Exception
    APIError = Exception

from .config import get_config
from ..api.guards import guard_llm_call, install_all_guards


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

    def _call_with_retry(self, api_params: Dict[str, Any], max_retries: int = 3) -> Any:
        """
        P0-5: Resilient API call with exponential backoff and rate limit handling.
        
        Per colleague_1's specification: "SDK pin + resilient adapter (timeouts, 
        retries/backoff, rate-limit handling; usage/latency only in traces)."
        
        Args:
            api_params: Parameters for the Responses API call
            max_retries: Maximum number of retry attempts
            
        Returns:
            OpenAI API response object
            
        Raises:
            Exception: If all retries are exhausted
        """
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                # Set timeout for this attempt (progressively longer)
                timeout = 30.0 + (attempt * 10.0)  # 30s, 40s, 50s, 60s
                
                # Temporarily set timeout on client
                original_timeout = getattr(self.client, 'timeout', None)
                self.client.timeout = timeout
                
                try:
                    # Make the API call
                    response = self.client.responses.create(**api_params)
                    
                    # Success - log latency only in traces (not transcript)
                    if attempt > 0:
                        print(f"📡 API success after {attempt} retries", file=__import__('sys').stderr)
                    
                    return response
                    
                finally:
                    # Restore original timeout
                    if original_timeout is not None:
                        self.client.timeout = original_timeout
                    
            except RateLimitError as e:
                last_exception = e
                if attempt == max_retries:
                    break
                    
                # Exponential backoff with jitter for rate limits
                backoff_time = (2 ** attempt) + random.uniform(0, 1)
                print(f"⏱️  Rate limit hit, retrying in {backoff_time:.1f}s (attempt {attempt + 1}/{max_retries + 1})", 
                      file=__import__('sys').stderr)
                time.sleep(backoff_time)
                
            except Exception as e:
                last_exception = e
                
                # Check if it's a timeout or connection error by name/type
                if "timeout" in str(e).lower() or "connection" in str(e).lower() or \
                   e.__class__.__name__ in ["APITimeoutError", "APIConnectionError"]:
                    if attempt == max_retries:
                        break
                        
                    # Exponential backoff for timeouts/connection errors
                    backoff_time = (2 ** attempt) + random.uniform(0, 0.5)
                    print(f"🔄 Connection/timeout error, retrying in {backoff_time:.1f}s (attempt {attempt + 1}/{max_retries + 1})", 
                          file=__import__('sys').stderr)
                    time.sleep(backoff_time)
                    continue
                    
                # Check if it's an API error (don't retry)
                elif e.__class__.__name__ == "APIError" or "APIError" in str(type(e)):
                    print(f"❌ API error (not retrying): {e}", file=__import__('sys').stderr)
                    break
                    
                # Don't retry on other unexpected errors
                else:
                    print(f"❌ Unexpected error (not retrying): {e}", file=__import__('sys').stderr)
                    break
        
        # All retries exhausted
        raise Exception(f"LLM API call failed after {max_retries + 1} attempts: {last_exception}") from last_exception

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
        # D2-4: Apply guards to prevent forbidden parameter overrides
        guard_llm_call("call_responses", 
                      temperature=temperature, 
                      max_tokens=max_tokens,
                      top_p=top_p,
                      verbosity=verbosity,
                      reasoning_effort=reasoning_effort)
        
        config = get_config()
        start_time = time.time()

        # Use provided values or defaults
        temp = temperature if temperature is not None else config.temperature
        max_tok = max_tokens if max_tokens is not None else config.max_tokens
        top_p_val = top_p if top_p is not None else config.top_p

        try:
            # PROPER: Use Responses API per colleague_1's requirements
            # Convert messages format to instructions + input for Responses API
            system_message = ""
            user_content = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                elif msg["role"] == "user":
                    user_content += f"[USER] {msg['content']}\n"
                elif msg["role"] == "assistant":
                    user_content += f"[ASSISTANT] {msg['content']}\n"
            
            # Clean up trailing newline
            user_content = user_content.rstrip("\n")
            
            # Build Responses API parameters
            api_params = {
                "model": config.model,
                "instructions": system_message,
                "input": user_content,
            }
            
            # Only include temperature if non-None
            if temp is not None:
                api_params["temperature"] = temp
            
            # Only include top_p if non-None
            if top_p_val is not None:
                api_params["top_p"] = top_p_val
            
            # Use max_output_tokens instead of max_tokens for Responses API
            if max_tok is not None:
                api_params["max_output_tokens"] = max_tok
            
            # Only include seed if it's provided (not all APIs support it)
            if config.seed is not None:
                api_params["seed"] = config.seed

            # Add JSON format if requested
            if json_only:
                api_params["response_format"] = {"type": "json_object"}

            # P0-5: Use resilient retry for legacy method too
            response = self._call_with_retry(api_params)

            # Extract JSON content safely from Responses API structure
            try:
                # Standard Responses API response format
                if hasattr(response, "output_text"):
                    content = response.output_text or ""
                elif hasattr(response, "output") and response.output:
                    # Handle structured output format
                    if isinstance(response.output, list) and response.output:
                        content = response.output[0].get("content", {}).get("text", "")
                    else:
                        content = str(response.output)
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
                    f"Invalid JSON response from Responses API: {e}\\nResponse preview: {content_preview}"
                )

            # Build metadata with normalized usage extraction
            latency_ms = int((time.time() - start_time) * 1000)
            usage_fields = self._normalize_usage_fields(response)

            metadata = {
                "model": getattr(response, "model", config.model),
                "temperature": temp,
                "top_p": top_p_val,
                "max_output_tokens": max_tok,  # Changed from max_tokens to match Responses API
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
            {
                "error": str(e),
                "latency_ms": latency_ms,
                "created_at": int(time.time()),
            }
            raise Exception(f"LLM API call failed: {e}") from e

    def call_responses_new(
        self,
        *,
        instructions: str,
        input: str,
        response_format: Optional[Dict[str, Any]] = None,
        store: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call OpenAI Responses API with instructions + input format.
        
        This is the canonical Responses API interface per colleague_1's specification.
        Uses instructions + input instead of messages array to maintain semantic purity.
        
        SELF-POLICING: Raises error if Chat Completions parameters are used.
        
        Args:
            instructions: System instructions (sent explicitly every call)  
            input: Complete input context (transcript + current stage prompt)
            response_format: JSON schema for strict response validation
            store: Whether to store the conversation
            metadata: Additional metadata for the request
            
        Returns:
            Dictionary with {id, output_text, usage, raw}
            
        Raises:
            ValueError: If forbidden Chat Completions parameters are provided
        """
        # Self-policing: Check for forbidden Chat Completions parameters
        forbidden_params = {
            'messages', 'message', 'role', 'content', 'system', 'user', 'assistant',
            'max_tokens', 'max_completion_tokens', 'function_call', 'functions',
            'chat', 'completions', 'stream', 'stream_options'
        }
        
        for param in kwargs:
            if param in forbidden_params:
                raise ValueError(
                    f"Forbidden Chat Completions parameter '{param}' detected in LLMClient. "
                    f"Chirality Framework requires Responses API with instructions+input format only."
                )
        
        if kwargs:
            # Any unexpected parameters should be flagged
            raise ValueError(
                f"Unexpected parameters: {list(kwargs.keys())}. "
                f"LLMClient.call_responses_new only accepts: instructions, input, response_format, store, metadata."
            )
        # D2-4: Apply guards (responses method gets parameters from config)
        guard_llm_call("call_responses_new", 
                      response_format=response_format,
                      store=store,
                      metadata=metadata)
        
        config = get_config()
        start_time = time.time()
        
        try:
            # PROPER: Use Responses API directly per colleague_1's specification
            # This is the canonical interface - instructions + input format
            api_params = {
                "model": config.model,
                "instructions": instructions,
                "input": input,
            }
            
            # Only include temperature if non-None
            if config.temperature is not None:
                api_params["temperature"] = config.temperature
            
            # Only include top_p if non-None
            if config.top_p is not None:
                api_params["top_p"] = config.top_p
            
            # Use max_output_tokens for Responses API
            if config.max_tokens is not None:
                api_params["max_output_tokens"] = config.max_tokens
            
            # Add response format if provided
            if response_format:
                api_params["response_format"] = response_format
            
            # Add seed if provided
            if config.seed is not None:
                api_params["seed"] = config.seed
            
            # P0-5: Call Responses API with resilient retry logic (per colleague_1's specification)
            response = self._call_with_retry(api_params)
            
            # Extract content using Responses API format
            if hasattr(response, "output_text"):
                output_text = response.output_text or ""
            elif hasattr(response, "output") and response.output:
                # Handle structured output format
                if isinstance(response.output, list) and response.output:
                    output_text = response.output[0].get("content", {}).get("text", "")
                else:
                    output_text = str(response.output)
            else:
                output_text = ""
            
            # Parse as JSON if response_format was provided
            if response_format:
                import json
                try:
                    response_dict = json.loads(output_text)
                except json.JSONDecodeError:
                    response_dict = {"error": "Invalid JSON response", "raw_output": output_text}
            else:
                response_dict = {"content": output_text}
            
            # Build metadata for Responses API
            latency_ms = int((time.time() - start_time) * 1000)
            usage_fields = self._normalize_usage_fields(response)
            
            # Convert to new return format
            return {
                "id": f"resp_{int(time.time())}", 
                "output_text": output_text,
                "usage": getattr(response, "usage", None),
                "raw": {
                    "response": response_dict,
                    "metadata": {
                        "model": getattr(response, "model", config.model),
                        "temperature": config.temperature,
                        "top_p": config.top_p,
                        "max_output_tokens": config.max_tokens,
                        "latency_ms": latency_ms,
                        "created_at": int(time.time()),
                        "response_format": response_format,
                        **usage_fields
                    },
                    "request": {
                        "instructions": instructions[:100] + "..." if len(instructions) > 100 else instructions,
                        "input": input[:100] + "..." if len(input) > 100 else input,
                        "response_format": response_format,
                        "store": store
                    }
                }
            }
            
        except Exception as e:
            # Return error in new format
            return {
                "id": f"error_{int(time.time())}",
                "output_text": "",
                "usage": None,
                "raw": {
                    "error": str(e),
                    "latency_ms": int((time.time() - start_time) * 1000),
                    "created_at": int(time.time())
                }
            }


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
    DEPRECATED: Legacy API removed - use call_responses instead.
    
    This function is no longer supported. All code must use the Responses API
    with call_responses(instructions=..., input=...) format.

    Raises:
        NotImplementedError: Always - this API is deprecated and removed
    """
    raise NotImplementedError(
        "Legacy Chat Completions API removed - use call_responses(instructions=..., input=...) instead. "
        "The messages array format is no longer supported."
    )


def call_responses(
    *,
    instructions: str,
    input: str, 
    response_format: Optional[Dict[str, Any]] = None,
    store: bool = True,
    metadata: Optional[Dict[str, Any]] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Call OpenAI Responses API with instructions + input format.
    
    Per colleague_1's D2-3 specification:
    - instructions = system.md (sent explicitly every call)
    - input = transcript_so_far + current_stage_asset_text
    - response_format = stage's JSON tail schema (strict)
    - store = conversation storage setting
    
    SELF-POLICING: Raises error if Chat Completions parameters are used.
    
    Args:
        instructions: System instructions (typically system.md content)
        input: Complete input context (transcript + current stage prompt)
        response_format: JSON schema for response validation
        store: Whether to store the conversation
        metadata: Additional metadata for the request
        
    Returns:
        Dictionary with {id, output_text, usage, raw}
        
    Raises:
        ValueError: If forbidden Chat Completions parameters are provided
    """
    # Self-policing: Check for forbidden Chat Completions parameters
    forbidden_params = {
        'messages', 'message', 'role', 'content', 'system', 'user', 'assistant',
        'max_tokens', 'max_completion_tokens', 'function_call', 'functions',
        'chat', 'completions', 'stream', 'stream_options'
    }
    
    for param in kwargs:
        if param in forbidden_params:
            raise ValueError(
                f"Forbidden Chat Completions parameter '{param}' detected. "
                f"Chirality Framework requires Responses API with instructions+input format only. "
                f"Use instructions=... and input=... instead of messages array."
            )
    
    if kwargs:
        # Log any unexpected parameters for debugging
        unexpected = set(kwargs.keys()) - {'temperature', 'top_p', 'max_output_tokens', 'seed', 'verbosity', 'reasoning_effort'}
        if unexpected:
            raise ValueError(
                f"Unexpected parameters: {unexpected}. "
                f"Only Responses API parameters are allowed: instructions, input, response_format, store, metadata."
            )
    
    client = get_client()
    return client.call_responses_new(
        instructions=instructions,
        input=input,
        response_format=response_format,
        store=store,
        metadata=metadata
    )
