"""
Neo4j Exporter for Chirality Framework "Working Memory".

This module is responsible for persisting the entire semantic journey for each
cell computation to a Neo4j graph database. It captures the final matrices,
the individual cells, and all the intermediate stages of the 3-stage
interpretation pipeline, creating a rich, queryable graph of the process.
"""

import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from ..core.types import Cell
from ..core.context import SemanticContext

try:
    from neo4j import GraphDatabase, Driver
except ImportError:
    GraphDatabase = None
    Driver = None

class Neo4jWorkingMemoryExporter:
    """Writes the output of cell computations to Neo4j.

    This class implements the logic to map the 3-stage pipeline results
    into a graph structure, connecting matrices, cells, and provenance.
    
    Supports context manager protocol for proper resource management.
    """

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        if GraphDatabase is None:
            raise ImportError("The 'neo4j' package is required to use the Neo4j exporter. Please install it with `pip install neo4j`.")

        uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = user or os.getenv("NEO4J_USER", "neo4j")
        password = password or os.getenv("NEO4J_PASSWORD", "password")

        self.driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        self.logger = logging.getLogger(__name__)
        self._ensure_schema()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures driver is closed."""
        self.close()
        return False

    def _ensure_schema(self):
        """Ensures necessary constraints are created in the database."""
        try:
            with self.driver.session() as session:
                # Constraint for Matrices to ensure they are unique by name
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (m:Matrix) REQUIRE m.name IS UNIQUE")
                # Constraint for Cells to ensure they are unique
                session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (c:Cell) REQUIRE c.id IS UNIQUE")
                # Index for faster stage lookups
                session.run("CREATE INDEX IF NOT EXISTS FOR (s:Stage) ON (s.timestamp)")
        except Exception as e:
            self.logger.warning(f"Failed to create Neo4j schema: {e}")

    def export_cell_computation(self, cell: Cell, context: SemanticContext):
        """Exports the complete journey of a single cell computation.

        Creates a batched graph representation of the canonical provenance:
        - Matrix node with station context
        - Cell node with coordinates and final value
        - Stage nodes with complete provenance metadata including timestamps
        
        Uses single transaction for efficiency and consistency.
        """
        try:
            with self.driver.session() as session:
                with session.begin_transaction() as tx:
                    cell_id = f"{context.matrix}-{cell.row}-{cell.col}"
                    provenance = cell.provenance
                    
                    # 1. Create matrix and cell nodes
                    tx.run("""
                        MERGE (m:Matrix {name: $matrix_name}) 
                        SET m.station = $station
                        
                        MERGE (c:Cell {id: $cell_id})
                        SET 
                            c.row = $row,
                            c.col = $col,
                            c.value = $value,
                            c.row_label = $row_label,
                            c.col_label = $col_label,
                            c.operation = $operation,
                            c.coordinates = $coordinates,
                            c.sources = $sources,
                            c.timestamp = $cell_timestamp
                        MERGE (m)-[:CONTAINS]->(c)
                        """,
                        matrix_name=context.matrix,
                        station=context.station_context,
                        cell_id=cell_id,
                        row=cell.row,
                        col=cell.col,
                        value=cell.value,
                        row_label=context.row_label,
                        col_label=context.col_label,
                        operation=provenance["operation"],
                        coordinates=provenance["coordinates"],
                        sources=provenance["sources"],
                        cell_timestamp=provenance["timestamp"]
                    )
                    
                    # 2. Create stage nodes based on operation type
                    operation = provenance["operation"]
                    stage_timestamp = datetime.now(timezone.utc).isoformat()
                    
                    if operation == "compute_C":
                        self._export_compute_c_stages(tx, cell_id, provenance, stage_timestamp)
                    elif operation == "compute_F":
                        self._export_compute_f_stages(tx, cell_id, provenance, stage_timestamp)
                    elif operation == "synthesize_D":
                        self._export_synthesize_d_stages(tx, cell_id, provenance, stage_timestamp)
                    
        except Exception as e:
            self.logger.error(f"Failed to export cell {cell_id} to Neo4j: {e}")
            # Don't re-raise - export failure shouldn't break computation
    
    def _export_compute_c_stages(self, tx, cell_id: str, provenance: Dict[str, Any], timestamp: str):
        """Export stages for compute_C operation (3 stages)."""
        # Stage 1: Combinatorial (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Combinatorial {
                products: $products,
                timestamp: $timestamp,
                operation: "compute_C"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, products=provenance["stage_1_products"], timestamp=timestamp)
        
        # Stage 2: Semantic (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Semantic {
                concepts: $concepts,
                timestamp: $timestamp,
                operation: "compute_C"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, concepts=provenance["stage_2_resolved"], timestamp=timestamp)
        
        # Stage 3: Lensed (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Lensed {
                meaning: $meaning,
                timestamp: $timestamp,
                operation: "compute_C"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, meaning=provenance["stage_3_lensed"], timestamp=timestamp)
    
    def _export_compute_f_stages(self, tx, cell_id: str, provenance: Dict[str, Any], timestamp: str):
        """Export stages for compute_F operation (3 stages)."""
        # Stage 1: ElementWise (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:ElementWise {
                element_pair: $element_pair,
                timestamp: $timestamp,
                operation: "compute_F"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, element_pair=provenance["stage_1_element_wise"], timestamp=timestamp)
        
        # Stage 2: Semantic (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Semantic {
                concepts: $concepts,
                timestamp: $timestamp,
                operation: "compute_F"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, concepts=provenance["stage_2_resolved"], timestamp=timestamp)
        
        # Stage 3: Lensed (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Lensed {
                meaning: $meaning,
                timestamp: $timestamp,
                operation: "compute_F"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, meaning=provenance["stage_3_lensed"], timestamp=timestamp)
    
    def _export_synthesize_d_stages(self, tx, cell_id: str, provenance: Dict[str, Any], timestamp: str):
        """Export stages for synthesize_D operation (2 stages)."""
        # Stage 1: Synthesis (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Synthesis {
                synthesis_statement: $synthesis,
                problem: $problem,
                timestamp: $timestamp,
                operation: "synthesize_D"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, synthesis=provenance["stage_1_synthesis"], 
               problem=provenance["problem"], timestamp=timestamp)
        
        # Stage 2: Lensed (always present)
        tx.run("""
            MATCH (c:Cell {id: $cell_id})
            CREATE (s:Stage:Lensed {
                meaning: $meaning,
                timestamp: $timestamp,
                operation: "synthesize_D"
            })
            CREATE (c)-[:HAS_STAGE]->(s)
            """, cell_id=cell_id, meaning=provenance["stage_2_lensed"], timestamp=timestamp)

    def close(self):
        """Closes the database connection."""
        try:
            if self.driver:
                self.driver.close()
                self.driver = None
        except Exception as e:
            self.logger.error(f"Error closing Neo4j driver: {e}")
    
    def __del__(self):
        """Cleanup on garbage collection."""
        self.close()
