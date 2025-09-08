"""
Phase 1 Dialogue Orchestrator.

Manages a single inclusive conversation from A through E,
building semantic understanding through dialogue history.
Each step returns JSON only (no tables).
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from pathlib import Path

from ...infrastructure.prompts.json_tails import get_tail
from ...infrastructure.llm.openai_adapter import call_responses_api
from ...infrastructure.llm.repair import try_parse_json_or_repair, create_matrix_schema_hint
from ...infrastructure.monitoring.tracer import JSONLTracer
from ...infrastructure.prompts.registry import get_registry
from ...domain.matrices.canonical import get_canonical_matrix
from .aggregator import validate_and_write_agg, create_aggregator_schema_hint


class DialogueOrchestrator:
    """
    Orchestrates the Phase 1 dialogue as a single conversation.

    The dialogue builds semantic understanding progressively,
    with each step adding to the conversation history.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.9,
        max_repair: int = 1,
        token_budget: Optional[int] = None,
        tracer: Optional[JSONLTracer] = None,
    ):
        """
        Initialize the dialogue orchestrator.

        Args:
            model: LLM model identifier
            temperature: Sampling temperature
            max_repair: Maximum repair attempts for invalid JSON
            token_budget: Optional token budget for the entire dialogue
            tracer: Optional JSONL tracer for logging
        """
        self.model = model
        self.temperature = temperature
        self.max_repair = max_repair
        self.token_budget = token_budget
        self.tracer = tracer

        # Track conversation history
        self.dialogue_history = []
        self.token_count = 0

        # Load canonical matrices
        self.A = get_canonical_matrix("A")
        self.B = get_canonical_matrix("B")
        self.J = get_canonical_matrix("J")

    def run_dialogue(self) -> Dict[str, Any]:
        """
        Run the complete Phase 1 dialogue from A through E.

        Returns:
            Dictionary with phase1_output structure
        """
        # Initialize dialogue with system message
        system_message = self._build_system_message()
        self.dialogue_history.append({"role": "system", "content": system_message})

        # Track results for aggregation
        results = {}

        # Matrix C: Problem Statement (A · B)
        results["C"] = self._compute_matrix_c()

        # Matrix J: Base canonical (truncated B)
        results["J"] = self._present_matrix_j()

        # Matrix F: Requirements (C ⊙ J)
        results["F"] = self._compute_matrix_f(results["C"], results["J"])

        # Matrix D: Objectives (A + F)
        results["D"] = self._compute_matrix_d(results["F"])

        # Matrix K: Transpose of D
        results["K"] = self._compute_matrix_k(results["D"])

        # Matrix X: Verification (K · J)
        results["X"] = self._compute_matrix_x(results["K"], results["J"])

        # Matrix Z: Validation (shift from X)
        results["Z"], principles = self._compute_matrix_z(results["X"])

        # Matrix G: First 3 rows of Z
        results["G"] = self._extract_matrix_g(results["Z"])

        # Array P: Fourth row of Z
        results["P"] = self._extract_array_p(results["Z"])

        # Matrix T: Transpose of J
        results["T"] = self._compute_matrix_t(results["J"])

        # Matrix E: Evaluation (G · T)
        results["E"] = self._compute_matrix_e(results["G"], results["T"])

        # Final aggregation
        final_output = self._aggregate_results(results, principles)

        return final_output

    def _build_system_message(self) -> str:
        """Build the system message with normative context."""
        # This would load from prompt_assets/system.md
        # For now, returning placeholder
        return "You are implementing the Chirality Framework Phase 1 through semantic operations."

    def _call_llm_with_json_tail(
        self, user_message: str, json_tail: str, operation: str
    ) -> Dict[str, Any]:
        """
        Call LLM with JSON tail enforcement.

        Args:
            user_message: The user message content
            json_tail: The JSON tail to append
            operation: Operation name for tracing

        Returns:
            Parsed JSON response
        """
        # Append JSON tail to user message
        full_message = f"{user_message}\n\n{json_tail}"

        # Add to dialogue history
        self.dialogue_history.append({"role": "user", "content": full_message})

        # Check token budget
        if self.token_budget and self.token_count > self.token_budget:
            raise ValueError(f"Token budget exceeded: {self.token_count} > {self.token_budget}")

        # Parse JSON response with repair if needed
        def adapter_call(messages):
            return call_responses_api(
                messages=messages, temperature=self.temperature, json_only=True
            )

        # Create schema hint for repair
        matrix_name = operation.split("_")[0] if "_" in operation else "unknown"
        step = operation.split("_")[1] if "_" in operation else "unknown"
        schema_hint = create_matrix_schema_hint(matrix_name, step)

        parsed, metadata = try_parse_json_or_repair(
            messages=self.dialogue_history,
            adapter_call=adapter_call,
            schema_hint=schema_hint,
            max_repair_attempts=self.max_repair,
        )

        # Update token count
        self.token_count += metadata.get("total_tokens", 0)

        # Note: dialogue history is already updated by the repair function

        # Trace if configured
        if self.tracer:
            self.tracer.trace_stage(
                stage=operation,
                context={"operation": operation, "matrix": parsed.get("name")},
                result=parsed,
                metadata=metadata,
            )

        return parsed

    def _compute_matrix_c(self) -> Dict[str, Any]:
        """Compute Matrix C through dialogue."""
        # Step 1: Mechanical dot product
        user_msg = f"""
Compute the dot product C = A · B mechanically.

Matrix A (3x4):
{self._format_matrix(self.A)}

Matrix B (4x4):
{self._format_matrix(self.B)}

For each position C[i,j], list the k-products A[i,k] * B[k,j] for k=0..3.
"""
        mechanical = self._call_llm_with_json_tail(
            user_msg, get_tail("C", "mechanical"), "C_mechanical"
        )

        # Step 2: Semantic interpretation
        user_msg = "Now interpret each k-product semantically using semantic multiplication."
        interpreted = self._call_llm_with_json_tail(
            user_msg, get_tail("C", "interpreted"), "C_interpreted"
        )

        # Step 3: Generate lenses
        user_msg = "Generate lenses for each cell using row × column × station perspective."
        lenses = self._call_llm_with_json_tail(user_msg, get_tail("C", "lenses"), "C_lenses")

        # Step 4: Apply lenses
        user_msg = "Apply the lenses to produce the final lensed matrix C."
        lensed = self._call_llm_with_json_tail(user_msg, get_tail("C", "lensed"), "C_lensed")

        return lensed

    def _present_matrix_j(self) -> Dict[str, Any]:
        """Present canonical Matrix J."""
        user_msg = f"""
Matrix J is the truncated version of B (first 3 rows):

{self._format_matrix(self.J)}

This represents the epistemic levels without Wisdom.
"""
        return self._call_llm_with_json_tail(user_msg, get_tail("J", "base"), "J_base")

    def _compute_matrix_f(self, C: Dict, J: Dict) -> Dict[str, Any]:
        """Compute Matrix F = C ⊙ J (element-wise)."""
        # Similar pattern: mechanical, interpreted, lenses, lensed
        user_msg = "Compute F = C ⊙ J using element-wise multiplication."

        # Mechanical
        mechanical = self._call_llm_with_json_tail(
            user_msg, get_tail("F", "mechanical"), "F_mechanical"
        )

        # Continue with interpreted, lenses, lensed...
        # (Following same pattern as C)

        return mechanical  # Placeholder for now

    def _compute_matrix_d(self, F: Dict) -> Dict[str, Any]:
        """Compute Matrix D using canonical addition formula."""
        user_msg = """
Compute D using the canonical formula:
D[i,j] = A[i,j] + " applied to frame the problem; " + F[i,j] + " to resolve the problem."
"""

        # Constructed (mechanical addition)
        constructed = self._call_llm_with_json_tail(
            user_msg, get_tail("D", "constructed"), "D_constructed"
        )

        # Lensed
        user_msg = "Apply lenses to matrix D for the Objectives station."
        lensed = self._call_llm_with_json_tail(user_msg, get_tail("D", "lensed"), "D_lensed")

        return lensed

    def _compute_matrix_k(self, D: Dict) -> Dict[str, Any]:
        """Compute Matrix K as transpose of D."""
        user_msg = "Compute K as the transpose of matrix D."
        return self._call_llm_with_json_tail(user_msg, get_tail("K", "transpose"), "K_transpose")

    def _compute_matrix_x(self, K: Dict, J: Dict) -> Dict[str, Any]:
        """Compute Matrix X = K · J."""
        # Similar to C computation pattern
        user_msg = "Compute X = K · J for Verification."

        # Would follow mechanical, interpreted, lenses, lensed pattern
        mechanical = self._call_llm_with_json_tail(
            user_msg, get_tail("X", "mechanical"), "X_mechanical"
        )

        return mechanical  # Placeholder

    def _compute_matrix_z(self, X: Dict) -> tuple[Dict[str, Any], List[str]]:
        """Compute Matrix Z through station shift and extract principles."""
        user_msg = "Apply station shift from Verification to Validation for matrix Z."
        shifted = self._call_llm_with_json_tail(user_msg, get_tail("Z", "shifted"), "Z_shifted")

        # Extract principles
        user_msg = "Extract validation principles from matrix Z."
        principles_response = self._call_llm_with_json_tail(
            user_msg, get_tail("Z", "principles"), "Z_principles"
        )

        return shifted, principles_response.get("items", [])

    def _extract_matrix_g(self, Z: Dict) -> Dict[str, Any]:
        """Extract Matrix G (first 3 rows of Z)."""
        user_msg = "Extract matrix G as the first 3 rows of matrix Z."
        return self._call_llm_with_json_tail(user_msg, get_tail("G", "base"), "G_base")

    def _extract_array_p(self, Z: Dict) -> Dict[str, Any]:
        """Extract Array P (fourth row of Z)."""
        user_msg = "Extract array P as the fourth row of matrix Z."
        return self._call_llm_with_json_tail(user_msg, get_tail("P", "base"), "P_base")

    def _compute_matrix_t(self, J: Dict) -> Dict[str, Any]:
        """Compute Matrix T as transpose of J."""
        user_msg = "Compute T as the transpose of matrix J."
        return self._call_llm_with_json_tail(user_msg, get_tail("T", "transpose"), "T_transpose")

    def _compute_matrix_e(self, G: Dict, T: Dict) -> Dict[str, Any]:
        """Compute Matrix E = G · T."""
        user_msg = "Compute E = G · T for Evaluation."

        # Would follow mechanical, interpreted, lenses, lensed pattern
        mechanical = self._call_llm_with_json_tail(
            user_msg, get_tail("E", "mechanical"), "E_mechanical"
        )

        return mechanical  # Placeholder

    def _aggregate_results(self, results: Dict[str, Dict], principles: List[str]) -> Dict[str, Any]:
        """Aggregate all results into final output format with validation."""
        # Request final aggregation with repair-capable parsing
        user_msg = "Aggregate all matrices into the final Phase 1 output."

        def adapter_call(messages):
            return call_responses_api(
                messages=messages, temperature=self.temperature, json_only=True
            )

        # Use aggregator schema hint for repair
        schema_hint = create_aggregator_schema_hint()

        aggregated, metadata = try_parse_json_or_repair(
            messages=self.dialogue_history
            + [{"role": "user", "content": f"{user_msg}\n\n{get_tail('aggregator', '')}"}],
            adapter_call=adapter_call,
            schema_hint=schema_hint,
            max_repair_attempts=self.max_repair,
        )

        # Add/update metadata
        aggregated["meta"] = {
            "kernel_hash": self._compute_kernel_hash(),
            "snapshot_hash": "",  # Will be computed after snapshot generation
            "model": self.model,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "token_count": self.token_count,
        }

        return aggregated

    def _compute_kernel_hash(self) -> str:
        """Compute kernel hash from prompt assets."""
        registry = get_registry()
        return registry.compute_kernel_hash()

    def _format_matrix(self, matrix) -> str:
        """Format a matrix for display in prompts."""
        lines = []
        for i, row in enumerate(matrix.cells):
            row_values = [cell.value for cell in row]
            lines.append(f"Row {i} ({matrix.row_labels[i]}): {row_values}")
        return "\n".join(lines)

    def save_dialogue(self, output_path: Path):
        """Save dialogue history to JSONL file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            for message in self.dialogue_history:
                f.write(json.dumps(message) + "\n")

    def save_output(self, final_output: Dict[str, Any], output_dir: Path):
        """Save and validate final Phase 1 output."""
        return validate_and_write_agg(final_output, str(output_dir))
