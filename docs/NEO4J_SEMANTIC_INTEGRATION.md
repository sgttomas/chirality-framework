# Neo4j Integration: The Framework's Working Memory

**Status:** Implemented for core pipeline (Matrices C, F, D) with universal 5‑stage schema and Run scoping

## 1. Purpose: A Queryable Record of the Semantic Journey

The Neo4j integration serves as the **working memory** for the Chirality Framework. It is not simply an export destination; it is a rich, queryable graph representation of the entire semantic generation process.

For every cell computed, the system records:
* The final `Cell` and its parent `Matrix`.
* The complete `provenance` of the cell, including the inputs and outputs of each step in the **Three‑Stage Interpretation Pipeline** (universal five-stage model).
* The relationships between all these entities, scoped to a unique `Run` node.

This allows developers and researchers to trace the full lineage of any generated concept and provides a powerful backend for visualization and analysis tools.

## 2. Workflow: How to Use the Exporter

The Neo4j export functionality is integrated directly into the `compute-cell` CLI command via a flag.

*   **Command:** `python -m chirality.cli compute-cell <MATRIX> [OPTIONS]`
*   **Flag:** `--neo4j-export`

When you run a computation with this flag, the `Neo4jWorkingMemoryExporter` is activated. After each cell is successfully computed, its entire history is written to the database in real-time. The CLI auto-generates a unique `run_id` per invocation and prints it so you can filter or compare results by run.

### Example Usage

```bash
# Ensure your Neo4j credentials are set in your .env file
# NEO4J_URI="bolt://localhost:7687"
# NEO4J_USER="neo4j"
# NEO4J_PASSWORD="your_password"

# Compute cell C(0,1) and write its full provenance to Neo4j
python -m chirality.cli compute-cell C --i 0 --j 1 --resolver openai --neo4j-export
```

## 3. Graph Schema

The exporter builds a universal, intuitive graph model:

* **Nodes:**
  * `(:Run {id, startedAt, …})`: Represents a single export session.
  * `(:Matrix {name, station, valley_summary})`: Represents a matrix like C, F, or D.
  * `(:Cell {id, row, col, value, row_label, col_label, operation, coordinates, timestamp})`: Represents a single cell (`id` is a stable composite key like `C-0-1`).
  * `(:Stage:Construct|:Semantic|:ColumnLensed|:RowLensed|:FinalSynthesis {…})`: One per stage, with rich content and metadata (text/texts, terms_used, warnings, modelId, latencyMs, promptHash, createdAt, phase), plus duplicated context (station, valley_summary, row_label, col_label).

* **Relationships:**
  * `(:Run)-[:CONTAINS]->(:Cell)` and `(:Run)-[:CONTAINS]->(:Stage)`
  * `(:Matrix)-[:CONTAINS]->(:Cell)`
  * `(:Cell)-[:HAS_STAGE {order}]->(:Stage)`

### Example Cypher Query

How was the final meaning for cell C(0,1) derived in a specific run?

```cypher
MATCH (r:Run {id: 'cli-20250831-abc123'})-[:CONTAINS]->(:Cell {id: 'C-0-1'})-[:HAS_STAGE]->(s)
RETURN s
ORDER BY s.order
```



This query would return the three `:Stage` nodes associated with that cell, showing the progression from raw products to resolved concepts to the final lensed meaning.
