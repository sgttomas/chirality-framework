"""
Test configuration for MVTS (Minimum Viable Test Suite).

Fresh test fixtures for the new two-phase architecture.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any

from chirality.infrastructure.llm.mock_resolvers import EchoResolver
from chirality.domain.matrices.canonical import get_canonical_matrix


@pytest.fixture
def echo_resolver():
    """Deterministic echo resolver for testing without LLM calls."""
    return EchoResolver()


@pytest.fixture
def temp_artifacts_dir():
    """Temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_phase1_output():
    """Sample Phase 1 output structure for contract testing."""
    return {
        "meta": {
            "kernel_hash": "abc123def456",
            "snapshot_hash": "xyz789uvw123",
            "model": "gpt-4"
        },
        "matrices": {
            "A": {
                "name": "A",
                "station": "Problem Statement",
                "rows": ["normative", "operative", "iterative"],
                "cols": ["guiding", "applying", "judging", "reflecting"],
                "elements": [
                    ["objectives", "actions", "benchmarks", "feedback"],
                    ["standards", "methods", "criteria", "adaptation"],
                    ["development", "coordination", "evaluation", "refinement"]
                ],
                "step": "base"
            },
            "B": {
                "name": "B", 
                "station": "Problem Statement",
                "rows": ["data", "information", "knowledge", "wisdom"],
                "cols": ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"],
                "elements": [
                    ["necessary", "sufficient", "complete", "consistent"],
                    ["contingent", "insufficient", "incomplete", "inconsistent"],
                    ["purposeful", "effective", "comprehensive", "coherent"],
                    ["constitutive", "optimal", "holistic", "principled"]
                ],
                "step": "base"
            }
        },
        "principles": {
            "from": "Matrix E",
            "items": [
                "Test principle 1",
                "Test principle 2"
            ]
        }
    }


@pytest.fixture
def canonical_matrices():
    """Canonical matrices for testing."""
    return {
        "A": get_canonical_matrix("A"),
        "B": get_canonical_matrix("B"), 
        "J": get_canonical_matrix("J")
    }