"""
Chirality Framework - Semantic Calculator

A fixed, canonical "semantic calculator" for structured problem-solving.
Not a framework but a precise algorithm with a 3-stage interpretation pipeline.
"""

# Read version from VERSION.md (single source of truth)
from pathlib import Path
try:
    version_path = Path(__file__).parent.parent / "VERSION.md"
    with open(version_path, "r") as f:
        __version__ = f.readline().split("—")[0].strip()
except Exception:
    __version__ = "0.0.0"  # Fallback version
__author__ = "Chirality Framework Team"

from .core.types import Cell, Matrix
from .core.context import SemanticContext
from .core.cell_resolver import CellResolver
from .core.resolvers import EchoResolver
from .core.operations import (
    compute_cell_C,
    compute_cell_F,
    compute_cell_D,
    compute_matrix_C,
    compute_matrix_F,
    compute_matrix_D
)
from .core.matrices import MATRIX_A, MATRIX_B, MATRIX_J
from .core.validate import FrameworkValidationError, validate_matrix, validate_cell
from .core.tracer import JSONLTracer

__all__ = [
    # Core types
    "Cell",
    "Matrix", 
    "SemanticContext",
    # Canonical matrices
    "MATRIX_A",
    "MATRIX_B",
    "MATRIX_J",
    # Resolvers
    "CellResolver",
    "EchoResolver",
    # Cell-level operations (the core algorithm)
    "compute_cell_C",
    "compute_cell_F",
    "compute_cell_D",
    # Matrix-level operations (convenience wrappers)
    "compute_matrix_C",
    "compute_matrix_F",
    "compute_matrix_D",
    # Validation
    "FrameworkValidationError",
    "validate_matrix",
    "validate_cell",
    # Tracing
    "JSONLTracer",
]
