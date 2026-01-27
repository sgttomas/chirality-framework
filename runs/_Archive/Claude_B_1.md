# Chirality Framework — Complete Matrix Derivations

## What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work.

The framework treats words not as labels but as attractors in embedding space. Matrix elements don't define answers—they partition the solution space into regions where answers can emerge. This is **tiling, not covering**: elements partition semantic space without attempting to enumerate all possibilities.

---

## Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.
2. **Seed, don't specify.** Give coordinates, not work instructions. The latent embedding space does the generative work.
3. **Show your work.** Explicitly write out each step according to the instructions below.

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
- is conditioned by the cell's coordinate axes (**row label r** and **column label c**),
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
   
   For each cell the product `L * a` must be written out.

---

# Matrix C (Formulation) — Full Derivation

**Matrix Parameters:**
- L = formulation
- Rows: [normative, operative, descriptive]
- Columns: [ontology, epistemology, praxeology, axiology]

---

## Step-by-Step Cell Computation

### Row: normative

**Cell (normative, ontology):**
- Step 1: `a := normative * ontology = prescribed being → categorical imperative`
- Step 2: `u := formulation * categorical imperative = definitional axiom`

**Cell (normative, epistemology):**
- Step 1: `a := normative * epistemology = prescribed knowing → validity criterion`
- Step 2: `u := formulation * validity criterion = epistemic principle`

**Cell (normative, praxeology):**
- Step 1: `a := normative * praxeology = prescribed action → duty`
- Step 2: `u := formulation * duty = rule statement`

**Cell (normative, axiology):**
- Step 1: `a := normative * axiology = prescribed value → virtue`
- Step 2: `u := formulation * virtue = value proposition`

---

### Row: operative

**Cell (operative, ontology):**
- Step 1: `a := operative * ontology = functional being → mechanism`
- Step 2: `u := formulation * mechanism = structural schema`

**Cell (operative, epistemology):**
- Step 1: `a := operative * epistemology = functional knowing → method`
- Step 2: `u := formulation * method = procedural specification`

**Cell (operative, praxeology):**
- Step 1: `a := operative * praxeology = functional action → practice`
- Step 2: `u := formulation * practice = operational protocol`

**Cell (operative, axiology):**
- Step 1: `a := operative * axiology = functional value → utility`
- Step 2: `u := formulation * utility = performance metric`

---

### Row: descriptive

**Cell (descriptive, ontology):**
- Step 1: `a := descriptive * ontology = observed being → phenomenon`
- Step 2: `u := formulation * phenomenon = factual description`

**Cell (descriptive, epistemology):**
- Step 1: `a := descriptive * epistemology = observed knowing → finding`
- Step 2: `u := formulation * finding = evidential report`

**Cell (descriptive, praxeology):**
- Step 1: `a := descriptive * praxeology = observed action → behavior`
- Step 2: `u := formulation * behavior = activity account`

**Cell (descriptive, axiology):**
- Step 1: `a := descriptive * axiology = observed value → preference`
- Step 2: `u := formulation * preference = evaluative appraisal`

---

## Matrix C (Assembled)

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **normative** | definitional axiom | epistemic principle | rule statement | value proposition |
| **operative** | structural schema | procedural specification | operational protocol | performance metric |
| **descriptive** | factual description | evidential report | activity account | evaluative appraisal |

---

# Matrix F (Requirements) — Full Derivation

**Matrix Parameters:**
- L = requirements
- Rows: [normative, operative, descriptive]
- Columns: [ontology, epistemology, praxeology, axiology]

---

## Step-by-Step Cell Computation

### Row: normative

**Cell (normative, ontology):**
- Step 1: `a := normative * ontology = prescribed being → categorical imperative`
- Step 2: `u := requirements * categorical imperative = mandatory constraint`

**Cell (normative, epistemology):**
- Step 1: `a := normative * epistemology = prescribed knowing → validity criterion`
- Step 2: `u := requirements * validity criterion = evidentiary standard`

