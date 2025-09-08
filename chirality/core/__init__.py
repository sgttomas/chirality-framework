"""
Core Chirality Framework semantic calculator modules.
"""

# Import shims for backward compatibility - TODO: remove after migration
from ..domain.types import Cell, Matrix
from ..infrastructure.llm.resolver import CellResolver
from ..infrastructure.llm.mock_resolvers import EchoResolver
from ..application.services.pipeline_service import (
    compute_cell_C,
    compute_cell_F,
    compute_cell_D,
    compute_matrix_C,
    compute_matrix_F,
    compute_matrix_D,
)
from ..domain.matrices.canonical import MATRIX_A, MATRIX_B, MATRIX_J
from ..domain.validation import FrameworkValidationError
from ..infrastructure.monitoring.tracer import JSONLTracer

__all__ = [
    # Core types
    "Cell",
    "Matrix",
    # Resolvers
    "CellResolver",
    "EchoResolver",
    # Operations (cell-level)
    "compute_cell_C",
    "compute_cell_F",
    "compute_cell_D",
    # Operations (matrix-level)
    "compute_matrix_C",
    "compute_matrix_F",
    "compute_matrix_D",
    # Canonical matrices
    "MATRIX_A",
    "MATRIX_B",
    "MATRIX_J",
    # Validation
    "FrameworkValidationError",
    # Tracing
    "JSONLTracer",
]
