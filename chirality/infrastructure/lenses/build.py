"""
Lens Builder System.

Generates lens text from triples using stateless LLM calls.
Each lens is computed independently and cached by lens_id.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path

from ..llm.openai_adapter import call_responses_api


class LensBuilder:
    """
    Builds lens text from lens triples statelessly.

    Each lens is generated independently without memory.
    Results are cached by lens_id for reuse.
    """

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        temperature: float = 0.2,  # CRITICAL: Lenses must be deterministic
        system_prompt: Optional[str] = None,
    ):
        """
        Initialize lens builder.

        Args:
            model: LLM model identifier
            temperature: Sampling temperature
            system_prompt: Optional custom system prompt
        """
        self.model = model
        self.temperature = temperature
        self.system_prompt = system_prompt or self._default_system_prompt()

    def build_lens_catalog(self, lens_triples_path: Path, output_path: Path) -> int:
        """
        Build complete lens catalog from triples.

        Args:
            lens_triples_path: Path to lenses_triples.json
            output_path: Path to write lens_catalog.jsonl

        Returns:
            Number of lenses generated
        """
        # Load lens triples
        with open(lens_triples_path, "r") as f:
            triples_data = json.load(f)

        lenses = triples_data["lenses"]

        # Generate lens text for each triple
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        generated_count = 0
        with open(output_path, "w") as f:
            for lens in lenses:
                lens_text = self._generate_lens_text(lens)

                # Write to JSONL catalog
                catalog_entry = {
                    "lens_id": lens["lens_id"],
                    "row": lens["row"],
                    "col": lens["col"],
                    "station": lens["station"],
                    "text": lens_text,
                    "matrix_source": lens["matrix_source"],
                    "kernel_hash": lens["kernel_hash"],
                    "model": lens["model"],
                    "prompt_version": lens["prompt_version"],
                }

                f.write(json.dumps(catalog_entry) + "\n")
                generated_count += 1

        return generated_count

    def _generate_lens_text(self, lens_spec: Dict[str, Any]) -> str:
        """
        Generate lens text for a single lens specification.

        Args:
            lens_spec: Lens specification dict

        Returns:
            Generated lens text
        """
        row = lens_spec["row"]
        col = lens_spec["col"]
        station = lens_spec["station"]

        # Build user prompt
        user_prompt = f"""
Generate a lens for semantic interpretation.

Ontological coordinates:
- Row perspective: {row}
- Column perspective: {col}
- Station context: {station}

Create a brief, focused interpretive lens that guides how semantic content
should be understood through this specific combination of row × column × station.

The lens should be 1-2 sentences that capture the essence of interpreting
content through this ontological position.

Examples:
- "Through the lens of normative × necessity at Problem Statement: Focus on essential standards that must be established."
- "Through the lens of operative × sufficiency at Requirements: Consider practical adequacy for implementation."
"""

        # Call LLM statelessly
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response, metadata = call_responses_api(
            messages=messages,
            temperature=0.2,  # CRITICAL: Force deterministic temperature
            max_tokens=512,  # Lenses should be brief
            json_only=True,
        )

        # Extract text from JSON response
        if "text" in response:
            return response["text"]
        elif "lens" in response:
            return response["lens"]
        elif isinstance(response, dict):
            # Try to find text in any field
            for value in response.values():
                if isinstance(value, str) and len(value) > 10:
                    return value

        # Fallback if JSON parsing fails
        return f"Through the lens of {row} × {col} at {station}"

    def _default_system_prompt(self) -> str:
        """Default system prompt for lens generation."""
        return """
You are generating interpretive lenses for the Chirality Framework.

A lens is a brief, focused statement that guides semantic interpretation
through specific ontological coordinates (row × column × station).

Each lens should:
1. Be concise (1-2 sentences)
2. Capture the essence of the ontological position
3. Guide interpretation without being overly prescriptive
4. Use clear, accessible language

Return JSON with: {"text": "lens text here"}
"""

    def extract_component_lenses(self, catalog_path: Path, component: str, output_path: Path):
        """
        Extract lenses for a specific component/matrix.

        Args:
            catalog_path: Path to lens_catalog.jsonl
            component: Component name (e.g., 'M', 'E', 'X')
            output_path: Path to write component lenses JSON
        """
        component_lenses = {}

        with open(catalog_path, "r") as f:
            for line in f:
                entry = json.loads(line)
                if entry["matrix_source"] == component:
                    key = f"{entry['row']}×{entry['col']}"
                    component_lenses[key] = {
                        "lens_id": entry["lens_id"],
                        "text": entry["text"],
                        "row": entry["row"],
                        "col": entry["col"],
                        "station": entry["station"],
                    }

        # Save component lenses
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_data = {
            "component": component,
            "lens_count": len(component_lenses),
            "lenses": component_lenses,
        }

        with open(output_path, "w") as f:
            json.dump(output_data, f, indent=2)


def build_lens_catalog(triples_path: Path, output_path: Path, model: str = "gpt-4o-mini") -> int:
    """
    Convenience function to build lens catalog.

    Args:
        triples_path: Path to lenses_triples.json
        output_path: Path to write lens_catalog.jsonl
        model: LLM model identifier

    Returns:
        Number of lenses generated
    """
    builder = LensBuilder(model=model)
    return builder.build_lens_catalog(triples_path, output_path)
