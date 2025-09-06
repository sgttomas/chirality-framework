"""
Integration tests for the new prompt system architecture.

Tests the complete flow: PromptStrategy -> PromptBuilder -> CellResolver.
Uses mocks to avoid dependencies on actual OpenAI API calls or file system.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any
import json

from chirality.lib.strategies import PromptStrategy
from chirality.lib.prompt_builder import PromptBuilder
from chirality.core.cell_resolver import CellResolver
from chirality.core.types import RichResult


class TestPromptSystemIntegration:
    """Integration tests for the complete prompt system."""

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.lib.prompt_builder.PromptRegistry")
    def test_complete_stage2_multiply_flow(self, mock_registry_class, mock_api):
        """Test complete Stage 2 multiply flow from strategy to resolver."""

        # Mock registry responses
        mock_registry = Mock()
        mock_registry.get_text.side_effect = lambda asset_id: {
            "system": "You are a semantic calculator.",
            "ops.multiply": "Multiply: {{terms}}",
        }.get(asset_id, f"Mock content for {asset_id}")

        mock_registry.get.return_value = Mock(
            id="system", sha256="abc123", version="1.0.0", text="Mock content"
        )

        mock_registry_class.return_value = mock_registry

        # Mock API response
        mock_response = {
            "text": "theoretical framework integrated with practical implementation",
            "terms_used": ["theoretical", "framework", "practical", "implementation"],
            "warnings": [],
        }

        mock_metadata = {
            "completion_tokens": 15,
            "prompt_tokens": 30,
            "total_tokens": 45,
            "model": "gpt-4",
            "response_id": "resp_123",
        }

        mock_api.return_value = (mock_response, mock_metadata)

        # Test flow
        resolver = CellResolver()
        result = resolver.run_stage2_multiply(
            ["theoretical framework", "practical implementation"], "C"
        )

        # Verify strategy planning worked
        expected_asset_ids = PromptStrategy.plan("stage2_multiply", "C")
        assert expected_asset_ids == ["system", "ops.multiply"]

        # Verify API was called
        mock_api.assert_called_once()

        # Verify result structure
        assert isinstance(result, RichResult)
        assert result.text == "theoretical framework integrated with practical implementation"
        assert len(result.terms_used) == 4
        assert result.warnings == []
        assert "operation" in result.metadata
        assert result.metadata["operation"] == "stage2_multiply"

    @patch("chirality.core.cell_resolver.call_responses_api")
    @patch("chirality.lib.prompt_builder.PromptRegistry")
    @patch("chirality.core.cell_resolver.PromptStrategy")
    def test_complete_combined_lens_flow(self, mock_strategy, mock_registry_class, mock_api):
        """Test complete combined lensing flow."""

        # Mock strategy responses
        mock_strategy.plan.return_value = ["system", "lens.combined"]
        mock_strategy.get_station_brief_id.return_value = "station.requirements"

        # Mock registry responses
        mock_registry = Mock()
        mock_registry.get_text.side_effect = lambda asset_id: {
            "system": "You are a semantic calculator.",
            "lens.combined": "Combined lens: {{content}} through {{station_brief}} for {{row_label}} × {{col_label}}",
            "station.requirements": "Requirements context for {{row_label}} × {{col_label}}",
        }.get(asset_id, f"Mock content for {asset_id}")

        mock_registry.get.return_value = Mock(id="test", sha256="def456", version="1.0.0")

        mock_registry_class.return_value = mock_registry

        # Mock API response
        mock_response = {
            "text": "Through Requirements lens, semantic integration yields systematic methodology for Theory × Practice implementation",
            "terms_used": ["systematic", "methodology", "implementation"],
            "warnings": [],
        }

        mock_metadata = {
            "completion_tokens": 25,
            "prompt_tokens": 50,
            "total_tokens": 75,
            "model": "gpt-4",
            "response_id": "lens_456",
        }

        mock_api.return_value = (mock_response, mock_metadata)

        # Test combined lensing flow
        resolver = CellResolver()
        result = resolver.run_combined_lens(
            content="semantic integration",
            component_id="C",
            row_label="Theory",
            col_label="Practice",
        )

        # Verify strategy calls
        mock_strategy.plan.assert_called_once_with("combined_lens", "C")
        mock_strategy.get_station_brief_id.assert_called_once_with("C")

        # Verify API was called
        mock_api.assert_called_once()

        # Verify result
        assert isinstance(result, RichResult)
        assert "Requirements lens" in result.text
        assert "methodology" in result.text
        assert result.metadata["operation"] == "combined_lens"

    def test_strategy_component_mapping_consistency(self):
        """Test that strategy mappings are consistent."""

        # Test all components have valid mappings
        components = ["C", "D", "F", "X", "Z", "E"]

        for component in components:
            # Should have station mapping
            station_brief = PromptStrategy.get_station_brief_id(component)
            assert station_brief.startswith("station.")

            # Should have operator mapping (or None for Z)
            operator = PromptStrategy.get_stage2_operator(component)
            if component == "Z":
                assert operator is None
            else:
                assert operator is not None

            # Should have pipeline stages
            stages = PromptStrategy.get_pipeline_stages(component)
            assert isinstance(stages, list)
            assert len(stages) > 0
            assert "combined_lens" in stages  # All have combined lensing

    def test_component_station_relationships(self):
        """Test correct component to station relationships."""

        expected_mappings = {
            "C": "station.requirements",
            "D": "station.objectives",
            "F": "station.objectives",
            "X": "station.verification",
            "Z": "station.validation",
            "E": "station.evaluation",
        }

        for component, expected_station in expected_mappings.items():
            actual_station = PromptStrategy.get_station_brief_id(component)
            assert (
                actual_station == expected_station
            ), f"Component {component} maps to wrong station"

    def test_stage2_operator_relationships(self):
        """Test Stage 2 operator relationships."""

        expected_operators = {
            "C": "ops.multiply",  # Semantic multiplication
            "D": "ops.add",  # Mechanical addition
            "F": "ops.elementwise",  # Element-wise operation
            "X": "ops.multiply",  # Semantic multiplication
            "Z": None,  # No Stage 2, direct to combined lens
            "E": "ops.multiply",  # Semantic multiplication
        }

        for component, expected_operator in expected_operators.items():
            actual_operator = PromptStrategy.get_stage2_operator(component)
            assert actual_operator == expected_operator, f"Component {component} has wrong operator"

    def test_mechanical_vs_llm_operations(self):
        """Test distinction between mechanical and LLM operations."""

        # Only D should be mechanical (Stage 2)
        assert PromptStrategy.is_mechanical_stage2("D") == True

        # All others should use LLM for Stage 2
        for component in ["C", "F", "X", "E"]:
            assert PromptStrategy.is_mechanical_stage2(component) == False

        # Z has no Stage 2, so not mechanical
        assert PromptStrategy.is_mechanical_stage2("Z") == False

    @patch("chirality.lib.prompt_builder.PromptRegistry")
    def test_placeholder_substitution_in_messages(self, mock_registry_class):
        """Test that placeholder substitution works in message building."""

        # Mock registry with placeholder content
        mock_registry = Mock()
        mock_registry.get_text.side_effect = lambda asset_id: {
            "system": "System: You are a semantic calculator for {{framework}}.",
            "ops.multiply": "Multiply these {{count}} terms: {{terms}}",
            "station.requirements": "Requirements for {{row_label}} × {{col_label}}: {{content}}",
        }.get(asset_id, f"Mock {asset_id}")

        mock_registry.get.return_value = Mock(id="mock", sha256="abc", version="1.0")
        mock_registry_class.return_value = mock_registry

        builder = PromptBuilder()

        # Test Stage 2 multiply with terms substitution
        messages = builder.build_stage2_multiply_messages(["term1", "term2"])

        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert messages[1]["role"] == "user"

        # Should have JSON array in user message
        assert '["term1", "term2"]' in messages[1]["content"]

    def test_asset_provenance_tracking(self):
        """Test that asset provenance is tracked correctly."""

        # This test verifies the design without mocking
        # Strategy should return correct asset sequences

        # Stage 2 multiply should use system + multiply operator
        multiply_assets = PromptStrategy.plan("stage2_multiply", "C")
        assert multiply_assets == ["system", "ops.multiply"]

        # Combined lensing should include system + lens
        lens_assets = PromptStrategy.plan("combined_lens", "C")
        assert lens_assets == ["system", "lens.combined"]

        # Z combined lensing should include shift
        z_lens_assets = PromptStrategy.plan("combined_lens", "Z")
        assert z_lens_assets == ["system", "ops.shift", "lens.combined"]

        # Station briefs should be correctly mapped
        c_station = PromptStrategy.get_station_brief_id("C")
        assert c_station == "station.requirements"

        e_station = PromptStrategy.get_station_brief_id("E")
        assert e_station == "station.evaluation"

    def test_error_handling_in_strategy(self):
        """Test error handling in strategy planning."""

        # Invalid component should raise
        with pytest.raises(ValueError, match="Invalid component_id"):
            PromptStrategy.plan("stage2_multiply", "INVALID")

        # Invalid stage should raise
        with pytest.raises(ValueError, match="Invalid stage"):
            PromptStrategy.plan("invalid_stage", "C")

        # Wrong operator for component should raise
        with pytest.raises(ValueError, match="does not use multiply operator"):
            PromptStrategy.plan("stage2_multiply", "F")  # F uses elementwise

        # Shift only valid for Z
        with pytest.raises(ValueError, match="Shift operation only valid for component Z"):
            PromptStrategy.plan("shift", "C")


class TestPromptArchitectureDesign:
    """Test the architectural design principles of the prompt system."""

    def test_single_source_of_truth_for_mappings(self):
        """Test that all mappings come from single strategy class."""

        # All component-to-station mappings should come from PromptStrategy
        components = ["C", "D", "F", "X", "Z", "E"]

        for component in components:
            # Should be able to get station brief
            station_brief = PromptStrategy.get_station_brief_id(component)
            assert isinstance(station_brief, str)
            assert station_brief.startswith("station.")

            # Should be able to get pipeline stages
            pipeline = PromptStrategy.get_pipeline_stages(component)
            assert isinstance(pipeline, list)

            # Should be able to get operator (or None)
            operator = PromptStrategy.get_stage2_operator(component)
            assert operator is None or isinstance(operator, str)

    def test_no_optionality_in_pipeline(self):
        """Test that pipeline has no optionality - fixed sequences."""

        # Each component should have exactly one pipeline sequence
        for component in ["C", "D", "F", "X", "Z", "E"]:
            pipeline1 = PromptStrategy.get_pipeline_stages(component)
            pipeline2 = PromptStrategy.get_pipeline_stages(component)

            # Should be identical (deterministic)
            assert pipeline1 == pipeline2

            # Should be non-empty
            assert len(pipeline1) > 0

    def test_asset_id_consistency(self):
        """Test that asset IDs follow consistent naming conventions."""

        # All station assets should start with 'station.'
        for component in ["C", "D", "F", "X", "Z", "E"]:
            station_brief = PromptStrategy.get_station_brief_id(component)
            assert station_brief.startswith("station.")

        # All operator assets should start with 'ops.'
        for component in ["C", "F", "X", "E"]:  # Multiply/elementwise components
            operator = PromptStrategy.get_stage2_operator(component)
            assert operator.startswith("ops.")

        # System asset should be just 'system'
        multiply_assets = PromptStrategy.plan("stage2_multiply", "C")
        assert "system" in multiply_assets

    def test_combined_lensing_universality(self):
        """Test that all components use combined lensing in Stage 3."""

        # All components should have combined_lens in their pipeline
        for component in ["C", "D", "F", "X", "Z", "E"]:
            pipeline = PromptStrategy.get_pipeline_stages(component)
            assert "combined_lens" in pipeline

        # Combined lens should be the final stage for all
        for component in ["C", "D", "F", "X", "Z", "E"]:
            pipeline = PromptStrategy.get_pipeline_stages(component)
            assert pipeline[-1] == "combined_lens"

    def test_maintainer_authority_over_semantics(self):
        """Test that semantic content comes from maintainer assets."""

        # This test verifies architectural principle:
        # All semantic content should come from maintainer-authored assets

        # Strategy should only provide asset IDs, not content
        assets = PromptStrategy.plan("stage2_multiply", "C")
        for asset_id in assets:
            assert isinstance(asset_id, str)
            assert len(asset_id) > 0
            # Asset IDs should be identifiers, not content
            assert not asset_id.startswith("You are")  # Not direct content
            assert not asset_id.startswith("Multiply")  # Not direct content


# Mark completed test creation
@pytest.mark.integration
class TestPromptSystemArchitecture:
    """High-level architecture validation tests."""

    def test_architecture_completeness(self):
        """Test that architecture covers all matrix operations."""

        # All matrix components should be supported
        supported_components = ["C", "D", "F", "X", "Z", "E"]

        for component in supported_components:
            # Should have complete pipeline definition
            pipeline = PromptStrategy.get_pipeline_stages(component)
            assert len(pipeline) > 0

            # Should have station mapping
            station = PromptStrategy.get_station_brief_id(component)
            assert station is not None

            # Should have operator mapping (or explicit None for Z)
            operator = PromptStrategy.get_stage2_operator(component)
            assert operator is not None or component == "Z"

    def test_semantic_valley_coverage(self):
        """Test that all semantic valley stations are covered."""

        # Expected stations from the semantic valley
        expected_stations = {
            "station.requirements",
            "station.objectives",
            "station.verification",
            "station.validation",
            "station.evaluation",
        }

        # Collect all stations used by components
        used_stations = set()
        for component in ["C", "D", "F", "X", "Z", "E"]:
            station = PromptStrategy.get_station_brief_id(component)
            used_stations.add(station)

        # Should cover all expected stations
        assert used_stations == expected_stations

    def test_operation_type_coverage(self):
        """Test that all operation types are supported."""

        # Should support multiply, elementwise, add, and shift operations
        operators_used = set()

        for component in ["C", "D", "F", "X", "Z", "E"]:
            operator = PromptStrategy.get_stage2_operator(component)
            if operator:  # Z has None
                operators_used.add(operator)

        expected_operators = {"ops.multiply", "ops.elementwise", "ops.add"}

        assert operators_used == expected_operators
