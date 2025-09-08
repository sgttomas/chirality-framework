"""
Test API Guards for Responses API enforcement

These tests ensure that the framework prevents usage of forbidden APIs
like Chat Completions, enforcing the normative specification requirement
to use only the Responses API.
"""

import pytest
from chirality.infrastructure.api.guards import (
    APIGuardError,
    forbid_chat_completions,
    install_chat_completions_guard,
    require_responses_api
)


class TestAPIGuards:
    """Test API guard functionality."""
    
    def test_forbid_chat_completions_always_raises(self):
        """Test that forbid_chat_completions always raises APIGuardError."""
        with pytest.raises(APIGuardError) as exc_info:
            forbid_chat_completions()
        
        assert "Chat Completions API is forbidden" in str(exc_info.value)
        assert "Use Responses API" in str(exc_info.value)
    
    def test_forbid_chat_completions_with_args(self):
        """Test that forbid_chat_completions raises regardless of arguments."""
        with pytest.raises(APIGuardError):
            forbid_chat_completions(model="gpt-4", messages=[])
        
        with pytest.raises(APIGuardError):
            forbid_chat_completions(some_kwarg="value")
    
    def test_require_responses_api_decorator(self):
        """Test that require_responses_api decorator works on functions."""
        @require_responses_api()
        def test_function():
            return "success"
        
        # Should work normally when no forbidden modules are imported
        result = test_function()
        assert result == "success"
    
    def test_install_chat_completions_guard(self):
        """Test that install_chat_completions_guard works without error."""
        # This should not raise even if openai is not installed
        install_chat_completions_guard()
        
    @pytest.mark.skipif(True, reason="Requires openai package and modifies global state")  
    def test_chat_completions_guard_blocks_openai(self):
        """Test that the guard actually blocks OpenAI Chat Completions."""
        # This test would need to be run in isolation to avoid affecting other tests
        try:
            import openai
            install_chat_completions_guard()
            
            # This should now raise our guard error
            with pytest.raises(APIGuardError):
                openai.chat.completions.create(model="gpt-4", messages=[])
                
        except ImportError:
            pytest.skip("OpenAI package not available")


class TestAPIGuardError:
    """Test the APIGuardError exception."""
    
    def test_api_guard_error_is_exception(self):
        """Test that APIGuardError is a proper exception."""
        error = APIGuardError("test message")
        assert isinstance(error, Exception)
        assert str(error) == "test message"
    
    def test_api_guard_error_inheritance(self):
        """Test that APIGuardError can be caught as Exception."""
        try:
            raise APIGuardError("test error")
        except Exception as e:
            assert isinstance(e, APIGuardError)
            assert "test error" in str(e)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])