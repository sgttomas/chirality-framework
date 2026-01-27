# The Chirality Framework

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work.  The framing of all matrices are as representations of stages of development in knowledge work.

The framework treats words not as labels but as attractors in embedding space. Matrix elements don't define answers—they partition the solution space into regions where answers can emerge. This is **tiling, not covering**: elements partition semantic space without attempting to enumerate all possibilities.

---

## Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.
2. **Seed, don't specify.** Give coordinates, not work instructions. The latent embedding space does the generative work.
3. **Show your work.**  Explicitly write out each step according to the instructions below.

---

## Semantic Operations

### Semantic Multiplication `*`
Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when the meaning of both concepts are combined.

Examples:
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

**Typing rule:** `*` is defined over **single semantic units** (words or phrase).  
If an operand is list-valued, it must first be interpreted with **I(r, c, L)** before any downstream use.

### Semantic Addition `+`
Semantic addition groups terms into a collection. 

### Order of Operations
1. Parentheses
2. `*` left-to-right
3. `+` left-to-right

---

## Interpretation Operator `I(r, c, L)`

### Purpose
`I` coerces a list-valued cell (a collection of contributors) into a **single atomic semantic unit** that:
- is conditioned by the cell’s coordinate axes (**row label r** and **column label c**),
- does **not** explicitly name those axes (axes are latent constraints),
- is compact and non-enumerative,
- will be used in downstream `*` operations.

### Inputs
- `r`: the **row axis term** for the cell (latent constraint)
- `c`: the **column axis term** for the cell (latent constraint)
- `L`: a **collection** of contributor terms (order-insensitive; treat as a set)

### Output
- `u`: a **single semantic unit** (words / phrase; may be sentence-length but should be compact and encapsulate the combined meaning)

### Precise Definition (procedural)
Let `L` be treated as a **set** .  Interpret one cell at a time, following each of these three steps in sequence.  

Show all three steps. Then assemble the matrix from verified cells.

1. **Axis anchor (latent coordinate frame):**  
   For every cell compute:
   `a := r * c`  
   
   The product must be written out for each cell.

2. **Coordinate-conditioned projection of contributors:**  
   For each cell and every contributor `t ∈ L`, compute a projected contributor:  
   `p_t := a * t`  
   
   The projection step must appear explicitly in the working. For each contributor t, the product a * t must be written out.
   
3. **Centroid attractor selection (non-enumerative synthesis):**  
   Choose an atomic unit `u` such that the meaning of `u` is the  **closest stable attractor** to the centroid of the set `{p_t}` . 
   Operationally, produce the **shortest** phrase that best captures the **shared semantic core** of `{p_t}` .

4. **Output constraints (hard):**
   - Output **one** unit only (no lists).
   - **Do not** repeat or enumerate all contributors.
   - **Do not** include the literal axis tokens `r` or `c` (axes are latent).
   - Produce the most integrally complete phrase that captures the intersection of all contributors. 
   - Prioritize semantic density over brevity.
   - Each member of the set {p_t} := {a*t}  must have its semantic result determined before centroid selection occurs. Interpretations that skip this step are invalid.

   
### Example of how to properly perform the I(r,c,L) procedure

#### Step 1
a = r * c = mandate * data = authoritative fact

#### Step 2
L = {t_1, t_2, t_3, t_4}
L = {bounded truth, traced proof, conformance indicator, adherence precision}

Projections:
a * t_1 = p_1 := authoritative fact * bounded truth = "Binding Reality"
a * t_2 = p_2 := authoritative fact * traced proof = "Verified Authority"
a * t_3 = p_3 := authoritative fact * conformance indicator = "Compliance Status"
a * t_4 = p_4 := authoritative fact * adherence precision = "Strict Liability"

#### Step 3
Centroid of {p_1, p_2, p_3, p_4} → u = "Binding Compliance Standard"

### Example of how NOT to perform the I(r,c,L) procedure

L = {bounded truth, traced proof, conformance indicator, adherence precision}
Axis anchor: mandate * data = authoritative fact
Centroid attractor: [jumps straight to output]

---

## Semantic Matrix Operations

### Dot product `·` 
Dot products yield a **collection** of semantic products, not a single term. This collection is **intermediate** and must be interpreted with `I(r,c,L)` before the result becomes a usable matrix.

#### Illustration of semantic dot product operation:
- Construct the intermediate collection:
  `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`
- Then interpret to the atomic cell value:
  `C(i,j) = I(row_i, col_j, L(i,j))`

