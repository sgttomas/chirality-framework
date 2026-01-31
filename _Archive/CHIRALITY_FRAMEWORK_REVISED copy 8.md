
# The Chirality Framework

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work. 

The framework treats words not as labels but as attractors in embedding space. Matrix elements don't define answers—they partition the solution space into regions where answers can emerge. This is "tiling, not covering": elements partition semantic space without attempting to enumerate all possibilities.

The name "Chirality" reflects the framework's core insight: meaning has handedness. The same elements, arranged differently, produce non-superimposable structures. Transpose, truncation, and lensing all preserve content while changing orientation—like left and right hands sharing the same fingers in mirror arrangement.

## Your Role as the LLM within the Chirality Framework

You follow instructions for construction, interpretation, and lensing of elements of semantic components.

### Principles

1. **Tile, don't cover.** Elements are attractors, not definitions. They partition semantic space into regions without attempting exhaustive specification.

2. **Seed, don't specify.** Create semantic coordinates, not work instructions or commands. 

3. **Separate substrate from surface.** Keep un-lensed matrices for computation.

---

## Semantic Operations

### Semantic Multiplication " * "

Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when both concepts are held together.

Examples:
- "sufficient" * "reason" = "justification"
- "necessary" * "condition" = "prerequisite"
- "practical" * "knowledge" = "skill"

The product is not a concatenation but a synthesis. It answers: "What concept lives at the intersection of these two meanings?"

### Semantic Addition " + "

Semantic addition groups terms into an ordered list.  The result is always a single flat ordered list.

Examples:
- "grounding" + "facts" = "[grounding, facts]"
- "adaptive" + "methods" = "[adaptive, methods]"

### Order of Operations

When combining multiple terms:

1. Evaluate within parentheses first 
2. Evaluate multiplications first, left to right
3. Then evaluate additions, left to right

Example:
```
"practical" * "knowledge" + "theoretical" * "understanding"
= "skill" + "comprehension"
= "[skill, comprehension]"
```

### Semantic Matrix Operations

- "·" = dot product (ordered fold of * then +)
- "⊙" = Hadamard product (**matrix-level**). Defined by: `([J] ⊙ [C])(i,j) = J(i,j) * C(i,j)`
- transpose = swap rows for columns, retaining ordering
- truncate = remove rows or columns

#### Semantic Dot Product

**Rule:** Whenever `Σₖ` appears, it is evaluated **in increasing k order** (left-to-right).  
Do **not** reorder, regroup, commute, or simplify the resulting sequence of terms.

#### Dot Product Definition

Dot products yield an ordered list of semantic products, not a single synthesized term.

For matrices with compatible inner dimension `p`, the semantic dot product is:

C(i,j) = Σₖ (A(i,k) * B(k,j))    (evaluate in k order; do not reorder)

#### Example Expansion (p = 4)

C(i,j) =
(A(i,1) * B(1,j)) +
(A(i,2) * B(2,j)) +
(A(i,3) * B(3,j)) +
(A(i,4) * B(4,j))

Evaluate left-to-right in the k sequence shown above.

Do not reorder or regroup these terms.

---

## Two-Track Architecture

The framework maintains strict separation between **un-lensed matrices** (computational substrate) and **lensed matrices** (interpretive overlays).

**Un-lensed matrices (computational substrate):**
- Participate in transformative operations (·, ⊙, +, transpose, truncation)
- Preserve raw semantic content
- Are the **only** version used for generation (before any lensing)

**Lensed matrices:**
- Are terminal—they do not feed into further operations

**The rule:** Every transformative operation works with un-lensed versions, and generation also uses un-lensed versions. Lensing is an interpretive step and must never be fed back into operations. This preserves compositionality.

```
[Unlensed C] ──→ operations ──→ [Unlensed F] ──→ operations ──→ ...
      │                               │
      │ (generation uses un-lensed)     │ (generation uses un-lensed)
      ↓                               ↓
  artifacts / drafts / candidates  artifacts / drafts / candidates

```

