"""
Phase 1 Output Contracts.

Pydantic models for strict validation of Phase 1 outputs.
Ensures consistent schema for Phase 2 and exporters.
"""

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, Field


Step = Literal[
    "base", "mechanical", "interpreted", "lenses", "lensed", "transpose", "shifted", "constructed"
]


class Meta(BaseModel):
    """Metadata for Phase 1 run."""

    kernel_hash: str
    snapshot_hash: str
    model: str
    timestamp: Optional[str] = None
    token_count: Optional[int] = None


class Matrix(BaseModel):
    """Matrix specification with validation."""

    name: str
    station: str
    rows: List[str]
    cols: List[str]
    elements: List[List[str]]
    step: Step
    op: Optional[str] = None
    # Optional: keep computed lenses for auditing
    lenses: Optional[List[List[str]]] = None


class Principles(BaseModel):
    """Principles extracted from validation."""

    from_: str = Field(alias="from")
    items: List[str]


class Phase1Output(BaseModel):
    """Complete Phase 1 output with strict validation."""

    meta: Meta
    matrices: Dict[str, Matrix]
    principles: Principles

    class Config:
        allow_population_by_field_name = True
