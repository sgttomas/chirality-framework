#!/usr/bin/env python3
"""
CLI for Chirality Framework Semantic Calculator

Provides direct access to the 3-stage pipeline for debugging and observability.
Focus on the compute-cell command which shows the complete transformation
from mechanical k-products through semantic resolution to ontological lensing.
"""

import click
import os
import uuid
from datetime import datetime, timezone
import json
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

def _get_version():
    """Reads the version from the VERSION.md file."""
    try:
        # Path to VERSION.md at the project root, relative to this file
        version_path = Path(__file__).parent.parent / "VERSION.md"
        with open(version_path, "r") as f:
            # First line should be like "15.0.1 — ..."
            return f.readline().split("—")[0].strip()
    except Exception:
        return "0.0.0" # Fallback version

# Load environment variables from .env file in project root
load_dotenv(override=True)

# Import core components
from .core.types import Cell, Matrix
from .core.context import SemanticContext
from .core.matrices import MATRIX_A, MATRIX_B, MATRIX_J
from .core.constants import CANONICAL_PROBLEM
from .core.operations import (
    compute_cell_C,
    compute_cell_F,
    compute_cell_D,
    compute_matrix_C,
    compute_matrix_F,
    compute_matrix_D
)
from .core.cell_resolver import CellResolver
from .core.resolvers import EchoResolver
from .exporters.working_memory_exporter import Neo4jWorkingMemoryExporter
from .core.tracer import JSONLTracer

# Click styling for better output
STAGE_STYLE = {"fg": "cyan", "bold": True}
SUCCESS_STYLE = {"fg": "green", "bold": True}
ERROR_STYLE = {"fg": "red", "bold": True}
INFO_STYLE = {"fg": "yellow"}
DIM_STYLE = {"dim": True}


@click.group()
@click.version_option(version=_get_version(), prog_name="Chirality Framework")
def cli():
    """
    Chirality Framework - Semantic Calculator

    A procedurally-rigorous methodology for structured problem-solving
    through a 3-stage semantic interpretation pipeline:

    \b
    Stage 1 (Combinatorial): Mechanical k-product generation
    Stage 2 (Semantic): LLM resolution of word pairs
    Stage 3 (Lensing): Ontological interpretation through coordinates

    Use 'compute-cell' to debug individual cells through the pipeline.
    """
    pass


@cli.command()
@click.argument('matrix', type=click.Choice(['C', 'F', 'D'], case_sensitive=False))
@click.option('--i', 'row', type=click.IntRange(0, 2), required=True, 
              help='Row index (0-2)')
@click.option('--j', 'col', type=click.IntRange(0, 3), required=True,
              help='Column index (0-3)')
@click.option('--verbose', '-v', is_flag=True,
              help='Show intermediate results from each stage')
@click.option('--resolver', type=click.Choice(['echo', 'openai'], case_sensitive=False),
              default='echo', help='Resolver to use (default: echo for testing)')
@click.option('--api-key', envvar='OPENAI_API_KEY',
              help='OpenAI API key (or set OPENAI_API_KEY env var)')
@click.option('--trace/--no-trace', default=False,
              help='Enable JSONL tracing to traces/ directory')
@click.option('--neo4j-export/--no-neo4j-export', default=False,
              help='Enable writing output to Neo4j.')
