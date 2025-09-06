"""
Tests for CellResolver with new prompt system architecture.

Tests the canonical resolver API with maintainer-authored assets and combined lensing.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

from chirality.core.cell_resolver import CellResolver
from chirality.core.types import RichResult


@pytest.fixture
def mock_builder():
    """Mock PromptBuilder for testing."""
    mock = Mock()

    # Mock build methods to return sample messages
    mock.build_stage2_multiply_messages.return_value = [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": 'Multiply: ["term1", "term2"]'},
    ]

    mock.build_stage2_elementwise_messages.return_value = [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": 'Element-wise: ["elem1", "elem2"]'},
    ]

    mock.build_stage2_addition.return_value = (
        "frame applied to frame the problem; resolve to resolve the problem."
    )

    mock.build_combined_lens_messages.return_value = [
        {"role": "system", "content": "System message"},
        {"role": "user", "content": "Combined lens: content through station for row × col"},
    ]

    # Mock provenance
    mock.get_asset_provenance.return_value = [
        {"id": "system", "sha256": "abc123", "version": "1.0.0"},
        {"id": "ops.multiply", "sha256": "def456", "version": "1.0.0"},
    ]

    return mock


@pytest.fixture
def mock_llm_response():
    """Mock LLM API response."""
    return (
        {"text": "semantic result", "terms_used": ["semantic", "result"], "warnings": []},
        {
            "completion_tokens": 10,
            "prompt_tokens": 20,
            "total_tokens": 30,
            "model": "gpt-4",
            "response_id": "resp_123",
        },
    )


class TestCellResolverInitialization:
    """Test CellResolver initialization."""

    @patch("chirality.core.cell_resolver.PromptBuilder")
    def test_resolver_initialization(self, mock_builder_class):
        """Test resolver initializes with prompt builder."""
        resolver = CellResolver()

        mock_builder_class.assert_called_once()
        assert resolver.builder is not None

    @patch("chirality.core.cell_resolver.PromptBuilder")
    def test_resolver_with_custom_builder(self, mock_builder_class):
        """Test resolver can use custom builder."""
        custom_builder = Mock()
        resolver = CellResolver()
        resolver.builder = custom_builder

        assert resolver.builder is custom_builder


class TestStage2Operations:
    """Test Stage 2 semantic operations."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    def test_run_stage2_multiply(self, mock_api, mock_builder, mock_llm_response):
        """Test Stage 2 multiply operation."""
        mock_api.return_value = mock_llm_response

        resolver = CellResolver()
        resolver.builder = mock_builder

        # Call multiply
        result = resolver.run_stage2_multiply(["term1", "term2"], "C")

        # Verify builder calls
        mock_builder.build_stage2_multiply_messages.assert_called_once_with(["term1", "term2"])
        mock_builder.get_asset_provenance.assert_called_once()

        # Verify API call
        mock_api.assert_called_once()

        # Verify result
        assert isinstance(result, RichResult)
        assert result.text == "semantic result"
        assert result.terms_used == ["semantic", "result"]
        assert result.warnings == []
        assert "operation" in result.metadata
        assert result.metadata["operation"] == "stage2_multiply"

    @patch("chirality.core.cell_resolver.call_responses_api")
    def test_run_stage2_elementwise(self, mock_api, mock_builder, mock_llm_response):
        """Test Stage 2 element-wise operation."""
        mock_api.return_value = mock_llm_response

        resolver = CellResolver()
        resolver.builder = mock_builder

        # Call elementwise
        result = resolver.run_stage2_elementwise(["elem1", "elem2"], "F")

        # Verify builder calls
        mock_builder.build_stage2_elementwise_messages.assert_called_once_with(["elem1", "elem2"])

        # Verify result
        assert isinstance(result, RichResult)
        assert result.text == "semantic result"
        assert result.metadata["operation"] == "stage2_elementwise"

    def test_run_stage2_addition(self, mock_builder):
        """Test Stage 2 addition (mechanical, no LLM)."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        # Call addition
        result = resolver.run_stage2_addition(["part1", "part2"], "D")

        # Verify builder call
        mock_builder.build_stage2_addition.assert_called_once_with(["part1", "part2"])

        # Verify result (string, not RichResult)
        assert isinstance(result, str)
        assert "frame" in result
        assert "resolve" in result


class TestCombinedLensing:
    """Test combined lensing operations."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.core.cell_resolver.PromptStrategy")
    def test_run_combined_lens(self, mock_strategy, mock_api, mock_builder, mock_llm_response):
        """Test combined lensing operation."""
        mock_api.return_value = mock_llm_response

        # Mock strategy calls
        mock_strategy.plan.return_value = ["system", "lens.combined"]
        mock_strategy.get_station_brief_id.return_value = "station.requirements"

        resolver = CellResolver()
        resolver.builder = mock_builder

        # Call combined lens
        result = resolver.run_combined_lens(
            content="semantic content", component_id="C", row_label="Theory", col_label="Practice"
        )

        # Verify strategy calls
        mock_strategy.plan.assert_called_once_with("combined_lens", "C")
        mock_strategy.get_station_brief_id.assert_called_once_with("C")

        # Verify builder calls
        mock_builder.build_combined_lens_messages.assert_called_once_with(
            "C", "Theory", "Practice", "semantic content"
        )

        # Verify provenance includes station brief
        expected_asset_ids = ["system", "lens.combined", "station.requirements"]
        mock_builder.get_asset_provenance.assert_called_once_with(expected_asset_ids)

        # Verify API call
        mock_api.assert_called_once()

        # Verify result
        assert isinstance(result, RichResult)
        assert result.metadata["operation"] == "combined_lens"

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.core.cell_resolver.PromptStrategy")
    def test_combined_lens_z_component(
        self, mock_strategy, mock_api, mock_builder, mock_llm_response
    ):
        """Test combined lensing for Z component (includes shift)."""
        mock_api.return_value = mock_llm_response

        # Mock strategy calls for Z (includes shift)
        mock_strategy.plan.return_value = ["system", "ops.shift", "lens.combined"]
        mock_strategy.get_station_brief_id.return_value = "station.validation"

        resolver = CellResolver()
        resolver.builder = mock_builder

        # Call combined lens for Z
        result = resolver.run_combined_lens(
            content="verification content",
            component_id="Z",
            row_label="Verification",
            col_label="Outcome",
        )

        # Verify strategy calls for Z
        mock_strategy.plan.assert_called_once_with("combined_lens", "Z")
        mock_strategy.get_station_brief_id.assert_called_once_with("Z")

        # Verify provenance includes shift assets
        expected_asset_ids = ["system", "ops.shift", "lens.combined", "station.validation"]
        mock_builder.get_asset_provenance.assert_called_once_with(expected_asset_ids)

        assert isinstance(result, RichResult)


