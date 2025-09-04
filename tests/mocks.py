"""
Mock implementations for testing the Chirality Framework semantic calculator.

Provides deterministic, predictable resolvers that don't require LLM calls,
enabling fast, offline testing of the 3-stage pipeline.
"""

from typing import Dict, Any
from chirality.core.context import SemanticContext
from chirality.core.types import RichResult


class MockCellResolver:
    """
    Deterministic resolver for testing the 3-stage pipeline.
    
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
            "resolve_semantic_pair": 0,
            "apply_column_lens": 0,
            "apply_row_lens": 0,
            "synthesize_lensed_perspectives": 0,
            "shift_station_context": 0
        }
    
    def resolve_semantic_pair(self, pair: str, context: SemanticContext) -> RichResult:
        """
        Mock semantic resolution for Stage 2.
        
        Returns predictable concept based on input pair.
        """
        self.call_count["resolve_semantic_pair"] += 1
        
        # Deterministic patterns for common test cases
        patterns = {
            "Values * Necessary": "Essential Values",
            "Actions * Contingent": "Conditional Actions",
            "Benchmarks * Fundamental": "Foundational Benchmarks",
            "Feedback * Best Practices": "Optimal Reference Points",
            "Processes * Necessary": "Required Processes",
            "Insights * Necessary": "Critical Insights",
            "Comparisons * Necessary": "Essential Comparisons",
            "Learning * Necessary": "Fundamental Learning",
            # Pattern matching for unknown pairs
        }
        
        # Check for exact match
        if pair in patterns:
            text = patterns[pair]
            terms = [pair]
        elif " * " in pair:
            left, right = pair.split(" * ", 1)
            terms = [left, right]
            if self.pattern_style == "minimal":
                text = f"{left[:3]}{right[:3]}"
            elif self.pattern_style == "mechanical":
                text = f"[{left}×{right}]"
            else:  # descriptive
                text = f"{right} {left}"
        else:
            text = f"Resolved({pair})"
            terms = [pair]
        
        return RichResult(
            text=text,
            terms_used=terms,
            warnings=[],
            metadata={"modelId": "mock_resolver"}
        )
    
    def apply_column_lens(self, content: str, context: SemanticContext) -> RichResult:
        """
        Mock column lens - Step 1 of universal lensing.
        """
        self.call_count["apply_column_lens"] += 1
        return RichResult(
            text=f"COL[{context.col_label}]: {content}",
            terms_used=[content],
            warnings=[],
            metadata={"modelId": "mock_resolver"}
        )
    
    def apply_row_lens(self, content: str, context: SemanticContext) -> RichResult:
        """
        Mock row lens - Step 2 of universal lensing.
        """
        self.call_count["apply_row_lens"] += 1
        return RichResult(
            text=f"ROW[{context.row_label}]: {content}",
            terms_used=[content],
            warnings=[],
            metadata={"modelId": "mock_resolver"}
        )
    
    def synthesize_lensed_perspectives(self, column_perspective: str, row_perspective: str, context: SemanticContext) -> RichResult:
        """
        Mock final synthesis - Step 3 of universal lensing.
        """
        self.call_count["synthesize_lensed_perspectives"] += 1
        return RichResult(
            text=f"SYN[{column_perspective} | {row_perspective}]",
            terms_used=[column_perspective, row_perspective],
            warnings=[],
            metadata={"modelId": "mock_resolver"}
        )
    
    def shift_station_context(self, content: str, context: SemanticContext) -> RichResult:
        """
        Mock station shift for testing Station 5 validation.
        
        Following colleague_1's guidance for clear Validation-oriented output with coordinates.
        """
        self.call_count["shift_station_context"] += 1
        return RichResult(
            text=f"VALIDATION[{context.row_label},{context.col_label}]: {content}",
            terms_used=[content],
            warnings=[],
            metadata={"modelId": "mock_resolver"}
        )
    
    def reset_call_counts(self):
        """Reset call counters for fresh test."""
        self.call_count = {
            "resolve_semantic_pair": 0,
            "apply_column_lens": 0,
            "apply_row_lens": 0,
            "synthesize_lensed_perspectives": 0,
            "shift_station_context": 0
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
    
    def trace_stage(self, stage_type: str, context: Any, result: Any, extras: Dict[str, Any] = None):
        """
        Capture trace event in memory.
        
        Args:
            stage_type: Type of stage being traced
            context: SemanticContext or similar
            result: Result dictionary with text, terms_used, warnings
            extras: Additional metadata
        """
        event = {
            "stage": stage_type,
            "context": context,
            "result": result,
            "extras": extras or {}
        }
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
        Verify that a complete 3-stage pipeline was traced.
        
        Returns:
            True if combinatorial, semantic, and lensing stages all present
        """
        expected_stages = {"combinatorial", "product:k=", "lensing:"}
        for stage in expected_stages:
            if not any(stage in s for s in self.stages_traced):
                return False
        return True


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
                cell = type('Cell', (), {
                    'row': i,
                    'col': j, 
                    'value': f"{name}[{i},{j}]"
                })()
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
        ["Insights", "Operations", "Metrics", "Learning"]
    ]
    
    test_values_B = [
        ["Necessary", "Sufficient", "Complete", "Optimal"],
        ["Contingent", "Dependent", "Conditional", "Variable"],
        ["Fundamental", "Essential", "Critical", "Core"],
        ["Best Practices", "Guidelines", "Principles", "Methods"]
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