def compute_cell(matrix: str, row: int, col: int, verbose: bool, 
                resolver: str, api_key: Optional[str], trace: bool, neo4j_export: bool):
    """
    Compute a single cell through the 3-stage pipeline.

    \b
    Examples:
        chirality compute-cell C --i 0 --j 0 -v
        chirality compute-cell F --i 1 --j 2 --verbose
        chirality compute-cell D --i 2 --j 1
    """
    resolver_obj = None
    tracer_obj = None
    exporter_obj = None

    try:
        # Setup resolver
        if resolver == 'openai':
            if not api_key:
                click.echo(click.style(
                    "Error: OpenAI API key required. Set OPENAI_API_KEY or use --api-key",
                    **ERROR_STYLE
                ))
                sys.exit(1)
            resolver_obj = CellResolver(api_key=api_key)
            click.echo(click.style("Using OpenAI resolver", **INFO_STYLE))
        else:
            resolver_obj = EchoResolver()
            click.echo(click.style("Using Echo resolver (deterministic mock)", **INFO_STYLE))
        
        # Setup tracer and exporter
        tracer_obj = JSONLTracer() if trace else None
        if trace:
            click.echo(click.style("Tracing enabled -> traces/", **INFO_STYLE))
        
        exporter_obj = None
        if neo4j_export:
            # Generate a unique run/session id for this CLI invocation
            run_id = f"cli-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
            run_tag = "cli"
            run_user = os.getenv("USER") or os.getenv("USERNAME")
            exporter_obj = Neo4jWorkingMemoryExporter(
                run_id=run_id,
                run_tag=run_tag,
                run_user=run_user,
            )
            click.echo(click.style(f"Neo4j export enabled (run_id={run_id})", **INFO_STYLE))

        # Get canonical matrices and context
        A, B, J = MATRIX_A, MATRIX_B, MATRIX_J
        valley_summary = "Problem Statement -> [Problem Requirements] -> Solution Objectives"
        
        click.echo()
        click.echo(click.style(f"Computing {matrix}[{row},{col}]", **STAGE_STYLE))
        click.echo(click.style("=" * 50, **DIM_STYLE))
        
        # Compute the requested cell based on matrix type
        if matrix.upper() == 'C':
            if verbose:
                # Show explicit 3-stage breakdown for C using helper
                _show_c_computation_verbose(row, col, A, B, resolver_obj, valley_summary, tracer_obj)
            # Always compute final cell to show consolidated result and provenance
            cell = compute_cell_C(row, col, A, B, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            _show_cell_result(cell, A.row_labels[row], B.col_labels[col])
                
        elif matrix.upper() == 'F':
            C = compute_matrix_C(A, B, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            if verbose:
                # Minimal staged view for F: element-wise pair → resolve → lens
                click.echo()
                click.echo(click.style("STAGE 1: Element-wise (J ⊙ C)", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                j_cell = J.get_cell(row, col)
                c_cell = C.get_cell(row, col)
                pair = f"{j_cell.value} * {c_cell.value}"
                click.echo(f"  Pair: {pair}")

                ctx1 = SemanticContext(
                    station_context="Solution Objectives",
                    valley_summary=valley_summary,
                    row_label=J.row_labels[row],
                    col_label=J.col_labels[col],
                    operation_type="*",
                    terms={"pair": pair},
                    matrix="F",
                    i=row,
                    j=col,
                )
                resolved_result = resolver_obj.resolve_semantic_pair(pair, ctx1)
                click.echo(click.style("STAGE 2: Semantic Resolution", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                click.echo(f"  {pair} → {click.style(resolved_result.text, fg='green')}")

                click.echo()
                click.echo(click.style("STAGE 3: Ontological Lensing", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                ctx2 = SemanticContext(
                    station_context="Solution Objectives",
                    valley_summary=valley_summary,
                    row_label=J.row_labels[row],
                    col_label=J.col_labels[col],
                    operation_type="interpret",
                    terms={"content": resolved_result.text, "problem": CANONICAL_PROBLEM},
                    matrix="F",
                    i=row,
                    j=col,
                )
                
                # Show the universal 3-step lensing process
                click.echo("  Step 1 - Column Lens:")
                col_result = resolver_obj.apply_column_lens(resolved_result.text, ctx2)
                click.echo(f"    {col_result.text}")
                
                click.echo("  Step 2 - Row Lens:")
                row_result = resolver_obj.apply_row_lens(resolved_result.text, ctx2)
                click.echo(f"    {row_result.text}")
                
                click.echo("  Step 3 - Final Synthesis:")
                final_result = resolver_obj.synthesize_lensed_perspectives(col_result.text, row_result.text, ctx2)
                click.echo(f"    {final_result.text}")

            cell = compute_cell_F(row, col, J, C, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            _show_cell_result(cell, J.row_labels[row], J.col_labels[col])
                
        elif matrix.upper() == 'D':
            C = compute_matrix_C(A, B, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            F = compute_matrix_F(J, C, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            if verbose:
                # Minimal staged view for D: synthesis formula → lens
                click.echo()
                click.echo(click.style("STAGE 1: Mechanical Formation", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                a_cell = A.get_cell(row, col)
                f_cell = F.get_cell(row, col)
                synthesis = f"{a_cell.value} applied to frame the problem; {f_cell.value} to resolve the problem."
                click.echo(f"  {synthesis}")

                click.echo()
                click.echo(click.style("STAGE 2: Semantic Operation (Mechanical +)", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                click.echo(f"  A[{row},{col}] + F[{row},{col}] → {synthesis}")

                click.echo()
                click.echo(click.style("STAGE 3: Ontological Lensing", **STAGE_STYLE))
                click.echo(click.style("-" * 40, **DIM_STYLE))
                ctx = SemanticContext(
                    station_context="Solution Objectives",
                    valley_summary=valley_summary,
                    row_label=A.row_labels[row],
                    col_label=A.col_labels[col],
                    operation_type="interpret",
                    terms={"content": synthesis, "problem": CANONICAL_PROBLEM},
                    matrix="D",
                    i=row,
                    j=col,
                )
                
                # Show the universal 3-step lensing process
                click.echo("  Step 1 - Column Lens:")
                col_result = resolver_obj.apply_column_lens(synthesis, ctx)
                click.echo(f"    {col_result.text}")
                
                click.echo("  Step 2 - Row Lens:")
                row_result = resolver_obj.apply_row_lens(synthesis, ctx)
                click.echo(f"    {row_result.text}")
                
                click.echo("  Step 3 - Final Synthesis:")
                final_result = resolver_obj.synthesize_lensed_perspectives(col_result.text, row_result.text, ctx)
                click.echo(f"    {final_result.text}")

            cell = compute_cell_D(row, col, A, F, resolver_obj, valley_summary, tracer_obj, exporter_obj)
            _show_cell_result(cell, A.row_labels[row], A.col_labels[col])
            
    except Exception as e:
        click.echo(click.style(f"Error: {e}", **ERROR_STYLE))
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    finally:
        # Safely close connections
        if tracer_obj:
            tracer_obj.close()
            click.echo(click.style("✓ Trace file closed.", **DIM_STYLE))
        if exporter_obj:
            exporter_obj.close()
            click.echo(click.style("✓ Neo4j connection closed.", **DIM_STYLE))


def _show_c_computation_verbose(row: int, col: int, A: Matrix, B: Matrix, 
                                resolver, valley_summary: str, tracer):
    """Show verbose output for C matrix cell computation."""
    click.echo()
    click.echo(click.style("STAGE 1: Combinatorial (Mechanical)", **STAGE_STYLE))
    click.echo(click.style("-" * 40, **DIM_STYLE))
    
    # Stage 1: Generate k-products
    raw_products = []
    for k in range(A.shape[1]):
        a_cell = A.get_cell(row, k)
        b_cell = B.get_cell(k, col)
        product = f"{a_cell.value} * {b_cell.value}"
        raw_products.append(product)
        click.echo(f"  k={k}: {product}")
    
    click.echo()
    click.echo(click.style("STAGE 2: Semantic Resolution (LLM)", **STAGE_STYLE))
    click.echo(click.style("-" * 40, **DIM_STYLE))
    
    # Stage 2: Resolve each pair
    resolved = []
    for k, product in enumerate(raw_products):
        context = SemanticContext(
            station_context="Problem Requirements",
            valley_summary=valley_summary,
            row_label=A.row_labels[row],
            col_label=B.col_labels[col],
            operation_type="*",
            terms={"pair": product},
            matrix="C",
            i=row,
            j=col
        )
        concept_result = resolver.resolve_semantic_pair(product, context)
        resolved.append(concept_result.text)
        click.echo(f"  {product} → {click.style(concept_result.text, fg='green')}")
    
    click.echo()
    click.echo(click.style("STAGE 3: Ontological Lensing", **STAGE_STYLE))
    click.echo(click.style("-" * 40, **DIM_STYLE))
    
    # Stage 3: Universal 3-step ontological lensing
    combined = ", ".join(resolved)
    click.echo(f"  Combined: {combined[:80]}...")
    
    context = SemanticContext(
        station_context="Problem Requirements",
        valley_summary=valley_summary,
        row_label=A.row_labels[row],
        col_label=B.col_labels[col],
        operation_type="interpret",
        terms={"content": combined, "problem": CANONICAL_PROBLEM},
        matrix="C",
        i=row,
        j=col
    )
    
    # Show the universal 3-step lensing process
    click.echo("  Step 1 - Column Lens:")
    col_result = resolver.apply_column_lens(combined, context)
    click.echo(f"    {col_result.text}")
    
    click.echo("  Step 2 - Row Lens:")
    row_result = resolver.apply_row_lens(combined, context)
    click.echo(f"    {row_result.text}")
    
    click.echo("  Step 3 - Final Synthesis:")
    final_result = resolver.synthesize_lensed_perspectives(col_result.text, row_result.text, context)
    click.echo(f"    {final_result.text}")
    
    click.echo()
    click.echo(click.style("FINAL RESULT:", **SUCCESS_STYLE))
    click.echo(click.style("-" * 40, **DIM_STYLE))
    click.echo(f"  {final_result.text}")


def _show_cell_result(cell: Cell, row_label: str, col_label: str):
    """Show the final cell result and provenance."""
    click.echo()
    click.echo(click.style("Result:", **SUCCESS_STYLE))
    click.echo(f"  Coordinates: ({row_label}, {col_label})")
    click.echo(f"  Value: {cell.value}")
    
    click.echo()
    click.echo(click.style("Provenance:", **INFO_STYLE))
    _show_provenance(cell.provenance)


def _show_provenance(provenance: dict, indent: int = 2):
    """Pretty print provenance dictionary."""
    for key, value in provenance.items():
        if isinstance(value, list) and len(value) > 3:
            # Abbreviate long lists
            click.echo(f"{' ' * indent}{key}: [{len(value)} items]")
            for item in value[:2]:
                click.echo(f"{' ' * (indent + 2)}- {item}")
            click.echo(f"{' ' * (indent + 2)}... ({len(value) - 2} more)")
        else:
            click.echo(f"{' ' * indent}{key}: {value}")


@cli.command()
def info():
    """
    Display information about the Chirality Framework semantic calculator.
    """
    click.echo(click.style("Chirality Framework - Semantic Calculator", **STAGE_STYLE))
    click.echo(click.style("=" * 50, **DIM_STYLE))
    click.echo()
    click.echo(f"Version: {_get_version()}")
    click.echo("Algorithm: 3-stage semantic interpretation pipeline")
    click.echo()
    click.echo(click.style("Canonical Matrices:", **INFO_STYLE))
    # Matrix A
    click.echo("  A: 3×4 (Axioms / Problem Statement)")
    click.echo(f"    Station: {MATRIX_A.station}")
    click.echo(f"    Rows:   {', '.join(MATRIX_A.row_labels)}")
    click.echo(f"    Columns:{' ' if MATRIX_A.col_labels else ''}{', '.join(MATRIX_A.col_labels)}")
    # Matrix B
    click.echo("  B: 4×4 (Bridge / Decision Basis)")
    click.echo(f"    Station: {MATRIX_B.station}")
    click.echo(f"    Rows:   {', '.join(MATRIX_B.row_labels)}")
    click.echo(f"    Columns:{' ' if MATRIX_B.col_labels else ''}{', '.join(MATRIX_B.col_labels)}")
    # Matrix J
    click.echo("  J: 3×4 (Judgment / Verification)")
    click.echo(f"    Station: {MATRIX_J.station}")
    click.echo(f"    Rows:   {', '.join(MATRIX_J.row_labels)}")
    click.echo(f"    Columns:{' ' if MATRIX_J.col_labels else ''}{', '.join(MATRIX_J.col_labels)}")
    click.echo()
    click.echo(click.style("Result Matrices:", **INFO_STYLE))
    click.echo("  C = A * B: Problem Requirements (3×4)")
    click.echo("  F = J ⊙ C: Solution Objectives (3×4)")
    click.echo("  D = synthesis(A, F): Solution Objectives (3×4)")
    # Explicit axes for derived matrices (without computing them)
    # F axes mirror J's rows × J's columns
    click.echo("    F Axes:")
    click.echo(f"      Station: Solution Objectives")
    click.echo(f"      Rows:   {', '.join(MATRIX_J.row_labels)}")
    click.echo(f"      Columns:{' ' if MATRIX_J.col_labels else ''}{', '.join(MATRIX_J.col_labels)}")
    # D axes mirror A's rows × A's columns (station is Objectives)
    click.echo("    D Axes:")
    click.echo(f"      Station: Solution Objectives")
    click.echo(f"      Rows:   {', '.join(MATRIX_A.row_labels)}")
    click.echo(f"      Columns:{' ' if MATRIX_A.col_labels else ''}{', '.join(MATRIX_A.col_labels)}")
    click.echo()
    click.echo(click.style("3-Stage Pipeline:", **INFO_STYLE))
    click.echo("  Stage 1: Combinatorial (mechanical k-products)")
    click.echo("  Stage 2: Semantic (LLM pair resolution)")
    click.echo("  Stage 3: Lensing (ontological interpretation)")
    click.echo()
    click.echo("Use 'chirality compute-cell --help' for debugging individual cells")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    cli()
