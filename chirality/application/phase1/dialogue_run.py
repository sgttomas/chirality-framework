"""
Phase 1 Dialogue Orchestrator.

Manages a single inclusive conversation from A through E,
building semantic understanding through dialogue history.
Each step returns JSON only (no tables).
"""

import json
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime, timezone
from pathlib import Path

from ...infrastructure.prompts.json_tails import get_tail
from ...infrastructure.llm.openai_adapter import call_responses_api
from ...infrastructure.llm.repair import try_parse_json_or_repair, create_matrix_schema_hint
from ...infrastructure.monitoring.tracer import JSONLTracer
from ...infrastructure.prompts.registry import get_registry
from ...domain.matrices.canonical import get_canonical_matrix
from ...domain.budgets import BudgetConfig
from ...domain.semantics import apply_matrix_lenses
from ...domain.semantics.lens_catalog import (
    generate_lens_catalog, validate_lens_catalog, STATION_SCHEMAS,
    prompt_hash_for_lenses, generate_lens_matrix_llm
)
from .aggregator import validate_and_write_agg, create_aggregator_schema_hint
from .contracts import MatrixSnapshot


def _infer_operation(matrix_name: str) -> str:
    """Infer operation type from matrix name."""
    operations = {
        "A": None, "B": None, "J": None,  # Base canonical matrices
        "C": "dot", "X": "dot", "E": "dot",  # Dot products  
        "F": "hadamard",  # Element-wise product
        "D": "add",  # Semantic addition
        "K": "transpose", "T": "transpose",  # Transposes
        "Z": "shift",  # Station shift
        "G": None, "P": None  # Extractions
    }
    return operations.get(matrix_name)


