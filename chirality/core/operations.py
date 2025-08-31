"""
Three-Stage Cell Pipeline Implementation for Chirality Framework v15.0.1

This is the "secret sauce" - the core algorithm that transforms
structural combinations into meaningful semantic insights through
a precise 3-stage interpretation process:

Stage 1 (Combinatorial): Mechanical generation of k-products
Stage 2 (Semantic): LLM resolution of word pairs into concepts  
Stage 3 (Lensing): Ontological interpretation through row/column coordinates

This embodies the "semantic calculator" philosophy: procedurally rigorous
methodology with fixed ontological structure that produces meaningful outputs 
through constrained stochastic processing of canonical inputs.
"""

from typing import List, Optional
from dataclasses import dataclass
from .types import Cell, Matrix, RichResult
from .context import SemanticContext
from .cell_resolver import CellResolver
from .tracer import JSONLTracer
from .provenance_schema import create_provenance
from .constants import CANONICAL_PROBLEM
from ..exporters.working_memory_exporter import Neo4jWorkingMemoryExporter


@dataclass
class SimpleResult:
    """Simple result object for tracer compatibility."""
    text: str
    terms_used: List[str] 
    warnings: List[str]


def _perform_three_step_lensing(content: str, context: SemanticContext, resolver: CellResolver, tracer: Optional[JSONLTracer] = None) -> tuple[RichResult, RichResult, RichResult]:
    """
    Universal 3-step ontological lensing process for ALL matrices.
    
    Step 1: Column lens interpretation
    Step 2: Row lens interpretation  
    Step 3: Final synthesis of both perspectives
    
    Args:
        content: Content to interpret (resolved concepts for C/F, synthesis statement for D)
        context: SemanticContext with station, coordinates, and problem
        resolver: CellResolver with the 3 lensing methods
        tracer: Optional tracer for observability
        
    Returns:
        Tuple of (column_perspective, row_perspective, final_synthesis)
    """
    # Step 1: Column lens
    column_result = resolver.apply_column_lens(content, context)
    if tracer:
        tracer.trace_stage(
            "lensing:column",
            context,
            SimpleResult(
                text=column_result.text,
                terms_used=column_result.terms_used,
                warnings=column_result.warnings
            ),
            {
                "station": context.station_context,
                "valley_summary": context.valley_summary,
                "stage_plan": ["column_lens"],
            },
        )
    
    # Step 2: Row lens  
    row_result = resolver.apply_row_lens(content, context)
    if tracer:
        tracer.trace_stage(
            "lensing:row",
            context,
            SimpleResult(
                text=row_result.text,
                terms_used=row_result.terms_used,
                warnings=row_result.warnings
            ),
            {
                "station": context.station_context,
                "valley_summary": context.valley_summary,
                "stage_plan": ["row_lens"],
            },
        )
    
    # Step 3: Synthesize both perspectives
    final_result = resolver.synthesize_lensed_perspectives(column_result.text, row_result.text, context)
    if tracer:
        tracer.trace_stage(
            "lensing:final",
            context,
            SimpleResult(
                text=final_result.text,
                terms_used=final_result.terms_used,
                warnings=final_result.warnings
            ),
            {
                "station": context.station_context,
                "valley_summary": context.valley_summary,
                "stage_plan": ["column_lens", "row_lens", "final_synthesis"],
            },
        )
    
    return column_result, row_result, final_result