---


## Canonical Matrix Definitions

### Matrix A

Matrix A defines the activity structure of knowledge work. It tiles the space of "what kind of activity is being performed" along two dimensions: the mode of engagement (normative, operative, descriptive) and the phase of activity (guiding, applying, judging, reflecting).

```
[A]
Size: 3x4
Column names: [guiding, applying, judging, reflecting]
Row names: [normative, operative, descriptive]
```

|            | guiding    | applying      | judging    | reflecting    |
|------------|------------|---------------|------------|---------------|
| **normative**  | principle | conduct | evaluation | integrity |
| **operative**  | procedure | methods | criteria | adaptation |
| **descriptive**| observation | documentation | assessment | understanding |

### Matrix B

Matrix B defines the knowledge structure across the DIKW hierarchy and the knowledge cycle domains. It tiles the space of "what kind of knowledge entity is being handled."

```
[B]
Size: 4x4
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [data, information, knowledge, wisdom]
```

|               | ontology     | epistemology | axiology       | praxeology |
|---------------|--------------|--------------|----------------|-----------|
| **data**      | fact | evidence | significance | signal |
| **information** | taxonomy | provenance | relevance | protocol |
| **knowledge** | architecture | framework | interpretation | principle |
| **wisdom**    | ground | insight | purpose | measure |

---

## Constructing Matrix C

### Matrix C

```
[C]
Size: 3×4
Lens: Formulation
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [normative, operative, descriptive]
```

**Construction:**

[A] · [B] = [C]

This is the semantic dot product. Each cell C(i,j) is computed by taking row i of Matrix A and column j of Matrix B, performing element-wise semantic multiplication, then semantic addition of the results.

```
for i from 1 to n
for j from 1 to m
do:
C(i,j) = Σₖ (A(i,k) * B(k,j))
```

**Instructions:**

1. For each row i and column j
2. Construct: Σₖ (A(i,k) * B(k,j))
3. Purely mechanical construction no interpretation

**Output:** Generate Matrix C in markdown table format.

---

## Semantic Operations

### Semantic Multiplication " * "

Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when both concepts are held together.

Examples:
- "sufficient" * "reason" = "justification"
- "necessary" * "condition" = "prerequisite"
- "practical" * "knowledge" = "skill"

The product is not a concatenation but a synthesis. It answers: "What concept lives at the intersection of these two meanings?"

### Semantic Addition " + "

Semantic addition groups terms into an ordered list. The result is always a single flat ordered list.

Examples:
- "grounding" + "facts" = "[grounding, facts]"
- "adaptive" + "methods" = "[adaptive, methods]"

### Order of Operations

When combining multiple terms:

1. Evaluate within parentheses first 
2. Evaluate multiplications first, left to right
3. Then evaluate additions, left to right

Example:
```
"practical" * "knowledge" + "theoretical" * "understanding"
= "skill" + "comprehension"
= "[skill, comprehension]"
```

### Semantic Matrix Operations

- "·" = dot product (ordered fold of * then +)
- "⊙" = Hadamard product (**matrix-level**). Defined by: `([J] ⊙ [C])(i,j) = J(i,j) * C(i,j)`
- transpose = swap rows for columns, retaining ordering
- truncate = remove rows or columns

#### Semantic Dot Product

**Rule:** Whenever `Σₖ` appears, it is evaluated **in increasing k order** (left-to-right).  
Do **not** reorder, regroup, commute, or simplify the resulting sequence of terms.

#### Dot Product Definition

Dot products yield an ordered list of semantic products, not a single synthesized term.

For matrices with compatible inner dimension `p`, the semantic dot product is:

C(i,j) = Σₖ (A(i,k) * B(k,j))    (evaluate in k order; do not reorder)

#### Example Expansion (p = 4)

C(i,j) =
(A(i,1) * B(1,j)) +
(A(i,2) * B(2,j)) +
(A(i,3) * B(3,j)) +
(A(i,4) * B(4,j))

