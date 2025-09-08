#!/usr/bin/env python3
"""
Import rewriter using Bowler for domain-driven refactoring
"""

from bowler import Query

# Import mapping: old_module -> new_module
import_mapping = {
    "chirality.domain.types": "chirality.domain.types",
    "chirality.core.constants": "chirality.domain.constants",
    "chirality.core.stations": "chirality.domain.stations",
    "chirality.core.validate": "chirality.domain.validation",
    "chirality.domain.matrices.canonical": "chirality.domain.matrices.canonical",
    "chirality.core.provenance_schema": "chirality.domain.provenance",
    "chirality.application.services.pipeline_service": "chirality.application.services.pipeline_service",
    "chirality.core.cell_resolver": "chirality.infrastructure.llm.resolver",
    "chirality.core.llm_config": "chirality.infrastructure.llm.config",
    "chirality.core.resolvers": "chirality.infrastructure.llm.mock_resolvers",
    "chirality.core.tracer": "chirality.infrastructure.monitoring.tracer",
    "chirality.core.api_guards": "chirality.infrastructure.api.guards",
    "chirality.core.llm_client": "chirality.infrastructure.llm.openai_adapter",
    "chirality.exporters.working_memory_exporter": "chirality.infrastructure.exporters.working_memory_exporter",
    "chirality.exporters.manifest_exporter": "chirality.infrastructure.exporters.manifest_exporter",
    "chirality.exporters.snapshot_exporter": "chirality.infrastructure.exporters.snapshot_exporter",
}


def main():
    """Rewrite imports using Bowler"""

    for old_module, new_module in import_mapping.items():
        print(f"Rewriting {old_module} -> {new_module}")
        query = Query(".")
        query = query.select_module(old_module).rename(new_module)
        query.execute(interactive=False, write=True)

    print("Import rewriting complete!")


if __name__ == "__main__":
    main()
