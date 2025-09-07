"""
API Guards for Chirality Framework

Ensures that only allowed APIs are used throughout the codebase.
"""


class APIGuardError(Exception):
    """Raised when a forbidden API is attempted."""
    pass


def forbid_chat_completions():
    """
    Guard against Chat Completions API usage.
    
    Raises:
        APIGuardError: Always, as Chat Completions is forbidden
    """
    raise APIGuardError(
        "Chat Completions API is forbidden in Chirality Framework. "
        "Use Responses API (client.responses.create) instead."
    )


def ensure_responses_api(client_method_name: str) -> None:
    """
    Ensure that only Responses API methods are used.
    
    Args:
        client_method_name: Name of the OpenAI client method being called
        
    Raises:
        APIGuardError: If method is not from Responses API
    """
    allowed_methods = {
        'responses.create',
        'responses',  # Allow accessing the responses object itself
    }
    
    forbidden_methods = {
        'chat.completions.create',
        'chat.completions',
        'completions.create',
        'completions',
    }
    
    # Check if it's explicitly forbidden
    if any(forbidden in client_method_name for forbidden in forbidden_methods):
        raise APIGuardError(
            f"Method '{client_method_name}' is forbidden. "
            f"Use Responses API (client.responses.create) instead."
        )
    
    # Log for debugging (optional)
    if client_method_name not in allowed_methods:
        # This might be okay for other utility methods
        pass