# The Chirality Framework (Revised: Interpretation Operator)

> This revision adds a **typed interpretation step** that coerces any list-valued cell into a **single semantic unit** *before* lensing and *before* the cell can participate in any downstream operation.

---

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work.

The framework treats words not as labels but as attractors in embedding space. Matrix elements don't define answers—they partition the solution space into regions where answers can emerge. This is **tiling, not covering**: elements partition semantic space without attempting to enumerate all possibilities.

The name **Chirality** reflects the framework’s core insight: meaning has handedness. The same elements, arranged differently, produce non-superimposable structures. Transpose, truncation, and lensing preserve content while changing orientation—like left and right hands sharing the same fingers in mirror arrangement.

---

## Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.
2. **Seed, don't specify.** Give coordinates, not work instructions. The latent embedding space does the generative work.
3. **Separate substrate from surface.** Keep un-lensed computational forms distinct from interpretive overlays.

---

## Two-Track Architecture (Updated)

The framework maintains strict separation between:

### 1) Computational substrate (un-lensed, **interpreted**)
- **May participate** in transformative operations (·, ⊙, +, transpose, truncation).
- **Must be atomic**: each cell is a single semantic unit (word/phrase), not a list.
- Is the **only** form allowed to flow into downstream operations and generation.

### 2) Interpretive overlays (lenses)
- Are terminal: they **do not feed** into further operations.

### Critical update: list-valued intermediates are not allowed to propagate
Some operations (notably dot products and additions) naturally create **list-valued intermediates**. Those intermediates must be **immediately coerced** into atomic units via the interpretation operator **I(r, c, L)** before any downstream use.

---

## Semantic Operations

### Semantic Multiplication `*`
Semantic multiplication combines two **atomic** terms into their semantic intersection—the meaning that emerges when both concepts are held together.

Examples:
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

**Typing rule:** `*` is defined over **atomic semantic units** (word/phrase).  
If an operand is list-valued, it must first be interpreted with **I**.

### Semantic Addition `+`
Semantic addition groups terms into a flat collection. It is used to record multiple contributors before interpretation.

**Note:** The result of `+` is an **intermediate collection**, not a stable cell value.

### Order of Operations
1. Parentheses
2. `*` left-to-right
3. `+` left-to-right

---

## NEW: Interpretation Operator `I(r, c, L)`

### Purpose
`I` coerces a list-valued cell (a collection of contributors) into a **single atomic semantic unit** that:
- is conditioned by the cell’s coordinate axes (**row label r** and **column label c**),
- does **not** explicitly name those axes (axes are latent constraints),
- is compact and non-enumerative,
- can safely participate in downstream `*` operations.

### Inputs
- `r`: the **row axis term** for the cell (latent constraint)
- `c`: the **column axis term** for the cell (latent constraint)
- `L`: a **collection** of contributor terms (order-insensitive; treat as a set)

### Output
- `u`: a **single semantic unit** (word/phrase; may be sentence-length but should be compact)

### Precise Definition (procedural)
Let `L` be treated as a **set** (order-insensitive; duplicates removed).

1. **Axis anchor (latent coordinate frame):**  
   `a := r * c`  
   This is not output; it defines the local semantic frame implied by the axes.

2. **Coordinate-conditioned projection of contributors:**  
   For every contributor `t ∈ L`, compute a projected contributor:  
   `p_t := a * t`  
   (Each contributor is “pulled” into the axis-defined intersection.)

3. **Centroid attractor selection (non-enumerative synthesis):**  
   Choose an atomic unit `u` such that, in embedding space, `u` is the **closest stable attractor** to the centroid of the set `{a} ∪ {p_t : t ∈ L}` **under the constraints imposed by** `a`.  
   Operationally, produce the **shortest** phrase that best captures the **shared semantic core** of all `p_t` while remaining consistent with `a`.

4. **Output constraints (hard):**
   - Output **one** unit only (no lists).
   - **Do not** repeat or enumerate all contributors.
   - **Do not** include the literal axis tokens `r` or `c` (axes are latent).
   - **Do not** include lens names.
   - Prefer a compact **noun phrase** (target 2–9 words) unless unavoidable.

### Identity case
If the cell is already atomic (`L` is a single unit), then:
- `I(r, c, L) = L`

---

## Semantic Matrix Operations

### Dot product `·` (list-valued intermediate + interpretation)
Dot products yield a **collection** of semantic products, not a single term. This collection is **intermediate** and must be interpreted with `I` before the result becomes a usable matrix.

For matrices with compatible inner dimension `p`:
- Construct the intermediate collection:
  `L(i,j) = Σ_k (A(i,k) * B(k,j))`
- Then interpret to the atomic cell value:
  `C(i,j) = I(row_i, col_j, L(i,j))`

**Evaluation order note:** `Σ_k` is evaluated in increasing `k` for deterministic construction, but **interpretation is order-insensitive** (treat the resulting contributors as a set).

### Hadamard product `⊙`
`([J] ⊙ [C])(i,j) = J(i,j) * C(i,j)`  
(With `C(i,j)` already interpreted to an atomic unit.)

