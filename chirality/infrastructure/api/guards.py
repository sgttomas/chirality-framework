"""
API Guards for Chirality Framework

Prevents usage of forbidden APIs like Chat Completions.
Enforces Responses API usage throughout the framework.
"""


class APIGuardError(Exception):
    """Raised when forbidden API is used."""

    pass


def forbid_chat_completions(*args, **kwargs):
    """
    Guard function to prevent Chat Completions API usage.

    Raises:
        APIGuardError: Always - Chat Completions API is forbidden
    """
    raise APIGuardError(
        "Chat Completions API is forbidden in Chirality Framework. "
        "Use Responses API (client.responses.create) instead. "
        "This is enforced by the normative specification."
    )


def require_responses_api():
    """
    Decorator to enforce Responses API usage.

    Usage:
        @require_responses_api()
        def my_llm_function():
            # Must use client.responses.create(input=...)
            pass
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Check for forbidden imports/calls during runtime
            import sys

            forbidden_modules = ["openai.chat", "openai.Completion"]
            for module_name in forbidden_modules:
                if module_name in sys.modules:
                    raise APIGuardError(
                        f"Forbidden module {module_name} detected. "
                        "Only Responses API is allowed."
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def install_chat_completions_guard():
    """
    Install a guard that monkey-patches OpenAI Chat Completions to always fail.

    This should be called in test setup to ensure no code accidentally uses
    the forbidden Chat Completions API.
    """
    try:
        import openai

        # Monkey patch chat completions to always raise our guard error
        if hasattr(openai, "chat") and hasattr(openai.chat, "completions"):
            openai.chat.completions.create = forbid_chat_completions

        # Also patch any Completions API if it exists
        if hasattr(openai, "Completion"):
            openai.Completion.create = forbid_chat_completions

    except ImportError:
        # OpenAI not installed, no need to guard
        pass


# Global guards that can be monkey-patched if needed
CHAT_COMPLETIONS_GUARD = forbid_chat_completions