def compute_cell_C(i: int, j: int, A: Matrix, B: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional['Neo4jWorkingMemoryExporter'] = None) -> Cell:
    """
    Complete 3-stage pipeline for computing C[i,j] = A[i,:] dot B[:,j]
    
    This is the core algorithm that transforms mechanical combinations
    into meaningful semantic insights. Each stage builds on the previous:
    
    Stage 1 (Combinatorial): Generate k-products mechanically (no LLM)
    Stage 2 (Semantic): Resolve word pairs into concepts (LLM)
    Stage 3 (Lensing): Apply ontological interpretation (LLM with deep context)
    
    Args:
        i: Row index in result matrix C
        j: Column index in result matrix C  
        A: Left input matrix (3x4)
        B: Right input matrix (4x4)
        resolver: CellResolver for LLM operations
        valley_summary: Current position in semantic valley
        
    Returns:
        Cell with final semantic result and complete provenance
    """
    
    # Stage 1: Combinatorial (mechanical, no LLM)
    raw_products = []
    for k in range(A.shape[1]):  # A is 3x4, so k goes 0-3
        a_cell = A.get_cell(i, k)
        b_cell = B.get_cell(k, j)
        product_pair = f"{a_cell.value} * {b_cell.value}"
        raw_products.append(product_pair)
    
    # Trace Stage 1 (combinatorial - no LLM call, just mechanical result)
    if tracer:
        stage1_context = SemanticContext(
            station_context="Problem Requirements",
            valley_summary=valley_summary,
            row_label=A.row_labels[i],
            col_label=B.col_labels[j],
            operation_type="combinatorial",
            terms={"products": raw_products},
            matrix="C",
            i=i,
            j=j
        )
        # Tracer expects cell context and result - we'll adapt SemanticContext
        tracer.trace_stage("product:combinatorial", stage1_context, SimpleResult(
            text=", ".join(raw_products),
            terms_used=[f"k={k}" for k in range(len(raw_products))],
            warnings=[]
        ), {
            "station": "Problem Requirements", 
            "valley_summary": valley_summary,
            "products": raw_products
        })

    # Stage 2: Semantic Resolution (LLM resolves each pair)
    resolved_concepts = []
    for k, product_pair in enumerate(raw_products):
        # Create SemanticContext object for this resolution
        context_for_stage2 = SemanticContext(
            station_context="Problem Requirements",
            valley_summary=valley_summary,
            row_label=A.row_labels[i],
            col_label=B.col_labels[j],
            operation_type="*",
            terms={"pair": product_pair},
            matrix="C",
            i=i,
            j=j
        )
        concept_result = resolver.resolve_semantic_pair(product_pair, context_for_stage2)
        resolved_concepts.append(concept_result)
        
        # Trace each individual semantic resolution
        if tracer:
            tracer.trace_stage(f"product:k={k}", context_for_stage2, SimpleResult(
                text=concept_result.text,
                terms_used=concept_result.terms_used,
                warnings=concept_result.warnings
            ), {
                "station": "Problem Requirements", 
                "valley_summary": valley_summary,
                "products": [product_pair]
            })

    # Stage 3: Universal 3-step ontological lensing
    combined_concepts = ", ".join([result.text for result in resolved_concepts])
    lensing_context = SemanticContext(
        station_context="Problem Requirements",
        valley_summary=valley_summary,
        row_label=A.row_labels[i],
        col_label=B.col_labels[j],
        operation_type="interpret",
        terms={"content": combined_concepts, "problem": CANONICAL_PROBLEM},
        matrix="C",
        i=i,
        j=j
    )
    
    # Perform universal 3-step lensing process
    column_result, row_result, final_result = _perform_three_step_lensing(
        combined_concepts, lensing_context, resolver, tracer
    )

    cell = Cell(
        row=i,
        col=j,
        value=final_result.text,
        provenance=create_provenance(
            operation="compute_C",
            coordinates=f"({A.row_labels[i]}, {B.col_labels[j]})",
            stage_data={
                "stage_1_construct": {"texts": raw_products, "metadata": {}, "terms_used": [f"k={k}" for k in range(len(raw_products))], "warnings": []},
                "stage_2_semantic": {"texts": [result.text for result in resolved_concepts], "metadata": [result.metadata for result in resolved_concepts], "terms_used": [result.terms_used for result in resolved_concepts], "warnings": [result.warnings for result in resolved_concepts]},
                "stage_3_column_lensed": {"text": column_result.text, "metadata": column_result.metadata, "terms_used": column_result.terms_used, "warnings": column_result.warnings},
                "stage_4_row_lensed": {"text": row_result.text, "metadata": row_result.metadata, "terms_used": row_result.terms_used, "warnings": row_result.warnings},
                "stage_5_final_synthesis": {"text": final_result.text, "metadata": final_result.metadata, "terms_used": final_result.terms_used, "warnings": final_result.warnings},
            },
            sources=["A", "B"],
            traced=tracer is not None
        )
    )
    
    # Export to Neo4j if exporter is provided
    if exporter:
        exporter.export_cell_computation(cell, lensing_context)
    
    return cell