### transpose / truncate
These are purely structural transforms that preserve cell content but change orientation.  
They operate only on the **un-lensed interpreted** matrices.

---

## Canonical Matrices

### Matrix A (Activity structure)
Size: 3×4  
Columns: [guiding, applying, judging, reflecting]  
Rows: [normative, operative, descriptive]

|            | guiding    | applying      | judging    | reflecting    |
|------------|------------|---------------|------------|---------------|
| **normative**  | principle | conduct | evaluation | integrity |
| **operative**  | procedure | methods | criteria | adaptation |
| **descriptive**| observation | documentation | assessment | understanding |

### Matrix B (Knowledge structure)
Size: 4×4  
Columns: [ontology, epistemology, axiology, praxeology]  
Rows: [data, information, knowledge, wisdom]

|               | ontology     | epistemology | axiology       | praxeology |
|---------------|--------------|--------------|----------------|-----------|
| **data**      | fact | evidence | significance | signal |
| **information** | taxonomy | provenance | relevance | protocol |
| **knowledge** | architecture | framework | interpretation | principle |
| **wisdom**    | ground | insight | purpose | measure |

---

## Matrix C (Formulation)

[C] Size: 3×4  
Columns: [ontology, epistemology, axiology, praxeology]  
Rows: [normative, operative, descriptive]

### Construction
1) Build intermediate collections:
- `L_C(i,j) = Σ_k (A(i,k) * B(k,j))`

2) Interpret to atomic units (un-lensed computational C):
- `C(i,j) = I(row_i, col_j, L_C(i,j))`

3) Lens (terminal overlay):
- Lens name: **Formulation**
- Lensed C is interpretive and terminal.

---

## Matrix J (truncate B)
[J] Size: 3×4  
Rows: [data, information, knowledge]  
Columns: [ontology, epistemology, axiology, praxeology]

Construction: remove the final row (wisdom) from B.

---

## Matrix F (Requirements)

[F] Size: 3×4  
Rows: [normative, operative, descriptive]  
Columns: [ontology, epistemology, axiology, praxeology]

### Construction
1) Hadamard:
- `F_raw(i,j) = J(i,j) * C(i,j)`  
  (Where `C(i,j)` is **un-lensed interpreted**.)

2) Interpretation (identity unless your `*` produces non-atomic output):
- `F(i,j) = I(row_i, col_j, F_raw(i,j))`

3) Lens (terminal overlay):
- Lens name: **Requirements**

---

## Matrix D (Objectives)

[D] Size: 3×4  
Rows: [normative, operative, descriptive]  
Columns: [guiding, applying, judging, reflecting]

### Construction
1) Create intermediate collection by addition:
- `L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`

2) Interpret to atomic unit:
- `D(i,j) = I(row_i, col_j, L_D(i,j))`

3) Lens (terminal overlay):
- Lens name: **Objectives**

---

## Matrix K (transpose of un-lensed interpreted D)

[K] Size: 4×3  
Rows: [guiding, applying, judging, reflecting]  
Columns: [normative, operative, descriptive]

Construction:
- `K(i,j) = D(j,i)`  
**Critical:** K must use the **un-lensed interpreted** D (not lensed D).

---

## Matrix X (Verification)

[X] Size: 4×4  
Rows: [guiding, applying, judging, reflecting]  
Columns: [ontology, epistemology, axiology, praxeology]

### Construction
1) Intermediate collections:
- `L_X(i,j) = Σ_k (K(i,k) * J(k,j))`  with k over [normative, operative, descriptive]

2) Interpret:
- `X(i,j) = I(row_i, col_j, L_X(i,j))`

3) Lens (terminal overlay):
- Lens name: **Verification**

---

## Matrix G (truncate X)
[G] Size: 3×4  
Rows: [guiding, applying, judging]  
Columns: [ontology, epistemology, axiology, praxeology]

Construction: retain rows [guiding, applying, judging] from **un-lensed interpreted** X; drop [reflecting].

---

## Matrix T (transpose of J)
[T] Size: 4×3  
Rows: [ontology, epistemology, axiology, praxeology]  
Columns: [data, information, knowledge]

Construction:
- `T(i,j) = J(j,i)`

---

## Matrix E (Evaluation)

[E] Size: 3×3  
Rows: [guiding, applying, judging]  
Columns: [data, information, knowledge]

### Construction
1) Intermediate collections:
- `L_E(i,j) = Σ_k (G(i,k) * T(k,j))` with k over [ontology, epistemology, axiology, praxeology]

2) Interpret:
- `E(i,j) = I(row_i, col_j, L_E(i,j))`

3) Lens (terminal overlay):
- Lens name: **Evaluation**

---

## Summary: What must happen after EVERY list-valued construction

Whenever a cell is produced as a collection (by dot product `·` or addition `+`):
1) Treat contributors as a **set** (order-insensitive).
2) Apply **I(row_axis, col_axis, L)** to cohere to a single unit.
3) Only then:
   - feed into downstream operations (un-lensed interpreted), and/or
   - apply the matrix’s lens (terminal overlay).

