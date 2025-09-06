"""
Mock implementations for testing the Chirality Framework with new prompt system architecture.

Provides deterministic, predictable resolvers that don't require LLM calls,
enabling fast, offline testing of the new combined lensing pipeline.
"""

from typing import Dict, Any, List
from chirality.core.types import RichResult


class MockCellResolver:
    """
    Deterministic resolver for testing the new prompt system architecture.

    Returns predictable outputs based on input patterns, allowing us to
    test the pipeline mechanics without OpenAI API calls.
    """

    def __init__(self, pattern_style: str = "descriptive"):
        """
        Initialize mock resolver.

        Args:
            pattern_style: Style of mock responses
                - "descriptive": Human-readable descriptions
                - "mechanical": Technical/mechanical style
                - "minimal": Shortest possible valid responses
        """
        self.pattern_style = pattern_style
        self.call_count = {
            "run_stage2_multiply": 0,
            "run_stage2_elementwise": 0,
            "run_stage2_addition": 0,
            "run_combined_lens": 0,
            "run_shift": 0,
        }

    def run_stage2_multiply(self, terms: List[str], component_id: str = "C") -> RichResult:
        """
        Mock Stage 2 semantic multiplication.

        Returns predictable concept based on input terms.
        """
        self.call_count["run_stage2_multiply"] += 1

        # Deterministic patterns for common test cases
        if len(terms) >= 2:
            left, right = terms[0], terms[1]

            # Specific patterns for known test cases
            patterns = {
                ("Values", "Necessary"): "Essential Values",
                ("Actions", "Contingent"): "Conditional Actions",
                ("Benchmarks", "Fundamental"): "Foundational Benchmarks",
                ("Feedback", "Best Practices"): "Optimal Reference Points",
                ("Processes", "Necessary"): "Required Processes",
                ("Insights", "Necessary"): "Critical Insights",
                ("Comparisons", "Necessary"): "Essential Comparisons",
                ("Learning", "Necessary"): "Fundamental Learning",
            }

            key = (left, right)
            if key in patterns:
                text = patterns[key]
            elif self.pattern_style == "minimal":
                text = f"{left[:3]}{right[:3]}"
            elif self.pattern_style == "mechanical":
                text = f"[{left}×{right}]"
            else:  # descriptive
                text = f"{right} {left}"

            used_terms = [left, right]
        else:
            text = f"MULTIPLY({', '.join(terms)})"
            used_terms = terms

        return RichResult(
            text=text,
            terms_used=used_terms,
            warnings=[],
            metadata={
                "resolver": "mock",
                "operation": "stage2_multiply",
                "component": component_id,
            },
        )

    def run_stage2_elementwise(self, terms: List[str], component_id: str = "F") -> RichResult:
        """
        Mock Stage 2 element-wise multiplication.
        """
        self.call_count["run_stage2_elementwise"] += 1

        if len(terms) >= 2:
            text = f"{terms[0]} ⊙ {terms[1]}"
            used_terms = terms[:2]
        else:
            text = f"ELEMENTWISE({', '.join(terms)})"
            used_terms = terms

        return RichResult(
            text=text,
            terms_used=used_terms,
            warnings=[],
            metadata={
                "resolver": "mock",
                "operation": "stage2_elementwise",
                "component": component_id,
            },
        )

    def run_stage2_addition(self, parts: List[str], component_id: str = "D") -> str:
        """
        Mock Stage 2 mechanical addition (Matrix D).

        This is mechanical string construction, no LLM call.
        """
        self.call_count["run_stage2_addition"] += 1

        if len(parts) == 2:
            return f"{parts[0]} applied to frame the problem; {parts[1]} to resolve the problem."
        else:
            return f"ADDITION({' + '.join(parts)})"

    def run_combined_lens(
        self, content: str, component_id: str, row_label: str, col_label: str
    ) -> RichResult:
        """
        Mock combined ontological lensing (row × col × station).

        This replaces the old three-step lensing process.
        """
        self.call_count["run_combined_lens"] += 1

        # Map components to stations for mock output
        station_map = {
            "C": "Requirements",
            "D": "Objectives",
            "F": "Objectives",
            "X": "Verification",
            "Z": "Validation",
            "E": "Evaluation",
        }

        station = station_map.get(component_id, "Unknown")

        # Generate mock combined lensing output based on style
        if self.pattern_style == "minimal":
            text = f"[{station[:3]}] {content}"
        elif self.pattern_style == "mechanical":
            text = f"{station}:{row_label}×{col_label}:{content}"
        else:  # descriptive
            text = f"[{station}] {row_label} × {col_label}: {content}"

        return RichResult(
            text=text,
            terms_used=[content],
            warnings=[],
            metadata={
                "resolver": "mock",
                "operation": "combined_lens",
                "component": component_id,
                "station": station,
                "row_label": row_label,
                "col_label": col_label,
            },
        )

    def run_shift(self, content: str, component_id: str = "Z") -> RichResult:
        """
        Mock station context shift (Verification → Validation).
        """
        self.call_count["run_shift"] += 1

        if component_id != "Z":
            raise ValueError(f"Shift operation only valid for component Z, got {component_id}")

        # Mock shift from verification to validation context
        text = f"VALIDATION_SHIFT: {content}"

        return RichResult(
            text=text,
            terms_used=[content],
            warnings=[],
            metadata={"resolver": "mock", "operation": "shift", "component": component_id},
        )

    def reset_call_counts(self):
        """Reset call counters for fresh test."""
        self.call_count = {
            "run_stage2_multiply": 0,
            "run_stage2_elementwise": 0,
            "run_stage2_addition": 0,
            "run_combined_lens": 0,
            "run_shift": 0,
        }

    def get_call_counts(self) -> Dict[str, int]:
        """Get current call counts for assertions."""
        return self.call_count.copy()


