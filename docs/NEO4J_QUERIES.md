# Neo4j Query Cookbook

This document provides a set of practical Cypher queries to explore and analyze the "working memory" of the Chirality Framework stored in the Neo4j database. The graph is created by the `Neo4jWorkingMemoryExporter` when you use the `--neo4j-export` flag. Each CLI invocation generates a unique `run_id` so results are scoped to a specific `(:Run)`.

## The Graph Schema

The graph model is universal (applies to all matrices) and designed for traceability:

* **Nodes:**
  * `(:Run {id, startedAt, …})`: One per export session.
  * `(:Matrix {name, station, valley_summary})`: Represents a matrix like C, F, or D.
  * `(:Cell {id, row, col, value, row_label, col_label, operation, coordinates, timestamp})`: A single computed cell (stable id like `C-0-1`).
  * `(:Stage:Construct|:Semantic|:ColumnLensed|:RowLensed|:FinalSynthesis {…})`: Pipeline stages with rich content (`text`/`texts`, `terms_used`, `warnings`) and metadata (`modelId`, `latencyMs`, `promptHash`, `createdAt`, `phase`), plus duplicated context (`station`, `valley_summary`, `row_label`, `col_label`).

* **Relationships:**
  * `(:Run)-[:CONTAINS]->(:Cell)` and `(:Run)-[:CONTAINS]->(:Stage)`
  * `(:Matrix)-[:CONTAINS]->(:Cell)`
  * `(:Cell)-[:HAS_STAGE {order}]->(:Stage)`

---

## Query Recipes

### 1. Find a Specific Cell

**Question:** How do I find the final computed value for cell D(2,1) in a specific run?

```cypher
MATCH (r:Run {id: 'cli-20250831-abc123'})-[:CONTAINS]->(c:Cell {id: 'D-2-1'})
RETURN c.value, c.row_label, c.col_label
```

### 2. Trace the Full History of a Single Cell

**Question:** How was the final value for cell C(0,0) created? Show me the universal five stages for a given run.

```cypher
MATCH (r:Run {id: 'cli-20250831-abc123'})-[:CONTAINS]->(:Cell {id: 'C-0-0'})-[:HAS_STAGE]->(s:Stage)
RETURN s.kind, s.order, coalesce(s.texts, s.text) AS content, s.modelId, s.latencyMs
ORDER BY s.order
```
*This will return the `:Construct`, `:Semantic`, `:ColumnLensed`, `:RowLensed`, and `:FinalSynthesis` stages with their content and metadata.* 

### 3. See All Cells in a Matrix

**Question:** Show me the final values for all cells in Matrix F.

```cypher
MATCH (m:Matrix {name: 'F'})-[:CONTAINS]->(c:Cell)
RETURN c.row, c.col, c.value
ORDER BY c.row, c.col
```

### 4. Find Cells with Specific Provenance

**Question:** Find all cells where the semantic resolution (Stage 2) included the concept "Guiding Imperatives".

```cypher
MATCH (s:Stage:Semantic)
WHERE (s.texts IS NOT NULL AND 'Guiding Imperatives' IN s.texts)
   OR (s.text  IS NOT NULL AND s.text CONTAINS 'Guiding Imperatives')
MATCH (c:Cell)-[:HAS_STAGE]->(s)
RETURN c.id, c.value
```

### 5. Analyze the Raw Inputs for a Cell

**Question:** What were the raw, mechanical products generated for cell C(1,2) before any LLM calls (in a given run)?

```cypher
MATCH (r:Run {id: 'cli-20250831-abc123'})-[:CONTAINS]->(:Cell {id: 'C-1-2'})-[:HAS_STAGE]->(s:Construct)
RETURN s.products
```