class TestShiftOperation:
    """Test shift operation for Z component."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.core.cell_resolver.PromptStrategy")
    def test_run_shift(self, mock_strategy, mock_api, mock_builder, mock_llm_response):
        """Test shift operation (Verification → Validation)."""
        mock_api.return_value = mock_llm_response
        mock_strategy.plan.return_value = ["system", "ops.shift"]

        # Mock registry to return asset text
        mock_registry = Mock()
        mock_registry.get_text.side_effect = lambda asset_id: {
            "system": "System prompt",
            "ops.shift": "Shift {{content}} from verification to validation",
        }[asset_id]

        resolver = CellResolver()
        resolver.builder = mock_builder
        resolver.builder.registry = mock_registry

        # Call shift
        result = resolver.run_shift("verification content", "Z")

        # Verify strategy call
        mock_strategy.plan.assert_called_once_with("shift", "Z")

        # Verify API call made
        mock_api.assert_called_once()

        # Verify result
        assert isinstance(result, RichResult)
        assert result.metadata["operation"] == "shift"

    def test_run_shift_invalid_component(self, mock_builder):
        """Test shift with invalid component (not Z)."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        # Should raise for non-Z components
        with pytest.raises(ValueError, match="Shift operation only valid for component Z"):
            resolver.run_shift("content", "C")


