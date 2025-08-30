"""
Clean resolvers for Chirality Framework v15.0.1 semantic calculator.

Contains only the essential EchoResolver for testing purposes.
All production semantic resolution goes through the CellResolver.
"""

from .context import SemanticContext


class EchoResolver:
    """
    Deterministic, zero-LLM resolver for testing.
    
    Returns predictable outputs that match the CellResolver interface.
    Perfect for testing the 3-stage pipeline without LLM calls.
    """
    
    def resolve_semantic_pair(self, pair: str, context: SemanticContext) -> str:
        """
        Mock semantic multiplication - reverses the order of terms.
        
        Args:
            pair: String like "term1 * term2"
            context: Full semantic context (ignored in mock)
            
        Returns:
            Reversed terms as mock resolution
        """
        if " * " in pair:
            left, right = pair.split(" * ", 1)
            return f"{right} {left}"
        return f"Resolved({pair})"
    
    def apply_ontological_lens(self, content: str, context: SemanticContext) -> str:
        """
        Mock ontological lensing - adds context labels.
        
        Args:
            content: Content to interpret
            context: Full semantic context with row/col labels
            
        Returns:
            Content with mock contextual interpretation
        """
        return f"Through {context.row_label} lens via {context.col_label}: {content}"