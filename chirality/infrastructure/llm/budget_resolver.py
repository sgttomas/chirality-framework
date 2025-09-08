"""
Budget-aware resolver wrapper.

Wraps existing resolvers to track usage and enforce budgets.
"""

from typing import Dict, Any, List
from chirality.domain.budgets import BudgetTracker
from chirality.domain.types import RichResult


class BudgetAwareResolver:
    """
    Wrapper that adds budget tracking to any resolver.

    Tracks usage from metadata and enforces budget limits.
    """

    def __init__(self, wrapped_resolver, budget_tracker: BudgetTracker):
        """
        Initialize budget-aware resolver.

        Args:
            wrapped_resolver: Original resolver to wrap
            budget_tracker: Budget tracker instance
        """
        self.wrapped_resolver = wrapped_resolver
        self.budget_tracker = budget_tracker

    def run_stage2_multiply(self, terms: List[str], component_id: str = "C") -> RichResult:
        """Stage 2 multiply with budget tracking."""
        result = self.wrapped_resolver.run_stage2_multiply(terms, component_id)

        # Track usage if metadata available
        if hasattr(result, "metadata") and result.metadata:
            self.budget_tracker.record_usage(
                result.metadata, model=result.metadata.get("model", "gpt-4")
            )

        return result

    def run_stage2_elementwise(self, terms: List[str], component_id: str = "F") -> RichResult:
        """Stage 2 elementwise with budget tracking."""
        result = self.wrapped_resolver.run_stage2_elementwise(terms, component_id)

        # Track usage if metadata available
        if hasattr(result, "metadata") and result.metadata:
            self.budget_tracker.record_usage(
                result.metadata, model=result.metadata.get("model", "gpt-4")
            )

        return result

    def run_stage2_addition(self, parts: List[str], component_id: str = "D") -> str:
        """Stage 2 addition with budget tracking."""
        result = self.wrapped_resolver.run_stage2_addition(parts, component_id)
        # Note: This returns a string, not RichResult, so no metadata to track
        return result

    def run_combined_lens(
        self, content: str, component_id: str, row_label: str, col_label: str
    ) -> RichResult:
        """Combined lensing with budget tracking."""
        result = self.wrapped_resolver.run_combined_lens(
            content, component_id, row_label, col_label
        )

        # Track usage if metadata available
        if hasattr(result, "metadata") and result.metadata:
            self.budget_tracker.record_usage(
                result.metadata, model=result.metadata.get("model", "gpt-4")
            )

        return result

    def run_shift(self, content: str, component_id: str = "Z") -> RichResult:
        """Shift with budget tracking."""
        result = self.wrapped_resolver.run_shift(content, component_id)

        # Track usage if metadata available
        if hasattr(result, "metadata") and result.metadata:
            self.budget_tracker.record_usage(
                result.metadata, model=result.metadata.get("model", "gpt-4")
            )

        return result

    def __getattr__(self, name):
        """Delegate other attributes to wrapped resolver."""
        return getattr(self.wrapped_resolver, name)