**Cell (normative, praxeology):**
- Step 1: `a := normative * praxeology = prescribed action → duty`
- Step 2: `u := requirements * duty = obligatory procedure`

**Cell (normative, axiology):**
- Step 1: `a := normative * axiology = prescribed value → virtue`
- Step 2: `u := requirements * virtue = quality threshold`

---

### Row: operative

**Cell (operative, ontology):**
- Step 1: `a := operative * ontology = functional being → mechanism`
- Step 2: `u := requirements * mechanism = system dependency`

**Cell (operative, epistemology):**
- Step 1: `a := operative * epistemology = functional knowing → method`
- Step 2: `u := requirements * method = capability specification`

**Cell (operative, praxeology):**
- Step 1: `a := operative * praxeology = functional action → practice`
- Step 2: `u := requirements * practice = process prerequisite`

**Cell (operative, axiology):**
- Step 1: `a := operative * axiology = functional value → utility`
- Step 2: `u := requirements * utility = performance criterion`

---

### Row: descriptive

**Cell (descriptive, ontology):**
- Step 1: `a := descriptive * ontology = observed being → phenomenon`
- Step 2: `u := requirements * phenomenon = situational condition`

**Cell (descriptive, epistemology):**
- Step 1: `a := descriptive * epistemology = observed knowing → finding`
- Step 2: `u := requirements * finding = informational input`

**Cell (descriptive, praxeology):**
- Step 1: `a := descriptive * praxeology = observed action → behavior`
- Step 2: `u := requirements * behavior = operational context`

**Cell (descriptive, axiology):**
- Step 1: `a := descriptive * axiology = observed value → preference`
- Step 2: `u := requirements * preference = acceptance criterion`

---

## Matrix F (Assembled)

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **normative** | mandatory constraint | evidentiary standard | obligatory procedure | quality threshold |
| **operative** | system dependency | capability specification | process prerequisite | performance criterion |
| **descriptive** | situational condition | informational input | operational context | acceptance criterion |

---

# Matrix D (Objectives) — Full Derivation

**Matrix Parameters:**
- L = objectives
- Rows: [normative, operative, descriptive]
- Columns: [mandate, specification, execution, warrant]

---

## Step-by-Step Cell Computation

### Row: normative

**Cell (normative, mandate):**
- Step 1: `a := normative * mandate = prescribed authority → directive`
- Step 2: `u := objectives * directive = governing aim`

**Cell (normative, specification):**
- Step 1: `a := normative * specification = prescribed detail → standard`
- Step 2: `u := objectives * standard = compliance target`

**Cell (normative, execution):**
- Step 1: `a := normative * execution = prescribed enactment → enforcement`
- Step 2: `u := objectives * enforcement = regulatory outcome`

**Cell (normative, warrant):**
- Step 1: `a := normative * warrant = prescribed justification → legitimacy`
- Step 2: `u := objectives * legitimacy = authorization goal`

---

### Row: operative

**Cell (operative, mandate):**
- Step 1: `a := operative * mandate = functional authority → commission`
- Step 2: `u := objectives * commission = mission intent`

**Cell (operative, specification):**
- Step 1: `a := operative * specification = functional detail → blueprint`
- Step 2: `u := objectives * blueprint = design target`

**Cell (operative, execution):**
- Step 1: `a := operative * execution = functional enactment → implementation`
- Step 2: `u := objectives * implementation = delivery milestone`

**Cell (operative, warrant):**
- Step 1: `a := operative * warrant = functional justification → rationale`
- Step 2: `u := objectives * rationale = viability benchmark`

---

### Row: descriptive

**Cell (descriptive, mandate):**
- Step 1: `a := descriptive * mandate = observed authority → charter`
- Step 2: `u := objectives * charter = scope definition`

**Cell (descriptive, specification):**
- Step 1: `a := descriptive * specification = observed detail → documentation`
- Step 2: `u := objectives * documentation = clarity goal`

**Cell (descriptive, execution):**
- Step 1: `a := descriptive * execution = observed enactment → performance`
- Step 2: `u := objectives * performance = measurable outcome`

