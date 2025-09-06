"""
Tests for LLM Client - OpenAI Responses API integration and validation.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
import json

from chirality.core.llm_client import call_responses_api
from chirality.core.llm_config import LLMConfig


# Mock response data that matches expected structure
MOCK_RESPONSE_TEXT = """
{
  "text": "Semantic concept resolved",
  "terms_used": ["concept", "resolved"],
  "warnings": []
}
"""

MOCK_RESPONSE_INVALID = """
{
  "incomplete": "missing required fields"
}
"""


@pytest.fixture
def sample_messages():
    """Sample messages for testing."""
    return [
        {"role": "system", "content": "You are a semantic calculator."},
        {"role": "user", "content": 'Resolve these terms: ["A", "B"]'},
    ]


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response object."""
    mock_response = Mock()
    mock_response.text = MOCK_RESPONSE_TEXT
    mock_response.usage.completion_tokens = 10
    mock_response.usage.prompt_tokens = 25
    mock_response.usage.total_tokens = 35
    mock_response.model = "gpt-4"
    mock_response.id = "response_123"
    return mock_response


class TestLLMConfig:
    """Test LLMConfig data structure."""

    def test_llm_config_defaults(self):
        """Test LLMConfig with default values."""
        config = LLMConfig()

        assert config.model == "gpt-4"
        assert config.temperature == 0.1
        assert config.max_tokens == 2000

    def test_llm_config_custom_values(self):
        """Test LLMConfig with custom values."""
        config = LLMConfig(model="gpt-3.5-turbo", temperature=0.5, max_tokens=1000)

        assert config.model == "gpt-3.5-turbo"
        assert config.temperature == 0.5
        assert config.max_tokens == 1000


class TestCallResponsesAPI:
    """Test call_responses_api function."""

    @patch("chirality.core.llm_client.OpenAI")
    def test_successful_api_call(self, mock_openai_class, sample_messages, mock_openai_response):
        """Test successful API call with valid response."""
        # Setup mock client
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client

        # Call function
        response, metadata = call_responses_api(sample_messages)

        # Verify API call
        mock_client.responses.create.assert_called_once()
        call_kwargs = mock_client.responses.create.call_args[1]
        assert call_kwargs["model"] == "gpt-4"
        assert call_kwargs["temperature"] == 0.1
        assert call_kwargs["max_tokens"] == 2000

        # Build expected prompt from messages
        expected_prompt = 'You are a semantic calculator.\n\nResolve these terms: ["A", "B"]'
        assert call_kwargs["prompt"] == expected_prompt

        # Verify response parsing
        assert response["text"] == "Semantic concept resolved"
        assert response["terms_used"] == ["concept", "resolved"]
        assert response["warnings"] == []

        # Verify metadata
        assert metadata["completion_tokens"] == 10
        assert metadata["prompt_tokens"] == 25
        assert metadata["total_tokens"] == 35
        assert metadata["model"] == "gpt-4"
        assert metadata["response_id"] == "response_123"

    @patch("chirality.core.llm_client.OpenAI")
    def test_custom_config(self, mock_openai_class, sample_messages, mock_openai_response):
        """Test API call with custom configuration."""
        # Setup mock client
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client

        # Custom config
        config = LLMConfig(model="gpt-3.5-turbo", temperature=0.7, max_tokens=1500)

        # Call function
        call_responses_api(sample_messages, config)

        # Verify custom config used
        call_kwargs = mock_client.responses.create.call_args[1]
        assert call_kwargs["model"] == "gpt-3.5-turbo"
        assert call_kwargs["temperature"] == 0.7
        assert call_kwargs["max_tokens"] == 1500

    @patch("chirality.core.llm_client.OpenAI")
    def test_invalid_json_response(self, mock_openai_class, sample_messages):
        """Test handling of invalid JSON response."""
        # Setup mock client with invalid JSON
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = "Invalid JSON response"
        mock_client.responses.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        # Should raise ValueError
        with pytest.raises(ValueError, match="Invalid JSON response from LLM"):
            call_responses_api(sample_messages)

    @patch("chirality.core.llm_client.OpenAI")
    def test_missing_required_fields(self, mock_openai_class, sample_messages):
        """Test handling of response missing required fields."""
        # Setup mock client with incomplete response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = MOCK_RESPONSE_INVALID
        mock_response.usage.completion_tokens = 5
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.total_tokens = 15
        mock_response.model = "gpt-4"
        mock_response.id = "response_456"
        mock_client.responses.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        # Should raise ValueError for missing fields
        with pytest.raises(ValueError, match="Missing required field"):
            call_responses_api(sample_messages)

    @patch("chirality.core.llm_client.OpenAI")
    def test_api_exception_handling(self, mock_openai_class, sample_messages):
        """Test handling of OpenAI API exceptions."""
        # Setup mock client that raises exception
        mock_client = Mock()
        mock_client.responses.create.side_effect = Exception("API Error")
        mock_openai_class.return_value = mock_client

        # Should re-raise exception
        with pytest.raises(Exception, match="API Error"):
            call_responses_api(sample_messages)

    def test_empty_messages(self):
        """Test handling of empty messages list."""
        with pytest.raises((ValueError, IndexError)):
            call_responses_api([])

    def test_messages_without_content(self):
        """Test handling of messages without content field."""
        invalid_messages = [
            {"role": "system"},  # Missing content
            {"role": "user", "content": "Valid message"},
        ]

        with pytest.raises((KeyError, ValueError)):
            call_responses_api(invalid_messages)