Evaluate left-to-right in the k sequence shown above.

Do not reorder or regroup these terms.

---

## Semantically calculating the elements of Matrix C

**Instructions:**

1. For each cell, follow the order of semantic operations and compute the meaning.  
2. Do not leave any semantic operators remaining
3. Do not interpret the meaning of the element as a whole, only compute the semantic operations according to your instructions

---

## Lensing of Matrix C

**Note:** Lensing is an interpretive overlay. It must not be used as input to subsequent operations.

The lens of "Formulation" is the governing context to interpret the contents of the elements.

**Instructions:**

1. Hold the lens "Formulation" as context
2. For each cell, ask: "Viewed as the formulation of a knowledge work task, what does this element point toward?"
3. Generate the lensed Matrix C in markdown table format.

---

## Constructing Matrix J

### Matrix J

```
[J]
Size: 3×4
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [data, information, knowledge]
```

**Construction:**

Matrix J is a truncated form of Matrix B. Remove the final row (wisdom).

**Output:** Generate Matrix J (this is simply Matrix B without the wisdom row) in markdown table format.

---

## Constructing Matrix F

### Matrix F

```
[F]
Size: 3×4
Lens: Requirements
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [normative, operative, descriptive]
```

**Construction:**

[J] ⊙ [C] = [F]

This is the semantic Hadamard product (element-wise multiplication).

```
for i from 1 to n
for j from 1 to m
do:
F(i,j) = J(i,j) * C(i,j)
```

**Instructions:**

1. For each row i and column j
2. Construct: J(i,j) * C(i,j)
3. Purely mechanical construction no interpretation

**Output:** Generate Matrix F in markdown table format.

---

## Semantically calculating the elements of Matrix F

**Instructions:**

1. For each cell, follow the order of semantic operations and compute the meaning.
2. Do not leave any semantic operators remaining
3. Do not interpret the meaning of the element as a whole, only compute the semantic operations according to your instructions

---

## Lensing of Matrix F

**Note:** Lensing is an interpretive overlay. It must not be used as input to subsequent operations.


The lens "Requirements" acts as a singular contextual lens.

**Instructions:**

1. Hold the lens name "Requirements" as context
2. For each cell, ask: "In what sense does this element represent requirements of knowledge work?"
3. Generate the lensed Matrix F in markdown table format.

---

## Constructing Matrix D

### Matrix D

```
[D]
Size: 3×4
Lens: Objectives
Column names: [guiding, applying, judging, reflecting]
Row names: [normative, operative, descriptive]
```

**Construction:**

```
for i from 1 to n
for j from 1 to m
do:
D(i,j) = A(i,j) + ("resolution" * F(i,j))
```

**Instructions:**

1. For each row i and column j
2. Construct: A(i,j) + ("resolution" * F(i,j))
3. Purely mechanical construction no interpretation

**Output:** Generate Matrix D in markdown table format.

---


## Semantically calculating the elements of Matrix D

**Instructions:**

1. For each cell, follow the order of semantic operations and compute the meaning.
2. Do not leave any semantic operators remaining
3. Do not interpret the meaning of the element as a whole, only compute the semantic operations according to your instructions

---

## Lensing of Matrix D

**Note:** Lensing is an interpretive overlay. It must not be used as input to subsequent operations.

The lens "Objectives" acts as a singular contextual lens.

**Instructions:**

1. Hold the lens name "Objectives" as context
2. For each cell, ask: "In what sense does this element represent objectives of knowledge work?"
3. Generate the lensed Matrix D in markdown table format.

---

## Constructing Matrix K

### Matrix K

```
[K]
Size: 4×3
Column names: [normative, operative, descriptive]
Row names: [guiding, applying, judging, reflecting]
```

**Construction:**

Matrix K is the transpose of **un-lensed** Matrix D.

```
for i from 1 to n
for j from 1 to m
do:
K(i,j) = D(j,i)
```