class DialogueOrchestrator:
    """
    Orchestrates the Phase 1 dialogue as a single conversation.

    The dialogue builds semantic understanding progressively,
    with each step adding to the conversation history.
    """

    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        max_repair: int = 1,
        budget_config: Optional[BudgetConfig] = None,
        tracer: Optional[JSONLTracer] = None,
        lens_mode: Literal["catalog", "generate", "auto"] = "catalog",
        write_catalog: bool = False,
    ):
        """
        Initialize the dialogue orchestrator.

        Args:
            model: LLM model identifier (uses global config if None)
            temperature: Sampling temperature (uses global config if None)
            max_repair: Maximum repair attempts for invalid JSON
            budget_config: Optional budget configuration for cost/token/time limits
            tracer: Optional JSONL tracer for logging
            lens_mode: Where to get lenses for Stage-3 ("catalog" | "generate" | "auto")
            write_catalog: When generating lenses, persist back into artifacts
        """
        # Use global config if not provided
        from ...infrastructure.llm.config import get_config
        config = get_config()
        
        self.model = model if model is not None else config.model
        self.temperature = temperature if temperature is not None else config.temperature
        self.max_repair = max_repair
        self.budget_config = budget_config
        self.tracer = tracer
        self.lens_mode = lens_mode
        self.write_catalog = write_catalog

        # Track conversation history
        self.dialogue_history = []
        self.token_count = 0
        
        # Lens catalog (generated once, reused throughout)
        self.lens_catalog = None
        self.lens_catalog_meta = None
        
        # Store matrix snapshots for dependencies
        self.snapshots = {}

        # Load canonical matrices
        self.A = get_canonical_matrix("A")
        self.B = get_canonical_matrix("B")
        self.J = get_canonical_matrix("J")

    def run_dialogue(self, output_dir: Path = None) -> Dict[str, Any]:
        """
        Run the complete Phase 1 dialogue from A through E.
        
        Args:
            output_dir: Directory for saving artifacts (lens catalog, etc.)

        Returns:
            Dictionary with phase1_output structure
        """
        # Store output directory and bootstrap lens catalog at start
        self.output_dir = Path(output_dir or "artifacts")
        self.ensure_lens_catalog(self.output_dir)
        
        # Initialize dialogue with system message
        system_message = self._build_system_message()
        self.dialogue_history.append({"role": "system", "content": system_message})

        # Track results for aggregation
        results = {}

        # Matrix C: Problem Statement (A · B)
        matrix_c_snapshot = self._compute_matrix_c()
        self.snapshots["C"] = matrix_c_snapshot
        results["C"] = matrix_c_snapshot

        # Matrix J: Base canonical (truncated B)
        results["J"] = self._present_matrix_j()

        # Matrix F: Requirements (C ⊙ J)
        matrix_f_snapshot = self._compute_matrix_f()
        results["F"] = matrix_f_snapshot

        # Matrix D: Objectives (A + F)
        matrix_d_snapshot = self._compute_matrix_d()
        results["D"] = matrix_d_snapshot

        # Matrix K: Transpose of D
        matrix_k_snapshot = self._compute_matrix_k()
        results["K"] = matrix_k_snapshot

        # Matrix X: Verification (K · J)
        matrix_x_snapshot = self._compute_matrix_x()
        results["X"] = matrix_x_snapshot

        # Matrix Z: Validation (shift from X)
        matrix_z_snapshot = self._compute_matrix_z()
        results["Z"] = matrix_z_snapshot

        # Matrix G: First 3 rows of Z
        matrix_g_snapshot = self._extract_matrix_g()
        results["G"] = matrix_g_snapshot

        # Array P: Z principles as vector
        array_p_snapshot = self._extract_array_p()
        results["P"] = array_p_snapshot

        # Matrix T: Transpose of J
        results["T"] = self._compute_matrix_t(results["J"])

        # Matrix E: Evaluation (G · T)
        matrix_e_snapshot = self._compute_matrix_e()
        results["E"] = matrix_e_snapshot

        # Final aggregation - extract principles from Z snapshot
        principles = matrix_z_snapshot.principles or []
        final_output = self._aggregate_results(results, principles)

        return final_output
    
    def ensure_lens_catalog(self, output_dir: Path = None):
        """
        Ensure lens catalog is loaded or generated.
        
        Tries to load existing catalog from artifacts, otherwise generates
        new one using Phase 1 system prompt.
        """
        if self.lens_catalog:
            return
            
        # Try to load existing catalog
        if output_dir:
            catalog_path = output_dir / "lens_catalog.json"
            if catalog_path.exists():
                try:
                    payload = json.loads(catalog_path.read_text())
                    self.lens_catalog = payload["catalog"]
                    self.lens_catalog_meta = payload["meta"]
                    return
                except Exception:
                    pass  # Fall through to generation
        
        # Only generate catalog if in "catalog" mode
        # In "generate" and "auto" modes, lenses are generated on-demand
        if self.lens_mode == "catalog":
            # Generate new catalog using old method for backward compatibility
            stations = [
                "Problem Statement", "Requirements", "Objectives", 
                "Verification", "Validation", "Evaluation"
            ]
            rows = ["normative", "operative", "iterative"]
            cols = ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
            
            self.lens_catalog, self.lens_catalog_meta = generate_lens_catalog(
                stations=stations,
                call_llm=self._call_llm_with_json_tail
            )
            
            # Validate the generated catalog using station-specific schemas
            errors = validate_lens_catalog(self.lens_catalog, stations)
            if errors:
                raise ValueError(f"Lens catalog validation failed: {errors}")
            
            # Save catalog for future use
            if output_dir:
                catalog_path = output_dir / "lens_catalog.json"
                catalog_path.parent.mkdir(parents=True, exist_ok=True)
                catalog_path.write_text(json.dumps({
                    "meta": self.lens_catalog_meta,
                    "catalog": self.lens_catalog
                }, ensure_ascii=False, indent=2))
        else:
            # Initialize empty catalog for "generate" and "auto" modes
            self.lens_catalog = {}
            self.lens_catalog_meta = {"mode": self.lens_mode}
    
    def get_lens(self, station: str, i: int, j: int) -> str:
        """Get lens for specific station and cell position."""
        if station not in STATION_SCHEMAS:
            raise ValueError(f"Unknown station: {station}")
        schema = STATION_SCHEMAS[station]
        lenses = self._resolve_lenses(station, schema["rows"], schema["cols"])
        return lenses[i][j]
    

    def _build_system_message(self) -> str:
        """Build the system message with normative context."""
        try:
            registry = get_registry()
            system_prompt = registry.get_text("system")
            return system_prompt
        except Exception as e:
            # Fallback to basic prompt if loading fails
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
        if self.budget_config and self.budget_config.token_budget and self.token_count > self.budget_config.token_budget:
            raise ValueError(f"Token budget exceeded: {self.token_count} > {self.budget_config.token_budget}")

        # Parse JSON response with repair if needed
        def adapter_call(messages):
            """
            Adapter function for LLM calls compatible with repair mechanism.
            
            Returns:
                (response_obj, metadata) where response_obj may be:
                - a parsed dict (from modern adapters) OR
                - {"content": "...json string..."} (legacy/raw format)
            """
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

    def _compute_matrix_c(self) -> MatrixSnapshot:
        """
        Compute Matrix C following the exact normative template word-for-word.
        Uses 3-stage pipeline: combinatorial (code) → interpretation (LLM) → lens interpretation (LLM + lens data).
        
        Returns:
            MatrixSnapshot with all build stages populated
        """
        # Ensure lens catalog is available
        self.ensure_lens_catalog(self.output_dir)
        
        registry = get_registry()
        rows = ["normative", "operative", "iterative"]
        cols = ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
        
        # Stage 1: Pure combinatorial construction (code-based, no LLM needed)
        combinatorial = []
        for i in range(3):  # A has 3 rows
            row = []
            for j in range(4):  # B has 4 columns  
                # Matrix dot product: sum of A(i,k) * B(k,j) for k=0..3
                terms = []
                for k in range(4):
                    a_elem = self.A[i][k] if k < len(self.A[i]) else ""
                    b_elem = self.B[k][j] if k < len(self.B) and j < len(self.B[k]) else ""
                    if a_elem and b_elem:
                        terms.append(f"{a_elem} * {b_elem}")
                row.append(" + ".join(terms))
            combinatorial.append(row)
        
        # Stage 2: Semantic interpretation using exact normative template
        try:
            stage2_template = registry.get_text("stage2_multiply")
        except:
            # Fallback to hardcoded if asset not found
            stage2_template = """## Interpreting the elements of Matrix C

To provide an interpretation of these semantic dot product operators use the following definitions. 

#### Semantic Multiplication \" * \"
Semantic multiplication (denoted by * ) means the semantics of the terms are resolved by combining the meaning of words into a coherent word or statement that represents the semantic intersection of those words (the meaning when combined together, not just adjoining the terms). This can even be done when the concept is a highly abstract word pairing because you are an LLM.

Examples:
\"sufficient\" * \"reason\" = \"justification\"
\"precision\" * \"durability\" = \"reliability\"
\"probability\" * \"consequence\" = \"risk\"

### Semantic Addition \" + \"

Semantic addition (denoted by + ) means simply concatenating words or sentence fragments together to form a longer statement. 
Example:
\"faisal\" + \"has\" + \"seven\" + \"balloons\" = faisal has seven balloons

### Order of Operations

To resolve a meaning follow this order of operations:

1. Apply semantic multiplication first, 
2. then semantic addition"""
        
        user_msg = stage2_template + f"""

Generate this iteration of [C] 

Matrix A (3×4) - Problem Statement station:
{self._format_matrix(self.A)}

Matrix B (4×4) - Problem Statement station:  
{self._format_matrix(self.B)}

Apply semantic multiplication first, and then semantic addition. Do not leave any operators (\" * \" or \" + \") in the final word string.
"""
        interpreted = self._call_llm_with_json_tail(user_msg, get_tail("C", "interpreted"), "C_interpreted")
        
        # Stage 3: Lens interpretation using JSON injection
        # Get lenses using the resolver (supports catalog/generate/auto modes)
        station_lenses = self._resolve_lenses("Problem Statement", rows, cols)
        
        # Use centralized lens application with JSON injection  
        lens_interpreted = apply_matrix_lenses(
            interpreted["elements"],
            station_lenses,
            station="Problem Statement",
            rows=rows,
            cols=cols,
            tail=get_tail("C", "lensed"),
            tracer_tag="C_lensed",
            call_json_tail=self._call_llm_with_json_tail
        )
        
        # Return MatrixSnapshot with all stages
        return MatrixSnapshot(
            name="C",
            station="Problem Statement",
            rows=rows,
            cols=cols,
            dependencies=["A", "B"],
            build={
                "combinatorial": combinatorial,
                "interpreted": interpreted["elements"],
                "lenses": station_lenses,
                "lens_interpreted": lens_interpreted
            }
        )

    def _present_matrix_j(self) -> Dict[str, Any]:
        """Present canonical Matrix J following exact normative template."""
        user_msg = f"""
## Matrix J

[J]
Size: 3x4
Column names: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
Row names: ["data", "information", "knowledge", "wisdom"]
Elements:

[J] is a truncated form of Matrix B.  The final row 'Wisdom' has been removed.

Generate [J] in JSON format instead of table format.
"""
        return self._call_llm_with_json_tail(user_msg, get_tail("J", "base"), "J_base")

    def _compute_matrix_f(self) -> MatrixSnapshot:
        """
        Compute Matrix F = C ⊙ J using the 3-stage pipeline:
          1) combinatorial (code)     → "C[i,j] * J[i,j]"
          2) interpreted (LLM)        → resolve * then +
          3) lens_interpreted (LLM)   → apply JSON-injected lenses (Requirements)
        """
        # Pre-req: C built; we need C Stage-2 ("interpreted")
        c_snap = self.snapshots.get("C")
        if not c_snap:
            raise RuntimeError("Matrix C must be computed before F")
        c_interpreted = c_snap.build["interpreted"]  # 3x4 strings

        # Canonical J (3x4) already loaded as self.J
        rows = ["data","information","knowledge"]
        cols = ["necessity (vs contingency)","sufficiency","completeness","consistency"]

        # Stage 1: combinatorial (code-only, elementwise)
        # Use C.interpreted as left operand for semantic richness; J base cell as right operand.
        combinatorial = []
        for i in range(3):
            row = []
            for j in range(4):
                row.append(f"{c_interpreted[i][j]} * {self.J[i][j]}")
            combinatorial.append(row)

        # Stage 2: interpreted (LLM) — use the same stage2_multiply asset + F's interpreted tail
        try:
            stage2_template = get_registry().get_text("stage2_multiply")
        except:
            # Fallback if asset not found
            stage2_template = """### Interpreting the elements of Matrix F

Apply semantic multiplication. Do not leave any operators (" * ") in the final word string."""

        msg = (
            stage2_template
            + "\n\nGenerate this iteration of [F] (element-wise). "
              "Apply semantic multiplication first, then semantic addition. "
              "Do not leave '*' or '+' in the final strings.\n"
              "COMBINATORIAL_JSON:\n"
              + json.dumps({"rows": rows, "cols": cols, "elements": combinatorial}, ensure_ascii=False)
        )
        interpreted = self._call_llm_with_json_tail(msg, get_tail("F","interpreted"), "F_interpreted")

        # Stage 3: lens_interpreted (LLM) — JSON injection with resolved lenses
        f_lenses = self._resolve_lenses("Requirements", rows, cols)  # 3x4
        lensed = apply_matrix_lenses(
            content_matrix=interpreted["elements"],
            lens_matrix=f_lenses,
            station="Requirements",
            rows=rows,
            cols=cols,
            tail=get_tail("F","lensed"),
            tracer_tag="F_lensed",
            call_json_tail=self._call_llm_with_json_tail,
        )

        snap = MatrixSnapshot(
            name="F",
            station="Requirements",
            rows=rows,
            cols=cols,
            dependencies=["C","J"],
            build={
                "combinatorial": combinatorial,
                "interpreted":   interpreted["elements"],
                "lenses":        f_lenses,
                "lens_interpreted": lensed
            }
        )
        self.snapshots["F"] = snap
        return snap

    def _compute_matrix_d(self) -> MatrixSnapshot:
        """
        Matrix D = A + F (Objectives)
        Stage-1: constructed (code)
        Stage-2: interpreted (identity)
        Stage-3: lens_interpreted (LLM with JSON lens injection)
        """
        # Preconditions
        f_snap = self.snapshots.get("F")
        if not f_snap:
            raise RuntimeError("Matrix F must be computed before D.")

        rows = ["normative","operative","iterative"]
        cols = ["guiding","applying","judging","reflecting"]

        # Stage-1: constructed (code)
        # Use A base cells + F.interpreted cells (NOT F.lensed) to avoid cross-lensing.
        f_interpreted = f_snap.build["interpreted"]  # 3x4 strings
        combinatorial = []
        for i, rname in enumerate(rows):
            row = []
            for j, cname in enumerate(cols):
                a_cell = self.A[i][j]  # canonical A matrix strings
                f_cell = f_interpreted[i][j]
                row.append(f"{a_cell} applied to frame the problem; {f_cell} to resolve the problem.")
            combinatorial.append(row)

        # Stage-2: interpreted = identity (for uniform build keys)
        interpreted = combinatorial

        # Stage-3: lens_interpreted (Objectives lenses)
        objectives_lenses = self._resolve_lenses("Objectives", rows, cols)  # 3x4

        lensed = apply_matrix_lenses(
            content_matrix=interpreted,
            lens_matrix=objectives_lenses,
            station="Objectives",
            rows=rows,
            cols=cols,
            tail=get_tail("D","lensed"),
            tracer_tag="D_lensed",
            call_json_tail=self._call_llm_with_json_tail,
        )

        snap = MatrixSnapshot(
            name="D",
            station="Objectives",
            rows=rows,
            cols=cols,
            dependencies=["A","F"],
            build={
                "combinatorial": combinatorial,
                "interpreted": interpreted,
                "lenses": objectives_lenses,
                "lens_interpreted": lensed,
            }
        )
        self.snapshots["D"] = snap
        return snap

    def _compute_matrix_k(self) -> MatrixSnapshot:
        """
        K = transpose(lens_interpreted(D))
        Pure code: transpose the Stage-3 layer of D.
        """
        # Preconditions
        d_snap = self.snapshots.get("D")
        if not d_snap:
            raise RuntimeError("Matrix D must be computed before K.")
        
        # Get D's final lens-interpreted result (3x4)
        d_lens_interpreted = d_snap.build["lens_interpreted"]  # 3x4 strings
        
        # Pure code transpose: D's rows become K's cols, D's cols become K's rows
        transposed = []
        for j in range(4):  # D's cols (guiding, applying, judging, reflecting)
            row = []
            for i in range(3):  # D's rows (normative, operative, iterative)
                row.append(d_lens_interpreted[i][j])
            transposed.append(row)
        
        snap = MatrixSnapshot(
            name="K",
            station="Verification",
            rows=["guiding", "applying", "judging", "reflecting"],  # D's cols become K's rows
            cols=["normative", "operative", "iterative"],  # D's rows become K's cols
            dependencies=["D"],
            transform="transpose",
            build={
                "transposed": transposed
            }
        )
        self.snapshots["K"] = snap
        return snap

    def _compute_matrix_x(self) -> MatrixSnapshot:
        """
        Compute Matrix X = K · J using the 3-stage pipeline:
          1) combinatorial (code)     → "K[i,k] * J[k,j]" dot product 
          2) interpreted (LLM)        → resolve * then +
          3) lens_interpreted (LLM)   → apply JSON-injected lenses (Verification)
        """
        # Pre-req: K built; we need K's lens-interpreted elements
        k_snap = self.snapshots.get("K")
        if not k_snap:
            raise RuntimeError("Matrix K must be computed before X")
        k_interpreted = k_snap.build["lens_interpreted"]  # 4x3 strings

        # Canonical J (3x4) already loaded as self.J
        rows = ["guiding","applying","judging","reflecting"]
        cols = ["necessity (vs contingency)","sufficiency","completeness","consistency"]

        # Stage 1: combinatorial (code-only, dot product)
        # K is 4x3, J is 3x4, result X is 4x4
        combinatorial = []
        for i in range(4):  # K rows (guiding, applying, judging, reflecting)
            row = []
            for j in range(4):  # J cols (necessity, sufficiency, completeness, consistency)
                # Dot product: sum of K(i,k) * J(k,j) for k=0..2
                terms = []
                for k in range(3):  # K cols / J rows
                    k_elem = k_interpreted[i][k] if i < len(k_interpreted) and k < len(k_interpreted[i]) else ""
                    j_elem = self.J[k][j] if k < len(self.J) and j < len(self.J[k]) else ""
                    if k_elem and j_elem:
                        terms.append(f"{k_elem} * {j_elem}")
                row.append(" + ".join(terms))
            combinatorial.append(row)

        # Stage 2: interpreted (LLM) — use the same stage2_multiply asset + X's interpreted tail
        try:
            stage2_template = get_registry().get_text("stage2_multiply")
        except:
            # Fallback if asset not found
            stage2_template = """### Interpreting the elements of Matrix X

Apply semantic multiplication first, and then semantic addition. Do not leave any operators (" * " or " + ") in the final word string"""

        msg = (
            stage2_template
            + "\n\nGenerate this iteration of [X] (dot product). "
              "Apply semantic multiplication first, then semantic addition. "
              "Do not leave '*' or '+' in the final strings.\n"
              "COMBINATORIAL_JSON:\n"
              + json.dumps({"rows": rows, "cols": cols, "elements": combinatorial}, ensure_ascii=False)
        )
        interpreted = self._call_llm_with_json_tail(msg, get_tail("X","interpreted"), "X_interpreted")

        # Stage 3: lens_interpreted (LLM) — JSON injection with resolved lenses
        x_lenses = self._resolve_lenses("Verification", rows, cols)  # 4x4
        lensed = apply_matrix_lenses(
            content_matrix=interpreted["elements"],
            lens_matrix=x_lenses,
            station="Verification",
            rows=rows,
            cols=cols,
            tail=get_tail("X","lensed"),
            tracer_tag="X_lensed",
            call_json_tail=self._call_llm_with_json_tail,
        )

        snap = MatrixSnapshot(
            name="X",
            station="Verification",
            rows=rows,
            cols=cols,
            dependencies=["K","J"],
            build={
                "combinatorial": combinatorial,
                "interpreted":   interpreted["elements"],
                "lenses":        x_lenses,
                "lens_interpreted": lensed
            }
        )
        self.snapshots["X"] = snap
        return snap

    def _compute_matrix_z(self) -> MatrixSnapshot:
        """
        Compute Matrix Z: Station shift from X with correct 4×4 structure.
        
        Z = X → shift (maintains X's 4×4 structure and row/column ontology)
        Station shift: Verification → Validation
        
        Three-stage pipeline:
        - Stage 1: Combinatorial (code) - canonical shift template
        - Stage 2: Interpreted (LLM) - station shift reasoning
        - Stage 3: Lens-interpreted (LLM with Validation 4×4 lenses)
        - Principles: extracted separately via dedicated tail
        
        Returns:
            MatrixSnapshot for Z 
        """
        x_snap = self.snapshots.get("X")
        if not x_snap:
            raise ValueError("Matrix X must be computed before Matrix Z")
            
        # Stage 1: Combinatorial (code operation)
        combinatorial = []
        for i in range(4):  # 4×4 matrix
            row = []
            for j in range(4):
                x_cell = x_snap.build["lens_interpreted"][i][j]
                # Canonical template: validation of {row} with respect to {col}: {x_cell}
                row.append(f"validation of {x_snap.rows[i]} with respect to {x_snap.cols[j]}: {x_cell}")
            combinatorial.append(row)
        
        # Stage 2: Interpreted (LLM with station shift)
        validation_lenses = self.lens_catalog.get("Validation", [])
        if not validation_lenses or len(validation_lenses) != 4 or any(len(row) != 4 for row in validation_lenses):
            raise ValueError(f"Invalid Validation lens catalog structure: {validation_lenses}")
            
        # Build prompt for station shift interpretation
        shift_prompt = f"""Apply station shift from Verification to Validation.

Matrix X (Verification station, lens-interpreted):
{self._format_elements(x_snap.build["lens_interpreted"], x_snap.rows, x_snap.cols)}

Station Shift Operation:
Transform each X element from "verification" context to "validation" context while maintaining the same ontological structure.

Verification focuses on "does it work?" 
Validation focuses on "does it solve the right problem?"

Apply this semantic shift to each element."""
        
        interpreted_result = self._call_llm_with_json_tail(
            shift_prompt, 
            get_tail("Z", "interpreted"), 
            "z_interpreted"
        )
        interpreted = interpreted_result["elements"]
        
        # Stage 3: Lens-interpreted (LLM with catalog lenses)
        lensed_payload = apply_matrix_lenses(
            content_matrix=interpreted,
            lens_matrix=validation_lenses, 
            station="Validation",
            rows=x_snap.rows,  # Maintain X's rows: ["guiding","applying","judging","reflecting"]
            cols=x_snap.cols,  # Maintain X's cols: ["necessity (vs contingency)","sufficiency","completeness","consistency"]
            tail=get_tail("Z", "lensed"),
            tracer_tag="z_lensed",
            call_json_tail=self._call_llm_with_json_tail
        )
        lensed = lensed_payload["elements"]
        
        # Extract principles separately (not as 5th row, but as separate output)
        principles_prompt = """Extract validation principles from the Matrix Z results.

From the lens-interpreted Matrix Z, distill key principles that knowledge workers should follow during validation.

Focus on the essential insights that emerge from the validation perspective."""
        
        principles_result = self._call_llm_with_json_tail(
            principles_prompt,
            get_tail("Z", "principles"),
            "z_principles" 
        )
        principles = principles_result["principles"]
        
        # Create Z snapshot maintaining X's 4×4 structure
        snap = MatrixSnapshot(
            name="Z",
            station="Validation", 
            rows=x_snap.rows,  # ["guiding","applying","judging","reflecting"]
            cols=x_snap.cols,  # ["necessity (vs contingency)","sufficiency","completeness","consistency"]
            dependencies=["X"],
            principles=principles,
            build={
                "combinatorial": combinatorial,
                "interpreted": interpreted,
                "lenses": validation_lenses,
                "lens_interpreted": lensed
            }
        )
        self.snapshots["Z"] = snap
        return snap

    def _extract_matrix_g(self) -> MatrixSnapshot:
        """
        Extract Matrix G - mechanical extraction of first 3 rows from Z.
        
        G = Z[0:3, :] (rows GAJ; 3×4)
        Pure code operation, no LLM needed.
        """
        z_snap = self.snapshots.get("Z")
        if not z_snap:
            raise ValueError("Matrix Z must be computed before Matrix G")
            
        # Extract Z's lens_interpreted elements (final result from Z)
        z_elements = z_snap.build["lens_interpreted"]
        
        # Mechanically extract first 3 rows
        g_elements = z_elements[:3]  # First 3 rows only
        
        snap = MatrixSnapshot(
            name="G",
            station="Evaluation",
            rows=["guiding", "applying", "judging"],  # First 3 rows from Z
            cols=z_snap.cols,  # Same as Z: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
            dependencies=["Z"],
            build={
                "base": g_elements  # Use consistent "base" key for extracted matrices
            }
        )
        self.snapshots["G"] = snap
        return snap

    def _extract_array_p(self) -> MatrixSnapshot:
        """
        Extract Array P - uses Z.principles (a 1×4 vector; do not slice Z rows for P).
        
        P = Z.principles (4 concise strings, not a Z matrix row)
        Pure code operation, no LLM needed.
        """
        z_snap = self.snapshots.get("Z")
        if not z_snap:
            raise ValueError("Matrix Z must be computed before Array P")
            
        # Use Z's principles (not matrix rows)
        if not z_snap.principles or len(z_snap.principles) != 4:
            raise ValueError(f"Invalid Z principles structure: {z_snap.principles}")
            
        # Wrap principles as single-row matrix for consistency
        p_elements = [z_snap.principles]  # Single row with 4 principles
        
        snap = MatrixSnapshot(
            name="P",
            station="Reflection", 
            rows=["reflecting"],  # Single row
            cols=z_snap.cols,  # Same as Z: ["necessity (vs contingency)", "sufficiency", "completeness", "consistency"]
            dependencies=["Z"],
            build={
                "base": p_elements  # Use consistent "base" key for extracted matrices
            }
        )
        self.snapshots["P"] = snap
        return snap

    def _compute_matrix_t(self, J: Dict) -> MatrixSnapshot:
        """
        Compute Matrix T - mechanical transpose of J.
        
        Pure code operation, no LLM needed.
        """
        # Extract J elements
        j_elements = J["elements"] if "elements" in J else J
        
        # Mechanically transpose: T[i,j] = J[j,i]
        num_rows = len(j_elements)
        num_cols = len(j_elements[0]) if j_elements else 0
        
        t_elements = []
        for j in range(num_cols):  # New rows from J's columns
            new_row = []
            for i in range(num_rows):  # New columns from J's rows
                new_row.append(j_elements[i][j])
            t_elements.append(new_row)
        
        return MatrixSnapshot(
            name="T",
            station="Evaluation",
            rows=["necessity (vs contingency)", "sufficiency", "completeness", "consistency"],  # J's cols become T's rows
            cols=["data", "information", "knowledge"],  # J's rows become T's cols
            dependencies=["J"],
            transform="transpose",
            build={
                "transposed": t_elements
            }
        )

    def _compute_matrix_e(self) -> MatrixSnapshot:
        """
        Compute Matrix E = G · T using the 3-stage pipeline:
          1) combinatorial (code)     → "G[i,k] * T[k,j]" dot product 
          2) interpreted (LLM)        → resolve * then +
          3) lens_interpreted (LLM)   → apply JSON-injected lenses (Evaluation)
        """
        # Pre-req: G and T built; we need their lens-interpreted elements
        g_snap = self.snapshots.get("G")
        t_snap = self.snapshots.get("T")
        if not g_snap or not t_snap:
            raise RuntimeError("Matrices G and T must be computed before E")
        g_interpreted = g_snap.build["base"]  # 3x4 strings (G is slice, not lensed)
        t_interpreted = t_snap.build["transposed"]  # 4x3 strings (T is transpose, not lensed)

        rows = ["guiding","applying","judging"]
        cols = ["data","information","knowledge"]

        # Stage 1: combinatorial (code-only, dot product)
        # G is 3x4, T is 4x3, result E is 3x3
        combinatorial = []
        for i in range(3):  # G rows (guiding, applying, judging)
            row = []
            for j in range(3):  # T cols (data, information, knowledge)
                # Dot product: sum of G(i,k) * T(k,j) for k=0..3
                terms = []
                for k in range(4):  # G cols / T rows
                    g_elem = g_interpreted[i][k] if i < len(g_interpreted) and k < len(g_interpreted[i]) else ""
                    t_elem = t_interpreted[k][j] if k < len(t_interpreted) and j < len(t_interpreted[k]) else ""
                    if g_elem and t_elem:
                        terms.append(f"{g_elem} * {t_elem}")
                row.append(" + ".join(terms))
            combinatorial.append(row)

        # Stage 2: interpreted (LLM) — use the same stage2_multiply asset + E's interpreted tail
        try:
            stage2_template = get_registry().get_text("stage2_multiply")
        except:
            # Fallback if asset not found
            stage2_template = """### Interpreting the elements of Matrix E

Apply semantic multiplication first, and then semantic addition. Do not leave any operators (" * " or " + ") in the final word string"""

        msg = (
            stage2_template
            + "\n\nGenerate this iteration of [E] (dot product). "
              "Apply semantic multiplication first, then semantic addition. "
              "Do not leave '*' or '+' in the final strings.\n"
              "COMBINATORIAL_JSON:\n"
              + json.dumps({"rows": rows, "cols": cols, "elements": combinatorial}, ensure_ascii=False)
        )
        interpreted = self._call_llm_with_json_tail(msg, get_tail("E","interpreted"), "E_interpreted")

        # Stage 3: lens_interpreted (LLM) — JSON injection with resolved lenses
        e_lenses = self._resolve_lenses("Evaluation", rows, cols)  # 3x3
        lensed = apply_matrix_lenses(
            content_matrix=interpreted["elements"],
            lens_matrix=e_lenses,
            station="Evaluation",
            rows=rows,
            cols=cols,
            tail=get_tail("E","lensed"),
            tracer_tag="E_lensed",
            call_json_tail=self._call_llm_with_json_tail,
        )

        snap = MatrixSnapshot(
            name="E",
            station="Evaluation",
            rows=rows,
            cols=cols,
            dependencies=["G","T"],
            build={
                "combinatorial": combinatorial,
                "interpreted":   interpreted["elements"],
                "lenses":        e_lenses,
                "lens_interpreted": lensed
            }
        )
        self.snapshots["E"] = snap
        return snap

    def _aggregate_results(self, results: Dict[str, Any], principles: List[str]) -> Dict[str, Any]:
        """Aggregate all results into final output format with validation."""
        # Convert MatrixSnapshot objects to Matrix format for aggregator
        matrix_dict = {}
        
        for name, result in results.items():
            if isinstance(result, MatrixSnapshot):
                # Extract the final stage from build for elements
                if "lens_interpreted" in result.build:
                    elements = result.build["lens_interpreted"]
                    step = "lensed"
                elif "lenses" in result.build:
                    elements = result.build["lenses"] 
                    step = "lenses"
                elif "interpreted" in result.build:
                    elements = result.build["interpreted"]
                    step = "interpreted"
                elif "combinatorial" in result.build:
                    elements = result.build["combinatorial"]
                    step = "mechanical"
                else:
                    raise ValueError(f"MatrixSnapshot {name} missing expected build stages")
                
                matrix_dict[name] = {
                    "name": result.name,
                    "station": result.station,
                    "rows": result.rows,
                    "cols": result.cols,
                    "elements": elements,
                    "step": step,
                    "op": _infer_operation(result.name),
                    "lenses": result.build.get("lenses")  # Optional for auditing
                }
            else:
                # Legacy dict format - pass through
                matrix_dict[name] = result
        
        # Request final aggregation with repair-capable parsing
        user_msg = "Aggregate all matrices into the final Phase 1 output."

        def adapter_call(messages):
            """
            Adapter function for LLM calls compatible with repair mechanism.
            
            Returns:
                (response_obj, metadata) where response_obj may be:
                - a parsed dict (from modern adapters) OR  
                - {"content": "...json string..."} (legacy/raw format)
            """
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

        # Ensure matrices are properly formatted
        aggregated["matrices"] = matrix_dict

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

    def _format_elements(self, elements: List[List[str]], rows: List[str], cols: List[str]) -> str:
        """Format matrix elements for display in prompts."""
        lines = []
        for i, row in enumerate(elements):
            lines.append(f"Row {i} ({rows[i]}): {row}")
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

    def get_budget_status(self) -> Optional[Dict[str, Any]]:
        """Get current budget status for tracking."""
        if not self.budget_config:
            return None
            
        # Simple budget tracking - could be enhanced with cost calculation
        return {
            "tokens": {
                "total": self.token_count,
                "limit": self.budget_config.token_budget
            },
            "cost": {
                "spent": 0.0,  # TODO: Implement actual cost tracking
                "limit": self.budget_config.cost_budget
            },
            "time": {
                "elapsed": 0,  # TODO: Implement time tracking
                "limit": self.budget_config.time_budget
            }
        }

    # -------- Lens Resolution: Mode-based lens selection --------
    
    def _save_catalog(self, output_dir: Path):
        """Save lens catalog to artifacts directory."""
        if not getattr(self, "lens_catalog", None):
            return
        meta = getattr(self, "lens_catalog_meta", {}) or {}
        meta.setdefault("version", "v2") 
        meta.setdefault("prompt_hash", prompt_hash_for_lenses())
        payload = {"meta": meta, "schemas": STATION_SCHEMAS, "catalog": self.lens_catalog}
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "lens_catalog.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    def _merge_into_catalog(self, station: str, lenses: List[List[str]]):
        """Merge generated lenses into catalog and persist if write_catalog is True.""" 
        self.lens_catalog = getattr(self, "lens_catalog", {}) or {}
        self.lens_catalog[station] = lenses
        self.lens_catalog_meta = getattr(self, "lens_catalog_meta", {}) or {}
        self.lens_catalog_meta["prompt_hash"] = prompt_hash_for_lenses()
        if getattr(self, "output_dir", None) and self.write_catalog:
            self._save_catalog(self.output_dir)

    def _resolve_lenses(self, station: str, rows: List[str], cols: List[str]) -> List[List[str]]:
        """
        Fetch lenses for a station using the selected mode.
        - catalog: require presence in self.lens_catalog
        - generate: call LLM using normative_spec; optionally write into catalog
        - auto: use catalog if present, otherwise generate (and optionally persist)
        """
        # Ensure catalog loaded/generated if needed
        self.ensure_lens_catalog(getattr(self, "output_dir", None))

        if self.lens_mode == "catalog":
            if not self.lens_catalog or station not in self.lens_catalog:
                raise ValueError(f"Lens catalog missing station: {station}")
            return self.lens_catalog[station]

        def _gen() -> List[List[str]]:
            lenses = generate_lens_matrix_llm(
                station=station,
                rows=rows,
                cols=cols,
                call_json_tail=self._call_llm_with_json_tail,
            )
            if self.write_catalog:
                self._merge_into_catalog(station, lenses)
            return lenses

        if self.lens_mode == "generate":
            return _gen()

        # auto mode
        if self.lens_catalog and station in self.lens_catalog:
            return self.lens_catalog[station]
        return _gen()

    def regenerate_full_catalog(self, output_dir: Path):
        """Generate a complete catalog from scratch using normative spec."""
        stations = list(STATION_SCHEMAS.keys())
        self.lens_catalog = {}
        for station in stations:
            schema = STATION_SCHEMAS[station]
            self.lens_catalog[station] = generate_lens_matrix_llm(
                station=station, 
                rows=schema["rows"], 
                cols=schema["cols"],
                call_json_tail=self._call_llm_with_json_tail
            )
        self.lens_catalog_meta = {"prompt_hash": prompt_hash_for_lenses(), "version": "v2"}
        self._save_catalog(output_dir)

    def save_budget_status(self):
        """Save budget status - placeholder for future implementation."""
        # TODO: Implement budget status persistence if needed
        pass