**Cell (descriptive, warrant):**
- Step 1: `a := descriptive * warrant = observed justification → evidence`
- Step 2: `u := objectives * evidence = traceability aim`

---

## Matrix D (Assembled)

| | **mandate** | **specification** | **execution** | **warrant** |
|---|---|---|---|---|
| **normative** | governing aim | compliance target | regulatory outcome | authorization goal |
| **operative** | mission intent | design target | delivery milestone | viability benchmark |
| **descriptive** | scope definition | clarity goal | measurable outcome | traceability aim |

---

# Matrix K (Transpose of D)

**Matrix Parameters:**
- Size: 4×3
- Rows: [mandate, specification, execution, warrant]
- Columns: [normative, operative, descriptive]
- Construction: `K(i,j) = D(j,i)`

## Matrix K (Assembled)

| | **normative** | **operative** | **descriptive** |
|---|---|---|---|
| **mandate** | governing aim | mission intent | scope definition |
| **specification** | compliance target | design target | clarity goal |
| **execution** | regulatory outcome | delivery milestone | measurable outcome |
| **warrant** | authorization goal | viability benchmark | traceability aim |

---

# Matrix X (Verification) — Full Derivation

**Matrix Parameters:**
- L = verification
- Rows: [mandate, specification, execution, warrant]
- Columns: [ontology, epistemology, praxeology, axiology]

---

## Step-by-Step Cell Computation

### Row: mandate

**Cell (mandate, ontology):**
- Step 1: `a := mandate * ontology = authoritative being → jurisdiction`
- Step 2: `u := verification * jurisdiction = authority confirmation`

**Cell (mandate, epistemology):**
- Step 1: `a := mandate * epistemology = authoritative knowing → decree`
- Step 2: `u := verification * decree = directive validation`

**Cell (mandate, praxeology):**
- Step 1: `a := mandate * praxeology = authoritative action → command`
- Step 2: `u := verification * command = instruction audit`

**Cell (mandate, axiology):**
- Step 1: `a := mandate * axiology = authoritative value → priority`
- Step 2: `u := verification * priority = alignment check`

---

### Row: specification

**Cell (specification, ontology):**
- Step 1: `a := specification * ontology = detailed being → schema`
- Step 2: `u := verification * schema = structural validation`

**Cell (specification, epistemology):**
- Step 1: `a := specification * epistemology = detailed knowing → definition`
- Step 2: `u := verification * definition = semantic confirmation`

**Cell (specification, praxeology):**
- Step 1: `a := specification * praxeology = detailed action → procedure`
- Step 2: `u := verification * procedure = process inspection`

**Cell (specification, axiology):**
- Step 1: `a := specification * axiology = detailed value → criterion`
- Step 2: `u := verification * criterion = standards compliance`

---

### Row: execution

**Cell (execution, ontology):**
- Step 1: `a := execution * ontology = enacted being → artifact`
- Step 2: `u := verification * artifact = deliverable inspection`

**Cell (execution, epistemology):**
- Step 1: `a := execution * epistemology = enacted knowing → demonstration`
- Step 2: `u := verification * demonstration = proof review`

**Cell (execution, praxeology):**
- Step 1: `a := execution * praxeology = enacted action → operation`
- Step 2: `u := verification * operation = functional testing`

**Cell (execution, axiology):**
- Step 1: `a := execution * axiology = enacted value → result`
- Step 2: `u := verification * result = outcome assessment`

---

### Row: warrant

**Cell (warrant, ontology):**
- Step 1: `a := warrant * ontology = justified being → grounds`
- Step 2: `u := verification * grounds = basis attestation`

**Cell (warrant, epistemology):**
- Step 1: `a := warrant * epistemology = justified knowing → reasoning`
- Step 2: `u := verification * reasoning = logic audit`

**Cell (warrant, praxeology):**
- Step 1: `a := warrant * praxeology = justified action → sanction`
- Step 2: `u := verification * sanction = authorization review`

**Cell (warrant, axiology):**
- Step 1: `a := warrant * axiology = justified value → legitimation`
- Step 2: `u := verification * legitimation = validity assurance`

