"""
JSON Repair Helper.

Provides repair pass functionality for malformed JSON responses.
Used by both dialogue runner and cell runner.
"""

import json
from typing import Dict, Any, List, Callable, Optional, Tuple


def try_parse_json_or_repair(
    messages: List[Dict[str, str]],
    adapter_call: Callable,
    schema_hint: Optional[str] = None,
    max_repair_attempts: int = 1,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Attempt to parse JSON, with repair pass if needed.

    Args:
        messages: List of chat messages
        adapter_call: Function to call LLM (should return (response, metadata))
        schema_hint: Optional schema hint for repair prompt
        max_repair_attempts: Maximum repair attempts

    Returns:
        Tuple of (parsed_json, metadata)

    Raises:
        json.JSONDecodeError: If JSON still invalid after repairs
    """
    # First attempt
    response, metadata = adapter_call(messages)

    # Try to parse response
    content = response.get("content", response.get("text", ""))

    try:
        return json.loads(content), metadata
    except json.JSONDecodeError:
        # Original parse failed, try repair
        for attempt in range(max_repair_attempts):
            # Create repair message
            repair_content = (
                "The previous output was invalid JSON. "
                "Return valid JSON only"
                + (f" matching this shape: {schema_hint}" if schema_hint else "")
                + "."
            )

            repair_message = {"role": "user", "content": repair_content}

            # Add repair message and try again
            repair_messages = (
                messages + [{"role": "assistant", "content": content}] + [repair_message]
            )

            response, metadata = adapter_call(repair_messages)
            content = response.get("content", response.get("text", ""))

            try:
                return json.loads(content), metadata
            except json.JSONDecodeError:
                if attempt == max_repair_attempts - 1:
                    # Last attempt failed, raise with helpful error
                    raise json.JSONDecodeError(
                        f"JSON repair failed after {max_repair_attempts} attempts. "
                        f"Final response: {content[:200]}...",
                        content,
                        0,
                    )
                continue

    # Should not reach here, but handle gracefully
    raise json.JSONDecodeError(f"Unexpected error parsing JSON: {content}", content, 0)


def create_schema_hint(expected_fields: Dict[str, str]) -> str:
    """
    Create schema hint string from expected fields.

    Args:
        expected_fields: Dict mapping field names to types

    Returns:
        Schema hint string
    """
    field_hints = []
    for field, field_type in expected_fields.items():
        if field_type.startswith("list"):
            field_hints.append(f'"{field}": [...]')
        elif field_type.startswith("dict"):
            field_hints.append(f'"{field}": {{...}}')
        else:
            field_hints.append(f'"{field}": "..."')

    return "{" + ", ".join(field_hints) + "}"


def create_matrix_schema_hint(matrix_name: str, step: str) -> str:
    """
    Create schema hint for matrix responses.

    Args:
        matrix_name: Matrix name (C, F, D, etc.)
        step: Step type (mechanical, interpreted, lensed, etc.)

    Returns:
        Schema hint string
    """
    base_hint = {
        "artifact": "matrix",
        "name": matrix_name,
        "station": "...",
        "rows": "[...]",
        "cols": "[...]",
        "step": step,
    }

    if step == "lenses":
        base_hint["lenses"] = "[[...]]"
    else:
        base_hint["elements"] = "[[...]]"
        if step not in ["base", "transpose"]:
            base_hint["op"] = "..."

    return create_schema_hint({k: str(v) for k, v in base_hint.items()})


def create_tensor_cell_schema_hint(tensor_name: str) -> str:
    """
    Create schema hint for tensor cell responses.

    Args:
        tensor_name: Tensor name (M, W, U, N)

    Returns:
        Schema hint string
    """
    return create_schema_hint({"tensor": tensor_name, "value": "string", "confidence": "0.0-1.0"})