class TestPrivateMethods:
    """Test private helper methods."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    def test_call_llm_with_provenance(self, mock_api, mock_builder, mock_llm_response):
        """Test _call_llm with provenance tracking."""
        mock_api.return_value = mock_llm_response

        resolver = CellResolver()
        resolver.builder = mock_builder

        messages = [{"role": "system", "content": "test"}]
        asset_provenance = [{"id": "test", "sha256": "abc123", "version": "1.0.0"}]

        response, metadata = resolver._call_llm(messages, asset_provenance, "test_op")

        # Verify API called
        mock_api.assert_called_once_with(messages, None)  # Default config

        # Verify metadata enriched
        assert metadata["operation"] == "test_op"
        assert "prompt_hash" in metadata
        assert metadata["assets"] == asset_provenance
        assert metadata["strategy"] == "combined"

    def test_validate_response_valid(self, mock_builder):
        """Test response validation with valid response."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        valid_response = {"text": "result", "terms_used": ["term"], "warnings": []}

        # Should not raise
        resolver._validate_response(valid_response)

    def test_validate_response_missing_field(self, mock_builder):
        """Test response validation with missing field."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        invalid_response = {
            "text": "result",
            # Missing terms_used and warnings
        }

        with pytest.raises(ValueError, match="Missing required field"):
            resolver._validate_response(invalid_response)

    def test_validate_response_wrong_type(self, mock_builder):
        """Test response validation with wrong field types."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        # Text should be string
        invalid_response = {"text": 123, "terms_used": ["term"], "warnings": []}  # Should be string

        with pytest.raises(ValueError, match="'text' field must be string"):
            resolver._validate_response(invalid_response)

        # terms_used should be list
        invalid_response2 = {
            "text": "result",
            "terms_used": "not a list",  # Should be list
            "warnings": [],
        }

        with pytest.raises(ValueError, match="'terms_used' field must be array"):
            resolver._validate_response(invalid_response2)

    def test_hash_messages(self, mock_builder):
        """Test message hashing for provenance."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        messages = [{"role": "system", "content": "system"}, {"role": "user", "content": "user"}]

        hash1 = resolver._hash_messages(messages)
        hash2 = resolver._hash_messages(messages)

        # Same messages should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex length

        # Different messages should produce different hash
        different_messages = [{"role": "system", "content": "different"}]
        hash3 = resolver._hash_messages(different_messages)
        assert hash1 != hash3

    def test_infer_station_from_provenance(self, mock_builder):
        """Test station inference from asset provenance."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        # With station asset
        provenance_with_station = [
            {"id": "system", "sha256": "abc"},
            {"id": "station.requirements", "sha256": "def"},
        ]

        station = resolver._infer_station(provenance_with_station)
        assert station == "requirements"

        # Without station asset
        provenance_without_station = [
            {"id": "system", "sha256": "abc"},
            {"id": "ops.multiply", "sha256": "def"},
        ]

        station = resolver._infer_station(provenance_without_station)
        assert station is None


class TestRichResultBuilding:
    """Test RichResult construction from responses."""

    def test_build_rich_result(self, mock_builder):
        """Test building RichResult from response and metadata."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        response = {
            "text": "semantic result",
            "terms_used": ["term1", "term2"],
            "warnings": ["warning1"],
        }

        metadata = {"operation": "test_op", "model": "gpt-4", "total_tokens": 50}

        asset_provenance = [{"id": "test", "version": "1.0.0"}]

        result = resolver._build_rich_result(response, metadata, asset_provenance)

        assert isinstance(result, RichResult)
        assert result.text == "semantic result"
        assert result.terms_used == ["term1", "term2"]
        assert result.warnings == ["warning1"]
        assert result.metadata == metadata

    def test_build_rich_result_with_defaults(self, mock_builder):
        """Test building RichResult with missing optional fields."""
        resolver = CellResolver()
        resolver.builder = mock_builder

        # Response missing some optional fields
        response = {
            "text": "result"
            # Missing terms_used and warnings - should use defaults
        }

        metadata = {"operation": "test"}

        result = resolver._build_rich_result(response, metadata, [])

        assert result.text == "result"
        assert result.terms_used == []  # Default empty list
        assert result.warnings == []  # Default empty list


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.core.cell_resolver.PromptStrategy")
    def test_matrix_c_computation_flow(self, mock_strategy, mock_api, mock_builder):
        """Test complete Matrix C computation flow."""
        # Mock multiply response
        multiply_response = (
            {
                "text": "theoretical framework × practical implementation",
                "terms_used": ["theoretical", "framework", "practical", "implementation"],
                "warnings": [],
            },
            {"operation": "multiply", "total_tokens": 40},
        )

        # Mock lens response
        lens_response = (
            {
                "text": "Requirements perspective on theoretical framework × practical implementation yields systematic development methodology",
                "terms_used": ["systematic", "development", "methodology"],
                "warnings": [],
            },
            {"operation": "lens", "total_tokens": 60},
        )

        # Setup API to return different responses
        mock_api.side_effect = [multiply_response, lens_response]

        # Setup strategy
        mock_strategy.plan.side_effect = [
            ["system", "ops.multiply"],  # Stage 2
            ["system", "lens.combined"],  # Combined lens
        ]
        mock_strategy.get_station_brief_id.return_value = "station.requirements"

        resolver = CellResolver()
        resolver.builder = mock_builder

        # Stage 2: Multiply
        stage2_result = resolver.run_stage2_multiply(
            ["theoretical framework", "practical implementation"], "C"
        )

        # Stage 3: Combined lens
        final_result = resolver.run_combined_lens(
            content=stage2_result.text, component_id="C", row_label="Theory", col_label="Practice"
        )

        # Verify complete flow
        assert "theoretical framework × practical implementation" in stage2_result.text
        assert "Requirements perspective" in final_result.text
        assert "methodology" in final_result.text
        assert len(final_result.terms_used) == 3