**Evaluation order note:** `Σ_k` is evaluated in increasing `k`, but treat the resulting contributors as a set.

### Hadamard product `⊙`
`([J] ⊙ [C])(i,j) = J(i,j) * C(i,j)`  
(With `C(i,j)` already interpreted to an atomic unit.)

### transpose / truncate
These are purely structural transforms that preserve cell content but change orientation.  
They operate only on the final version of the matrices.

---

## Canonical Matrices

### Matrix A 
Size: 4×4  
Columns: [normative, operative, descriptive, interpretive] 
Rows: [event, pattern, structure, paradigm] 

| | **normative** | **operative** | **descriptive** | **interpretive** |
|---|---|---|---|---|
| **event** | directive | response | report | interpretation |
| **pattern** | standard | routine | trend | theme |
| **structure** | policy | process | model | explanation |
| **paradigm** | ethos | methodology | worldview | narrative |



### Matrix B 
Size: 4×4  
Columns: [ontology, epistemology, praxeology, axiology]  
Rows: [data, information, knowledge, wisdom]  

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **data** | registry | observation | telemetry | indicator |
| **information** | taxonomy | evidence | procedure | criteria |
| **knowledge** | model | methodology | playbook | rubric |
| **wisdom** | doctrine | warrant | strategy | charter |

---

## Matrix C 

[C] Size: 4×4  
Columns: [ontology, epistemology, praxeology, axiology]  
Rows: [event, pattern, structure, paradigm] 

### Construction
1) Build intermediate collections:
- `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`

2) Interpretation to atomic units:
- `C(i,j) = I(row_i, col_j, L_C(i,j))`
- present the output in markdown table format.

---

## Matrix F 

[F] Size: 4×4  
Columns: [ontology, epistemology, praxeology, axiology] 
Rows: [data, information, knowledge, wisdom]  

### Construction
1) Hadamard:
- `F_raw(i,j) = B(i,j) * C(i,j)`  
  (Where `C(i,j)` is the final form of the matrix)

2) Interpretation to atomic units:
- `F(i,j) = I(row_i, col_j, F_raw(i,j))`
- present the output in markdown table format.

---

## Matrix D 

[D] Size: 4×4  
Columns: [normative, operative, descriptive, interpretive]  
Rows: [event, pattern, structure, paradigm]  

### Construction
1) Create intermediate collection by addition:
- `L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`

2) Interpretation to atomic unit:
- `D(i,j) = I(row_i, col_j, L_D(i,j))`
- present the output in markdown table format.

---

## Matrix K (transpose of D)

[K] Size: 4×4  
Columns: [event, pattern, structure, paradigm] 
Rows: [normative, operative, descriptive, interpretive]  

Construction:
- `K(i,j) = D(j,i)`  

---

## Matrix G (transpose of A)
[G] Size: 4×4  
Columns: [event, pattern, structure, paradigm]  
Rows: [normative, operative, descriptive, interpretive] 

Construction:
- `G(i,j) = A(j,i)`

---

## Matrix T (transpose of B)
[T] Size: 4×4  
Columns: [data, information, knowledge, wisdom]
Rows: [ontology, epistemology, praxeology, axiology] 

Construction:
- `T(i,j) = B(j,i)`

---

## Matrix X 

[X] Size: 4×4  
Columns: [data, information, knowledge, wisdom]
Rows: [normative, operative, descriptive, interpretive]  

### Construction
1) Build intermediate collections:
- `L_X(i,j) = Σ_k (K(i,k) * T(k,j))`  

2) Interpretation to atomic units:
- `X(i,j) = I(row_i, col_j, L_X(i,j))`
- present the output in markdown table format.

--- 

## Matrix E 

[E] Size: 4×4  
Columns: [event, pattern, structure, paradigm]  
Rows: [normative, operative, descriptive, interpretive]  

### Construction
1) Build intermediate collections:
- `L_E(i,j) = Σ_k (G(i,k) * A(k,j))` 

2) Interpretation to atomic units:
- `E(i,j) = I(row_i, col_j, L_E(i,j))`
- present the output in markdown table format.

---

## Summary: What must happen after EVERY list-valued construction

Whenever a cell is produced as a collection (by dot product `·` or addition `+`):
1) Treat contributors as a **set** (order-insensitive).
2) Apply **I(row_axis, col_axis, L)** to cohere to a single semantic unit.
3) Only then feed into downstream operations.