Rows become columns. Columns become rows. The content is preserved; the orientation changes.

**Critical:** K must use the un-lensed D. If lensed D were used, the lens-specific interpretation would propagate into K and contaminate all downstream matrices.

**Instructions:**

1. Take un-lensed Matrix D
2. Swap rows and columns

**Output:** Generate Matrix K in markdown table format.

---

## Constructing Matrix X

### Matrix X

```
[X]
Size: 4×4
Lens: Verification
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [guiding, applying, judging, reflecting]
```

**Construction:**

[K] · [J] = [X]

This is the semantic dot product of Matrix K (4×3) with Matrix J (3×4).

```
for i from 1 to n
for j from 1 to m
do:
X(i,j) = Σₖ (K(i,k) * J(k,j))
```

Each cell is the sum of three semantic products.

**Instructions:**

1. For each row i and column j
2. Construct: Σₖ (K(i,k) * J(k,j))
3. Purely mechanical construction no interpretation

**Output:** Generate Matrix X in markdown table format.

---

## Semantically calculating the elements of Matrix X

**Instructions:**

1. For each cell, follow the order of semantic operations and compute the meaning.
2. Do not leave any semantic operators remaining
3. Do not interpret the meaning of the element as a whole, only compute the semantic operations according to your instructions

---

## Lensing of Matrix X

**Note:** Lensing is an interpretive overlay. It must not be used as input to subsequent operations.

The lens "Verification" acts as a singular contextual lens.

**Instructions:**

1. Hold the lens name "Verification" as context
2. For each cell, ask: "In what sense does this element represent verification of knowledge work?"
3. Generate the lensed Matrix X in markdown table format.

---

## Constructing Matrix G

### Matrix G

```
[G]
Size: 3×4
Column names: [ontology, epistemology, axiology, praxeology]
Row names: [guiding, applying, judging]
```

**Construction:**

To construct [G], use only the top three rows of **un-lensed** [X]. 

**Output:** Generate Matrix G in markdown table format.

---

## Constructing Matrix T

### Matrix T

```
[T]
Size: 4×3
Column names: [data, information, knowledge]
Row names: [ontology, epistemology, axiology, praxeology]
```

**Construction:**

Matrix T is the transpose of Matrix J.

```
for i from 1 to n
for j from 1 to m
do:
T(i,j) = J(j,i)
```

**Output:** Generate Matrix T in markdown table format.

---

## Constructing Matrix E

### Matrix E

```
[E]
Size: 3×3
Lens: Evaluation
Column names: [data, information, knowledge]
Row names: [guiding, applying, judging]
```

**Construction:**

[G] · [T] = [E]

This is the semantic dot product of Matrix G (3×4) with Matrix T (4×3).

```
for i from 1 to n
for j from 1 to m
do:
E(i,j) = Σₖ (G(i,k) * T(k,j))
```

**Instructions:**

1. For each row i and column j
2. Construct: Σₖ (G(i,k) * T(k,j))
3. Purely mechanical construction no interpretation

**Output:** Generate Matrix E in markdown table format.

---

## Semantically calculating the elements of Matrix E

**Instructions:**

1. For each cell, follow the order of semantic operations and compute the meaning.
2. Do not leave any semantic operators remaining
3. Do not interpret the meaning of the element as a whole, only compute the semantic operations according to your instructions

---

## Lensing of Matrix E

**Note:** Lensing is an interpretive overlay. It must not be used as input to subsequent operations.

The lens "Evaluation" acts as a singular contextual lens.

**Instructions:**

1. Hold the lens name "Evaluation" as context
2. For each cell, ask: "In what sense does this element represent evaluation of knowledge work?"
3. Generate the lensed Matrix E in markdown table format.

---

## Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.

2. **Seed, don't specify.** Give coordinates, not commands. The latent embedding space does the generative work.

3. **Separate substrate from surface.** Keep un-lensed matrices for computation.

---