class TestPromptAssembly:
    """Test prompt assembly from messages."""

    @patch("chirality.core.llm_client.OpenAI")
    def test_single_message_prompt(self, mock_openai_class):
        """Test prompt assembly from single message."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        messages = [{"role": "user", "content": "Single message"}]

        try:
            call_responses_api(messages)
        except:
            pass  # We only care about the prompt assembly

        # Check prompt construction
        call_kwargs = mock_client.responses.create.call_args[1]
        assert call_kwargs["prompt"] == "Single message"

    @patch("chirality.core.llm_client.OpenAI")
    def test_multiple_message_prompt(self, mock_openai_class):
        """Test prompt assembly from multiple messages."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message 1"},
            {"role": "user", "content": "User message 2"},
        ]

        try:
            call_responses_api(messages)
        except:
            pass  # We only care about the prompt assembly

        # Check prompt construction (messages joined with double newlines)
        call_kwargs = mock_client.responses.create.call_args[1]
        expected = "System message\n\nUser message 1\n\nUser message 2"
        assert call_kwargs["prompt"] == expected

    @patch("chirality.core.llm_client.OpenAI")
    def test_whitespace_handling_in_prompt(self, mock_openai_class):
        """Test whitespace handling in prompt assembly."""
        mock_client = Mock()
        mock_openai_class.return_value = mock_client

        messages = [
            {"role": "system", "content": "  System with spaces  "},
            {"role": "user", "content": "\tUser with tabs\t"},
        ]

        try:
            call_responses_api(messages)
        except:
            pass

        # Messages should be joined as-is (content already stripped by builder)
        call_kwargs = mock_client.responses.create.call_args[1]
        expected = "  System with spaces  \n\n\tUser with tabs\t"
        assert call_kwargs["prompt"] == expected