---

## Matrix X (Assembled)

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **mandate** | authority confirmation | directive validation | instruction audit | alignment check |
| **specification** | structural validation | semantic confirmation | process inspection | standards compliance |
| **execution** | deliverable inspection | proof review | functional testing | outcome assessment |
| **warrant** | basis attestation | logic audit | authorization review | validity assurance |

---

# Matrix G (Truncate X)

**Matrix Parameters:**
- Size: 3×4
- Rows: [mandate, specification, execution]
- Columns: [ontology, epistemology, praxeology, axiology]
- Construction: retain rows [mandate, specification, execution] from X; drop [warrant]

## Matrix G (Assembled)

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **mandate** | authority confirmation | directive validation | instruction audit | alignment check |
| **specification** | structural validation | semantic confirmation | process inspection | standards compliance |
| **execution** | deliverable inspection | proof review | functional testing | outcome assessment |

---

# Matrix E (Evaluation) — Full Derivation

**Matrix Parameters:**
- L = evaluation
- Rows: [mandate, specification, execution]
- Columns: [data, information, knowledge]

---

## Step-by-Step Cell Computation

### Row: mandate

**Cell (mandate, data):**
- Step 1: `a := mandate * data = authoritative signal → directive input`
- Step 2: `u := evaluation * directive input = requirement completeness`

**Cell (mandate, information):**
- Step 1: `a := mandate * information = authoritative meaning → policy statement`
- Step 2: `u := evaluation * policy statement = scope adequacy`

**Cell (mandate, knowledge):**
- Step 1: `a := mandate * knowledge = authoritative understanding → governance framework`
- Step 2: `u := evaluation * governance framework = strategic soundness`

---

### Row: specification

**Cell (specification, data):**
- Step 1: `a := specification * data = detailed signal → parameter`
- Step 2: `u := evaluation * parameter = precision assessment`

**Cell (specification, information):**
- Step 1: `a := specification * information = detailed meaning → description`
- Step 2: `u := evaluation * description = clarity appraisal`

**Cell (specification, knowledge):**
- Step 1: `a := specification * knowledge = detailed understanding → expertise`
- Step 2: `u := evaluation * expertise = technical sufficiency`

---

### Row: execution

**Cell (execution, data):**
- Step 1: `a := execution * data = enacted signal → measurement`
- Step 2: `u := evaluation * measurement = metric validation`

**Cell (execution, information):**
- Step 1: `a := execution * information = enacted meaning → report`
- Step 2: `u := evaluation * report = status accuracy`

**Cell (execution, knowledge):**
- Step 1: `a := execution * knowledge = enacted understanding → competence`
- Step 2: `u := evaluation * competence = capability judgment`

---

## Matrix E (Assembled)

| | **data** | **information** | **knowledge** |
|---|---|---|---|
| **mandate** | requirement completeness | scope adequacy | strategic soundness |
| **specification** | precision assessment | clarity appraisal | technical sufficiency |
| **execution** | metric validation | status accuracy | capability judgment |

---

# Summary of All Matrices

## Primary Matrices (with full derivations)

| Matrix | Lens | Size | Rows | Columns |
|--------|------|------|------|---------|
| C | formulation | 3×4 | normative, operative, descriptive | ontology, epistemology, praxeology, axiology |
| F | requirements | 3×4 | normative, operative, descriptive | ontology, epistemology, praxeology, axiology |
| D | objectives | 3×4 | normative, operative, descriptive | mandate, specification, execution, warrant |
| X | verification | 4×4 | mandate, specification, execution, warrant | ontology, epistemology, praxeology, axiology |
| E | evaluation | 3×3 | mandate, specification, execution | data, information, knowledge |

## Derived Matrices (transpose/truncate operations)

| Matrix | Operation | Size | Source |
|--------|-----------|------|--------|
| K | transpose | 4×3 | D |
| G | truncate | 3×4 | X (drop warrant row) |
| J | truncate | 3×4 | B (drop wisdom row) |
| T | transpose | 4×3 | J |