def compute_cell_F(i: int, j: int, J: Matrix, C: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional['Neo4jWorkingMemoryExporter'] = None) -> Cell:
    """
    Element-wise operation F[i,j] = J[i,j] ⊙ C[i,j] with lensing
    
    Since coordinates match, skip combinatorial stage.
    Stage 1: Direct semantic multiplication 
    Stage 2: Apply ontological lens for objectives context
    
    Args:
        i: Row index
        j: Column index
        J: Judgment matrix (3x4)
        C: Composition matrix (3x4)
        resolver: CellResolver for LLM operations
        valley_summary: Current position in semantic valley
        
    Returns:
        Cell with element-wise multiplication result
    """

    # Stage 1: Direct element-wise multiplication (same coordinates)
    j_cell = J.get_cell(i, j)
    c_cell = C.get_cell(i, j)
    element_pair = f"{j_cell.value} * {c_cell.value}"
    
    context_for_stage1 = SemanticContext(
        station_context="Solution Objectives", 
        valley_summary=valley_summary,
        row_label=J.row_labels[i], 
        col_label=J.col_labels[j],
        operation_type="*", 
        terms={"pair": element_pair},
        matrix="F",
        i=i,
        j=j
    )
    resolved_result = resolver.resolve_semantic_pair(element_pair, context_for_stage1)
    
    # Trace Stage 1 (element-wise semantic resolution)
    if tracer:
        tracer.trace_stage("element-wise", context_for_stage1, SimpleResult(
            text=resolved_result.text,
            terms_used=resolved_result.terms_used,
            warnings=resolved_result.warnings
        ), {
            "station": "Solution Objectives", 
            "valley_summary": valley_summary,
            "products": [element_pair]
        })

    # Stage 2: Universal 3-step ontological lensing
    lensing_context = SemanticContext(
        station_context="Solution Objectives", 
        valley_summary=valley_summary,
        row_label=J.row_labels[i], 
        col_label=J.col_labels[j],
        operation_type="interpret", 
        terms={"content": resolved_result.text, "problem": CANONICAL_PROBLEM},
        matrix="F",
        i=i,
        j=j
    )
    
    # Perform universal 3-step lensing process
    column_result, row_result, final_result = _perform_three_step_lensing(
        resolved_result.text, lensing_context, resolver, tracer
    )

    cell = Cell(
        row=i,
        col=j,
        value=final_result.text,
        provenance=create_provenance(
            operation="compute_F",
            coordinates=f"({J.row_labels[i]}, {J.col_labels[j]})",
            stage_data={
                "stage_1_construct": {"text": element_pair, "metadata": {}, "terms_used": element_pair.split(" * "), "warnings": []},
                "stage_2_semantic": {"text": resolved_result.text, "metadata": resolved_result.metadata, "terms_used": resolved_result.terms_used, "warnings": resolved_result.warnings},
                "stage_3_column_lensed": {"text": column_result.text, "metadata": column_result.metadata, "terms_used": column_result.terms_used, "warnings": column_result.warnings},
                "stage_4_row_lensed": {"text": row_result.text, "metadata": row_result.metadata, "terms_used": row_result.terms_used, "warnings": row_result.warnings},
                "stage_5_final_synthesis": {"text": final_result.text, "metadata": final_result.metadata, "terms_used": final_result.terms_used, "warnings": final_result.warnings},
            },
            sources=["J", "C"],
            traced=tracer is not None
        )
    )
    
    # Export to Neo4j if exporter is provided
    if exporter:
        exporter.export_cell_computation(cell, lensing_context)
    
    return cell