class TestResponseValidation:
    """Test response validation logic."""

    @patch("chirality.core.llm_client.OpenAI")
    def test_valid_response_structure(
        self, mock_openai_class, sample_messages, mock_openai_response
    ):
        """Test validation of valid response structure."""
        mock_client = Mock()
        mock_client.responses.create.return_value = mock_openai_response
        mock_openai_class.return_value = mock_client

        # Should not raise any errors
        response, metadata = call_responses_api(sample_messages)

        # Verify required fields present
        assert "text" in response
        assert "terms_used" in response
        assert "warnings" in response
        assert isinstance(response["text"], str)
        assert isinstance(response["terms_used"], list)
        assert isinstance(response["warnings"], list)

    @patch("chirality.core.llm_client.OpenAI")
    def test_response_with_extra_fields(self, mock_openai_class, sample_messages):
        """Test response with extra fields (should be allowed)."""
        # Response with extra fields
        response_with_extra = {
            "text": "Semantic result",
            "terms_used": ["term1", "term2"],
            "warnings": [],
            "extra_field": "extra_value",
            "confidence": 0.95,
        }

        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = json.dumps(response_with_extra)
        mock_response.usage.completion_tokens = 10
        mock_response.usage.prompt_tokens = 20
        mock_response.usage.total_tokens = 30
        mock_response.model = "gpt-4"
        mock_response.id = "resp_789"
        mock_client.responses.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        # Should succeed and preserve extra fields
        response, metadata = call_responses_api(sample_messages)

        assert response["text"] == "Semantic result"
        assert response["terms_used"] == ["term1", "term2"]
        assert response["warnings"] == []
        assert response.get("extra_field") == "extra_value"  # Extra fields preserved
        assert response.get("confidence") == 0.95


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    @patch("chirality.core.llm_client.OpenAI")
    def test_stage2_multiply_scenario(self, mock_openai_class):
        """Test realistic Stage 2 multiply scenario."""
        # Realistic multiply response
        multiply_response = {
            "text": "coherent semantic integration of conceptual frameworks",
            "terms_used": ["conceptual", "frameworks", "integration"],
            "warnings": ["abstract concepts may need more context"],
        }

        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = json.dumps(multiply_response)
        mock_response.usage.completion_tokens = 15
        mock_response.usage.prompt_tokens = 40
        mock_response.usage.total_tokens = 55
        mock_response.model = "gpt-4"
        mock_response.id = "mult_123"
        mock_client.responses.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        # Realistic multiply messages
        messages = [
            {
                "role": "system",
                "content": "You are a semantic calculator for the Chirality Framework.",
            },
            {
                "role": "user",
                "content": 'Multiply these terms: ["theoretical framework", "practical application"]',
            },
        ]

        response, metadata = call_responses_api(messages)

        # Verify realistic response
        assert "integration" in response["text"]
        assert len(response["terms_used"]) == 3
        assert len(response["warnings"]) == 1
        assert metadata["total_tokens"] == 55

    @patch("chirality.core.llm_client.OpenAI")
    def test_combined_lens_scenario(self, mock_openai_class):
        """Test realistic combined lensing scenario."""
        # Realistic lensing response
        lens_response = {
            "text": "Through the Requirements station lens, theoretical framework × practical application yields implementation methodology that bridges abstract concepts with concrete execution strategies.",
            "terms_used": ["implementation", "methodology", "execution", "strategies"],
            "warnings": [],
        }

        mock_client = Mock()
        mock_response = Mock()
        mock_response.text = json.dumps(lens_response)
        mock_response.usage.completion_tokens = 35
        mock_response.usage.prompt_tokens = 80
        mock_response.usage.total_tokens = 115
        mock_response.model = "gpt-4"
        mock_response.id = "lens_456"
        mock_client.responses.create.return_value = mock_response
        mock_openai_class.return_value = mock_client

        # Realistic combined lens messages with station brief
        messages = [
            {
                "role": "system",
                "content": "You are a semantic calculator for the Chirality Framework.",
            },
            {
                "role": "user",
                "content": "Combined lens: semantic integration through Requirements station: theoretical × practical context for Theory × Practice",
            },
        ]

        response, metadata = call_responses_api(messages)

        # Verify realistic lensing response
        assert "Requirements station" in response["text"]
        assert "methodology" in response["text"]
        assert len(response["terms_used"]) == 4
        assert len(response["warnings"]) == 0
