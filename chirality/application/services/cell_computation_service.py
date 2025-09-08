"""
Application service for cell computation.

Orchestrates domain logic with infrastructure services.
This is where the domain rules meet the real world.
"""

from typing import Optional, Protocol
from ...core.types import Cell, Matrix
from ...domain.pipeline.stages import PipelineStage, get_matrix_pipeline_stages
from ...domain.semantics.operations import SemanticOperation, SemanticOperationType


class LLMResolver(Protocol):
    """Interface for LLM resolvers (dependency inversion)."""

    def run_stage2_multiply(self, terms, component_id: str):
        """Resolve semantic multiplication."""
        ...

    def run_stage2_elementwise(self, terms, component_id: str):
        """Resolve elementwise operation."""
        ...

    def run_combined_lens(self, content: str, component_id: str, row_label: str, col_label: str):
        """Apply combined lensing."""
        ...

    def run_shift(self, content: str, component_id: str):
        """Apply station shift for Z matrix."""
        ...


class Tracer(Protocol):
    """Interface for tracing (dependency inversion)."""

    def trace_stage(self, stage_name: str, context: dict, result):
        """Trace a pipeline stage."""
        ...


class CellComputationService:
    """
    Application service for computing matrix cells.

    Orchestrates domain logic with infrastructure services without
    being coupled to specific implementations.
    """

    def __init__(self, resolver: LLMResolver, tracer: Optional[Tracer] = None):
        """
        Initialize service with dependencies.

        Args:
            resolver: LLM resolver implementation
            tracer: Optional tracer for observability
        """
        self.resolver = resolver
        self.tracer = tracer

    def compute_cell(
        self,
        matrix_type: str,
        row: int,
        col: int,
        source_matrices: dict,
        row_label: str,
        col_label: str,
    ) -> Cell:
        """
        Compute a single matrix cell using domain rules.

        Args:
            matrix_type: Matrix component ('C', 'D', 'F', 'X', 'Z', 'E')
            row: Row index
            col: Column index
            source_matrices: Input matrices
            row_label: Row ontology label
            col_label: Column ontology label

        Returns:
            Computed cell with full provenance
        """
        # Get pipeline stages from domain rules
        stages = get_matrix_pipeline_stages(matrix_type)

        # Stage 1: Mechanical construction (domain logic)
        stage1_result = self._execute_stage1(matrix_type, row, col, source_matrices)

        # Stage 2: Semantic resolution (LLM via infrastructure)
        stage2_result = self._execute_stage2(matrix_type, stage1_result)

        # Stage 3: Combined lensing (LLM via infrastructure)
        stage3_result = self._execute_stage3(matrix_type, stage2_result, row_label, col_label)

        # Build final cell with provenance
        return Cell(
            row=row,
            col=col,
            value=stage3_result.text,
            provenance={
                "operation": f"compute_{matrix_type}",
                "coordinates": f"({row_label}, {col_label})",
                "stage_1_construct": stage1_result,
                "stage_2_semantic": stage2_result,
                "stage_3_combined_lensed": stage3_result,
            },
        )

    def _execute_stage1(self, matrix_type: str, row: int, col: int, source_matrices: dict):
        """Execute Stage 1 using domain logic."""
        # This would implement the mechanical construction logic
        # For now, placeholder that maintains interface
        return {
            "texts": ["placeholder", "k-products"],
            "metadata": {"stage": "construct"},
            "terms_used": ["term1", "term2"],
            "warnings": [],
        }

    def _execute_stage2(self, matrix_type: str, stage1_result):
        """Execute Stage 2 using LLM resolver."""
        # Use domain rules to determine operation type
        if matrix_type in ["C", "X", "E"]:
            return self.resolver.run_stage2_multiply(stage1_result["texts"], matrix_type)
        elif matrix_type == "F":
            return self.resolver.run_stage2_elementwise(stage1_result["texts"], matrix_type)
        elif matrix_type == "D":
            # Mechanical addition - no LLM call
            return {
                "text": " applied to frame the problem; ".join(stage1_result["texts"])
                + " to resolve the problem.",
                "metadata": {"stage": "mechanical_addition"},
                "terms_used": stage1_result["texts"],
                "warnings": [],
            }
        else:
            raise ValueError(f"Unknown matrix type: {matrix_type}")

    def _execute_stage3(self, matrix_type: str, stage2_result, row_label: str, col_label: str):
        """Execute Stage 3 using LLM resolver."""
        # Use domain rules for lensing type
        if matrix_type == "Z":
            return self.resolver.run_shift(stage2_result["text"], matrix_type)
        else:
            return self.resolver.run_combined_lens(
                stage2_result["text"], matrix_type, row_label, col_label
            )