class MockTracer:
    """
    Mock tracer for testing without file I/O.

    Captures trace events in memory for verification.
    """

    def __init__(self):
        self.events = []
        self.stages_traced = set()

    def trace_stage(
        self, stage_type: str, context: Any, result: Any, extras: Dict[str, Any] = None
    ):
        """
        Capture trace event in memory.

        Args:
            stage_type: Type of stage being traced
            context: SemanticContext or similar
            result: Result dictionary with text, terms_used, warnings
            extras: Additional metadata
        """
        event = {"stage": stage_type, "context": context, "result": result, "extras": extras or {}}
        self.events.append(event)
        self.stages_traced.add(stage_type)

    def get_events(self):
        """Get all traced events."""
        return self.events

    def get_stages_traced(self):
        """Get unique stages that were traced."""
        return self.stages_traced

    def reset(self):
        """Clear all captured events."""
        self.events = []
        self.stages_traced = set()

    def find_events_by_stage(self, stage_pattern: str):
        """Find all events matching a stage pattern."""
        return [e for e in self.events if stage_pattern in e["stage"]]

    def verify_complete_pipeline(self) -> bool:
        """
        Verify that a complete pipeline was traced.

        Returns:
            True if required stages were traced
        """
        # For new architecture: Check if any computation completed
        # The tracer now captures high-level completion events
        completion_patterns = [
            "compute_C_complete",
            "compute_F_complete",
            "compute_D_complete",
            "compute_X_complete",
            "compute_E_complete",
            "compute_Z_complete",
        ]
        return any(pattern in self.stages_traced for pattern in completion_patterns)


class MockMatrix:
    """
    Simple mock matrix for testing without loading full canonical matrices.
    """

    def __init__(self, name: str, rows: int = 3, cols: int = 4):
        self.name = name
        self.shape = (rows, cols)
        self.row_labels = [f"Row{i}" for i in range(rows)]
        self.col_labels = [f"Col{j}" for j in range(cols)]
        self.cells = []

        # Generate simple test cells
        for i in range(rows):
            row_cells = []
            for j in range(cols):
                cell = type("Cell", (), {"row": i, "col": j, "value": f"{name}[{i},{j}]"})()
                row_cells.append(cell)
            self.cells.append(row_cells)

    def get_cell(self, i: int, j: int):
        """Get cell at position (i, j)."""
        return self.cells[i][j]


def create_test_matrices():
    """
    Create a standard set of test matrices.

    Returns:
        tuple: (A, B) matrices for testing
    """
    A = MockMatrix("A", 3, 4)
    B = MockMatrix("B", 4, 4)

    # Set meaningful test values
    test_values_A = [
        ["Values", "Actions", "Benchmarks", "Feedback"],
        ["Processes", "Decisions", "Standards", "Outcomes"],
        ["Insights", "Operations", "Metrics", "Learning"],
    ]

    test_values_B = [
        ["Necessary", "Sufficient", "Complete", "Optimal"],
        ["Contingent", "Dependent", "Conditional", "Variable"],
        ["Fundamental", "Essential", "Critical", "Core"],
        ["Best Practices", "Guidelines", "Principles", "Methods"],
    ]

    # Apply test values
    for i in range(3):
        for j in range(4):
            A.cells[i][j].value = test_values_A[i][j]

    for i in range(4):
        for j in range(4):
            B.cells[i][j].value = test_values_B[i][j]

    # Set ontological labels
    A.row_labels = ["Normative", "Operative", "Evaluative"]
    A.col_labels = ["Guiding", "Applying", "Judging", "Reflecting"]

    B.row_labels = ["Determinacy", "Sufficiency", "Necessity", "Contingency"]
    B.col_labels = ["Possibility", "Challenge", "Comparison", "Paradigm"]

    return A, B
