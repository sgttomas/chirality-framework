#!/usr/bin/env python3
"""
Simple import fixer for domain-driven refactoring
"""

import os
import glob

# Import replacements
replacements = [
    ("from chirality.domain.types", "from chirality.domain.types"),
    ("from chirality.domain.constants", "from chirality.domain.constants"),
    ("from chirality.domain.stations", "from chirality.domain.stations"),
    ("from chirality.domain.validation", "from chirality.domain.validation"),
    ("from chirality.domain.matrices.canonical", "from chirality.domain.matrices.canonical"),
    ("from chirality.domain.provenance", "from chirality.domain.provenance"),
    (
        "from chirality.application.services.pipeline_service",
        "from chirality.application.services.pipeline_service",
    ),
    ("from chirality.infrastructure.llm.resolver", "from chirality.infrastructure.llm.resolver"),
    ("from chirality.infrastructure.llm.config", "from chirality.infrastructure.llm.config"),
    (
        "from chirality.infrastructure.llm.mock_resolvers",
        "from chirality.infrastructure.llm.mock_resolvers",
    ),
    (
        "from chirality.infrastructure.monitoring.tracer",
        "from chirality.infrastructure.monitoring.tracer",
    ),
    ("from chirality.infrastructure.api.guards", "from chirality.infrastructure.api.guards"),
    (
        "from chirality.infrastructure.llm.openai_adapter",
        "from chirality.infrastructure.llm.openai_adapter",
    ),
    ("import chirality.domain.types", "import chirality.domain.types"),
    (
        "import chirality.application.services.pipeline_service",
        "import chirality.application.services.pipeline_service",
    ),
    ("import chirality.domain.matrices.canonical", "import chirality.domain.matrices.canonical"),
    ("chirality.domain.types", "chirality.domain.types"),
    (
        "chirality.application.services.pipeline_service",
        "chirality.application.services.pipeline_service",
    ),
    ("chirality.domain.matrices.canonical", "chirality.domain.matrices.canonical"),
]


def fix_imports_in_file(filepath):
    """Fix imports in a single file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        for old_import, new_import in replacements:
            content = content.replace(old_import, new_import)

        if content != original_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated: {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")


def main():
    """Fix imports in all Python files"""
    # Find all Python files in chirality, tests, and scripts
    python_files = []

    for pattern in ["./chirality/**/*.py", "./tests/**/*.py", "./scripts/**/*.py"]:
        python_files.extend(glob.glob(pattern, recursive=True))

    # Filter out problematic files
    python_files = [f for f in python_files if os.path.isfile(f)]
    python_files = [f for f in python_files if "__pycache__" not in f]

    print(f"Processing {len(python_files)} Python files...")

    for filepath in python_files:
        fix_imports_in_file(filepath)

    print("Import fixing complete!")


if __name__ == "__main__":
    main()