def compute_cell_D(i: int, j: int, A: Matrix, F: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional['Neo4jWorkingMemoryExporter'] = None) -> Cell:
    """
    Compute D[i,j] using the canonical D formula with fixed problem statement.
    D[i,j] = A[i,j] + "applied to frame the problem;" + F[i,j] + " to resolve the problem."
    
    Stage 1: Apply canonical synthesis formula mechanically
    Stage 2: Universal 3-step ontological lensing (same as C and F)
    
    Args:
        i: Row index
        j: Column index
        A: Axioms matrix (3x4)
        F: Functions matrix (3x4)
        resolver: CellResolver for LLM operations
        valley_summary: Current position in semantic valley
        
    Returns:
        Cell with synthesized solution objective
    """

    # Stage 1: Apply the canonical synthesis formula with fixed problem
    a_cell = A.get_cell(i, j)
    f_cell = F.get_cell(i, j)
    synthesis_statement = f"{a_cell.value} applied to frame the problem; {f_cell.value} to resolve the problem."
    
    # Trace Stage 1 (mechanical synthesis)
    if tracer:
        stage1_context = SemanticContext(
            station_context="Solution Objectives",
            valley_summary=valley_summary,
            row_label=A.row_labels[i],
            col_label=A.col_labels[j],
            operation_type="synthesis",
            terms={"formula": synthesis_statement, "problem": CANONICAL_PROBLEM},
            matrix="D",
            i=i,
            j=j
        )
        tracer.trace_stage("mechanical_synthesis", stage1_context, SimpleResult(
            text=synthesis_statement,
            terms_used=[a_cell.value, f_cell.value, CANONICAL_PROBLEM],
            warnings=[]
        ), {
            "station": "Solution Objectives", 
            "valley_summary": valley_summary,
            "products": [synthesis_statement]
        })

    # Stage 2: Universal 3-step ontological lensing (same as C and F)
    lensing_context = SemanticContext(
        station_context="Solution Objectives", 
        valley_summary=valley_summary,
        row_label=A.row_labels[i], 
        col_label=A.col_labels[j],  # Note: using A's column labels for D
        operation_type="interpret",
        terms={"content": synthesis_statement, "problem": CANONICAL_PROBLEM},
        matrix="D",
        i=i,
        j=j
    )
    
    # Perform universal 3-step lensing process
    column_result, row_result, final_result = _perform_three_step_lensing(
        synthesis_statement, lensing_context, resolver, tracer
    )

    cell = Cell(
        row=i,
        col=j,
        value=final_result.text,
        provenance=create_provenance(
            operation="compute_D",
            coordinates=f"({A.row_labels[i]}, {A.col_labels[j]})",
            stage_data={
                "stage_1_construct": {"text": f"A[{i},{j}] + F[{i},{j}]", "metadata": {}, "terms_used": [a_cell.value, f_cell.value], "warnings": []},
                "stage_2_semantic": {"text": synthesis_statement, "metadata": {}, "terms_used": [a_cell.value, f_cell.value], "warnings": []},
                "stage_3_column_lensed": {"text": column_result.text, "metadata": column_result.metadata, "terms_used": column_result.terms_used, "warnings": column_result.warnings},
                "stage_4_row_lensed": {"text": row_result.text, "metadata": row_result.metadata, "terms_used": row_result.terms_used, "warnings": row_result.warnings},
                "stage_5_final_synthesis": {"text": final_result.text, "metadata": final_result.metadata, "terms_used": final_result.terms_used, "warnings": final_result.warnings},
            },
            sources=["A", "F"],
            traced=tracer is not None,
            problem=CANONICAL_PROBLEM
        )
    )

    # Export to Neo4j if exporter is provided
    if exporter:
        exporter.export_cell_computation(cell, lensing_context)

    return cell


def compute_matrix_C(A: Matrix, B: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional['Neo4jWorkingMemoryExporter'] = None) -> Matrix:
    """
    Convenience wrapper - loops over compute_cell_C. NO semantic logic here.
    
    Simple iteration over the 3x4 result matrix, calling compute_cell_C for each position.
    This follows the "semantic calculator" principle: matrix operations are just
    organized collections of cell operations.
    """
    cells = []
    for i in range(3):  # A is 3x4
        row_cells = []
        for j in range(4):  # B is 4x4, so result is 3x4
            cell = compute_cell_C(i, j, A, B, resolver, valley_summary, tracer, exporter)
            row_cells.append(cell)
        cells.append(row_cells)

    return Matrix(
        name="C",
        station="Problem Requirements",
        row_labels=A.row_labels,
        col_labels=B.col_labels,
        cells=cells
    )


def compute_matrix_F(J: Matrix, C: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional['Neo4jWorkingMemoryExporter'] = None) -> Matrix:
    """Convenience wrapper - loops over compute_cell_F"""
    cells = []
    for i in range(3):  # Both J and C are 3x4
        row_cells = []
        for j in range(4):
            cell = compute_cell_F(i, j, J, C, resolver, valley_summary, tracer, exporter)
            row_cells.append(cell)
        cells.append(row_cells)

    return Matrix(
        name="F",
        station="Solution Objectives",
        row_labels=J.row_labels,
        col_labels=J.col_labels,
        cells=cells
    )


def compute_matrix_D(A: Matrix, F: Matrix, resolver: CellResolver, valley_summary: str, tracer: Optional[JSONLTracer] = None, exporter: Optional[Neo4jWorkingMemoryExporter] = None) -> Matrix:
    """Convenience wrapper - loops over compute_cell_D with canonical problem"""
    cells = []
    for i in range(3):
        row_cells = []
        for j in range(4):
            cell = compute_cell_D(i, j, A, F, resolver, valley_summary, tracer, exporter)
            row_cells.append(cell)
        cells.append(row_cells)

    return Matrix(
        name="D",
        station="Solution Objectives",
        row_labels=A.row_labels,  # D uses A's row labels
        col_labels=A.col_labels,  # D uses A's col labels
        cells=cells
    )
