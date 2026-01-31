# The Chirality Framework

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work.

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
- `L`: a **lens** given by the label for that Matrix (will be one of: formulation, requirements, objectives, verification, evaluation)

### Output
- `u`: a **single semantic unit** (words / phrase; may be sentence-length but should be compact and encapsulate the combined meaning)

### Precise Definition (procedural)
Interpret one cell at a time, following each of these three steps in sequence.  

Show the full work for both steps. Then assemble the matrix from cells into a markdown table format.

1. **Axis anchor (latent coordinate frame):**  
   For every cell compute:
   `a := r * c`  
   
   The product must be written out for each cell.
   
2. **Coordinate-conditioned projection of matrix label:**  
   Let the label for that matrix be `L`
   
   For every cell compute: 
   
   `u := L * a`  
   
   For each cell the product `L *a` must be written out.
   
---

##  Transpose / Truncate Operations

These are purely structural transforms that preserve cell content but change orientation.  
They operate only on the **un-lensed interpreted** matrices.

---

## Matrix A (Orientation)

[C] Size: 3×4  
L: orientation
Columns: [event, pattern, structure, paradigm] 
Rows: [normative, operative, descriptive]

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix B (Conceptualization)

[C] Size: 4×4  
L: conceptualization
Columns: [ontology, epistemology, praxeology, axiology]  
Rows: [data, information, knowledge, wisdom]  

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix C (Formulation)

[C] Size: 3×4  
L: formulation
Columns: [ontology, epistemology, praxeology, axiology]  
Rows: [normative, operative, descriptive]

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix J (truncate B)
[J] Size: 3×4  
Rows: [data, information, knowledge]  
Columns: [ontology, epistemology, praxeology, axiology] 

Construction: remove the final row (wisdom) from B.

---

## Matrix F (Requirements)

[F] Size: 3×4  
L: requirements
Rows: [normative, operative, descriptive]  
Columns: [ontology, epistemology, praxeology, axiology] 

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix D (Objectives)

[D] Size: 3×4  
L: objectives
Rows: [normative, operative, descriptive]  
Columns: [mandate, specification, execution, warrant]  

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix K (transpose of D)

[K] Size: 4×3  
Rows: [mandate, specification, execution, warrant]   
Columns: [normative, operative, descriptive]

Construction:
- `K(i,j) = D(j,i)`  

---

## Matrix X (Verification)

[X] Size: 4×4  
L: verification
Rows: [mandate, specification, execution, warrant]   
Columns: [ontology, epistemology, praxeology, axiology] 

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---

## Matrix G (truncate X)
[G] Size: 3×4  
Rows: [mandate, specification, execution]   
Columns: [ontology, epistemology, praxeology, axiology] 

Construction: retain rows [mandate, specification, execution] from X; drop [warrant].

---

## Matrix T (transpose of J)
[T] Size: 4×3  
Rows: [ontology, epistemology, praxeology, axiology] 
Columns: [data, information, knowledge]

Construction:
- `T(i,j) = J(j,i)`

---

## Matrix E (Evaluation)

[E] Size: 3×3  
L: evaluation
Rows: [mandate, specification, execution]  
Columns: [data, information, knowledge]

### Construction
Compute the `u` for each cell individually using the interpretation function I(r,c,L) .  
Output in a single markdown format table.

---


