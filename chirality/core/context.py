"""
SemanticContext for Chirality Framework three-stage interpretation pipeline.

This dataclass carries all the valley context, ontological coordinates,
and operation details needed for fragment-based prompt composition.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SemanticContext:
    """
    Complete context for semantic operations in the three-stage pipeline.

    Carries all the information needed for fragment-based prompt composition
    AND tracing. This is the single, canonical context object used throughout the framework.

    Includes:
    - Valley position and station context
    - Ontological coordinates (row/column labels)
    - Cell coordinates for tracing (matrix, i, j)
    - Operation type and terms to process
    """

    # Valley position
    station_context: str  # "Requirements", "Objectives", etc.
    valley_summary: str  # "Problem Statement → [Requirements] → Objectives..."

    # Ontological coordinates
    row_label: str  # Row ontology label ("Normative", "Operative", etc.)
    col_label: str  # Column ontology label ("Determinacy", "Sufficiency", etc.)

    # Operation specifics
    operation_type: str  # "*", "⊙", "synthesize", "interpret"
    terms: Dict[str, Any]  # The actual content to process

    # Cell coordinates for tracing
    matrix: str  # "C", "F", "D", "X", "Z", "E" - target matrix being computed
    i: int  # Row index in target matrix
    j: int  # Column index in target matrix

    def __post_init__(self) -> None:
        """Validate the context after initialization."""
        if not self.station_context:
            raise ValueError("station_context is required")
        if not self.valley_summary:
            raise ValueError("valley_summary is required")
        if not self.operation_type:
            raise ValueError("operation_type is required")
        if not self.terms:
            raise ValueError("terms dictionary is required")
