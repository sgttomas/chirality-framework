#!/usr/bin/env python3
"""
Boundary linter for domain-driven architecture

Prevents cross-layer imports that violate clean architecture principles.
Run in CI to enforce architectural boundaries.
"""

import ast
import pathlib
import sys
from typing import Dict, List, Set

ROOT = pathlib.Path("chirality")

# Define layer boundaries - what each layer is forbidden to import
LAYER_RULES: Dict[str, Dict[str, List[str]]] = {
    "domain": {"forbid": ["infrastructure", "application"]},
    "application": {"forbid": ["infrastructure.prompts.builder"]},  # app should use interfaces
    # Infrastructure can import from anywhere (it's the outermost layer)
}


def find_imports_in_file(filepath: pathlib.Path) -> List[str]:
    """Extract all import module names from a Python file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content, filename=str(filepath))
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name:
                        imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return imports

    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}")
        return []


def check_layer_violations() -> List[tuple]:
    """Check for architectural boundary violations."""
    violations = []

    if not ROOT.exists():
        print(f"Warning: {ROOT} directory not found")
        return violations

    for py_file in ROOT.rglob("*.py"):
        # Skip __pycache__ and other generated files
        if "__pycache__" in str(py_file) or py_file.suffix != ".py":
            continue

        # Determine which layer this file belongs to
        relative_path = py_file.relative_to(ROOT)
        path_parts = list(relative_path.parts)

        if len(path_parts) < 2:
            continue  # Skip root-level files

        layer = path_parts[0]  # domain, application, infrastructure

        if layer not in LAYER_RULES:
            continue  # No rules for this layer

        # Check imports in this file
        imports = find_imports_in_file(py_file)

        for import_name in imports:
            # Only check chirality imports
            if not import_name.startswith("chirality."):
                continue

            # Extract the layer being imported
            import_parts = import_name.split(".")
            if len(import_parts) < 2:
                continue

            imported_layer = import_parts[1]  # domain, application, infrastructure

            # Check if this import is forbidden
            rules = LAYER_RULES[layer]
            forbidden_layers = rules.get("forbid", [])

            for forbidden in forbidden_layers:
                if import_name.startswith(f"chirality.{forbidden}"):
                    violations.append((py_file, import_name, layer, forbidden))

    return violations


def main():
    """Run boundary linting."""
    print("🔍 Checking architectural boundary violations...")

    violations = check_layer_violations()

    if not violations:
        print("✅ No architectural boundary violations found!")
        return 0

    print(f"❌ Found {len(violations)} architectural boundary violations:")
    print()

    for file_path, import_name, layer, forbidden in violations:
        print(f"VIOLATION: {file_path}")
        print(f"  {layer} layer importing from {forbidden}")
        print(f"  Import: {import_name}")
        print()

    print("Fix these violations to maintain clean architecture!")
    return 1


if __name__ == "__main__":
    sys.exit(main())
