# The Chirality Framework: Complete Derivation Log

## 1. Framework Definitions & Canonical Matrices

### What is the Chirality Framework?

The Chirality Framework is a semantic algebra for knowledge work.

The framework treats words not as labels but as attractors in embedding space. Matrix elements don't define answers—they partition the solution space into regions where answers can emerge. This is **tiling, not covering**: elements partition semantic space without attempting to enumerate all possibilities.

---

### Principles

1. **Tile, don't cover.** Cells are attractors, not definitions. They partition semantic space into navigable regions without attempting exhaustive specification.
2. **Seed, don't specify.** Give coordinates, not work instructions. The latent embedding space does the generative work.
3. **Show your work.** Explicitly write out each step according to the instructions below.

---

### Semantic Operations

#### Semantic Multiplication `*`
Semantic multiplication combines two terms into their semantic intersection—the meaning that emerges when the meaning of both concepts are combined.

Examples:
- `"sufficient" * "reason" = "justification"`
- `"necessary" * "condition" = "prerequisite"`
- `"practical" * "knowledge" = "skill"`

**Typing rule:** `*` is defined over **single semantic units** (words or phrase).  
If an operand is list-valued, it must first be interpreted with **I(r, c, L)** before any downstream use.

#### Semantic Addition `+`
Semantic addition groups terms into a collection. 

#### Order of Operations
1. Parentheses
2. `*` left-to-right
3. `+` left-to-right

---

### Interpretation Operator `I(r, c, L)`

#### Purpose
`I` coerces a list-valued cell (a collection of contributors) into a **single atomic semantic unit** that:
- is conditioned by the cell’s coordinate axes (**row label r** and **column label c**),
- does **not** explicitly name those axes (axes are latent constraints),
- is compact and non-enumerative,
- will be used in downstream `*` operations.

#### Precise Definition (procedural)
Let `L` be treated as a **set**. Interpret one cell at a time, following each of these three steps in sequence.  

1. **Axis anchor (latent coordinate frame):** For every cell compute: `a := r * c`  
   The product must be written out for each cell.

2. **Coordinate-conditioned projection of contributors:** For each cell and every contributor `t ∈ L`, compute a projected contributor: `p_t := a * t`  
   The projection step must appear explicitly in the working.

3. **Centroid attractor selection (non-enumerative synthesis):** Choose an atomic unit `u` such that the meaning of `u` is the **closest stable attractor** to the centroid of the set `{p_t}`.

---

### Canonical Matrices

#### Matrix A 
Size: 3×4  
Columns: [mandate, specification, execution, warrant]  
Rows: [normative, operative, descriptive]

| | **mandate** | **specification** | **execution** | **warrant** |
|---|---|---|---|---|
| **normative** | obligation | requirements | congruence | sufficiency |
| **operative** | directive | design | implementation | decision |
| **descriptive** | constraint | configuration | outcome | substantiation |

#### Matrix B 
Size: 4×4  
Columns: [ontology, epistemology, praxeology, axiology]  
Rows: [data, information, knowledge, wisdom]

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **data** | fact | evidence | signal | accuracy |
| **information** | context | traceability | analysis | relevance | 
| **knowledge** | model | verification | method | validation |
| **wisdom** | principle | justification | governance | prudence |

---

## 2. Derivation of Matrix C

### Construction Logic
**Matrix Operation:** Dot Product (`·`)
`L_C(i,j) = Σ_k (A(i,k) * B(k,j))`
Summation occurs over `k` = [1..4], mapping the columns of A (`mandate, specification, execution, warrant`) to the rows of B (`data, information, knowledge, wisdom`).

**Interpretation:**
`C(i,j) = I(row_i, col_j, L_C(i,j))`

### Row 1: Normative
**Axis:** `r = normative`

#### Cell C(1,1): Normative / Ontology
**Step 1: Axis Anchor**
`a` = normative * ontology = **"Regulated Existence"**
**Step 2: Projection of Contributors (L)**
1. `obligation` * `fact` = *binding reality* -> `p_1` = **"Statutory Fact"**
2. `requirements` * `context` = *necessary condition* -> `p_2` = **"Prerequisite State"**
3. `congruence` * `model` = *aligned representation* -> `p_3` = **"Standard Model"**
4. `sufficiency` * `principle` = *foundational adequacy* -> `p_4` = **"Constitutive Basis"**
**Step 3: Centroid Attractor**
`u` = **"Constitutive Standard"**

#### Cell C(1,2): Normative / Epistemology
**Step 1: Axis Anchor**
`a` = normative * epistemology = **"Authoritative Knowledge"**
**Step 2: Projection of Contributors (L)**
1. `obligation` * `evidence` = *burden of proof* -> `p_1` = **"Required Evidence"**
2. `requirements` * `traceability` = *audit trail* -> `p_2` = **"Compliance Trace"**
3. `congruence` * `verification` = *conformance check* -> `p_3` = **"Verification Standard"**
4. `sufficiency` * `justification` = *defensible reason* -> `p_4` = **"Warranted Logic"**
**Step 3: Centroid Attractor**
`u` = **"Compliance Verification"**

#### Cell C(1,3): Normative / Praxeology
**Step 1: Axis Anchor**
`a` = normative * praxeology = **"Prescribed Action"**
**Step 2: Projection of Contributors (L)**
1. `obligation` * `signal` = *imperative cue* -> `p_1` = **"Call to Action"**
2. `requirements` * `analysis` = *scoping* -> `p_2` = **"Feasibility Study"**
3. `congruence` * `method` = *procedural integrity* -> `p_3` = **"Best Practice"**
4. `sufficiency` * `governance` = *regulatory oversight* -> `p_4` = **"Control Framework"**
**Step 3: Centroid Attractor**
`u` = **"Standard Operating Procedure"**

#### Cell C(1,4): Normative / Axiology
**Step 1: Axis Anchor**
`a` = normative * axiology = **"Required Value"**
**Step 2: Projection of Contributors (L)**
1. `obligation` * `accuracy` = *strict fidelity* -> `p_1` = **"Precision Mandate"**
2. `requirements` * `relevance` = *pertinence* -> `p_2` = **"Scope Definition"**
3. `congruence` * `validation` = *fitness for purpose* -> `p_3` = **"Acceptance Criteria"**
4. `sufficiency` * `prudence` = *risk mitigation* -> `p_4` = **"Safety Margin"**
**Step 3: Centroid Attractor**
`u` = **"Quality Assurance"**

### Row 2: Operative
**Axis:** `r = operative`

#### Cell C(2,1): Operative / Ontology
**Step 1: Axis Anchor**
`a` = operative * ontology = **"Functional Reality"**
**Step 2: Projection of Contributors (L)**
1. `directive` * `fact` = *established order* -> `p_1` = **"System State"**
2. `design` * `context` = *architecture* -> `p_2` = **"Environment Topology"**
3. `implementation` * `model` = *realization* -> `p_3` = **"Deployed Instance"**
4. `decision` * `principle` = *ruling* -> `p_4` = **"Operational Rule"**
**Step 3: Centroid Attractor**
`u` = **"Operational Entity"**

#### Cell C(2,2): Operative / Epistemology
**Step 1: Axis Anchor**
`a` = operative * epistemology = **"Technical Knowledge"**
**Step 2: Projection of Contributors (L)**
1. `directive` * `evidence` = *command validation* -> `p_1` = **"Input Validation"**
2. `design` * `traceability` = *lineage* -> `p_2` = **"Version Control"**
3. `implementation` * `verification` = *build check* -> `p_3` = **"Unit Test"**
4. `decision` * `justification` = *rationale* -> `p_4` = **"Design Logic"**
**Step 3: Centroid Attractor**
`u` = **"Technical Specification"**

#### Cell C(2,3): Operative / Praxeology
**Step 1: Axis Anchor**
`a` = operative * praxeology = **"Active Execution"**
**Step 2: Projection of Contributors (L)**
1. `directive` * `signal` = *trigger* -> `p_1` = **"Process Start"**
2. `design` * `analysis` = *engineering* -> `p_2` = **"Solution Architecture"**
3. `implementation` * `method` = *technique* -> `p_3` = **"Deployment Mechanism"**
4. `decision` * `governance` = *steering* -> `p_4` = **"Management Action"**
**Step 3: Centroid Attractor**
`u` = **"Workflow Execution"**

#### Cell C(2,4): Operative / Axiology
**Step 1: Axis Anchor**
`a` = operative * axiology = **"Functional Utility"**
**Step 2: Projection of Contributors (L)**
1. `directive` * `accuracy` = *target precision* -> `p_1` = **"Performance Goal"**
2. `design` * `relevance` = *utility* -> `p_2` = **"Feature Fit"**
3. `implementation` * `validation` = *stress test* -> `p_3` = **"Reliability Check"**
4. `decision` * `prudence` = *risk aversion* -> `p_4` = **"Fail-safe"**
**Step 3: Centroid Attractor**
`u` = **"Performance Metric"**

### Row 3: Descriptive
**Axis:** `r = descriptive`

#### Cell C(3,1): Descriptive / Ontology
**Step 1: Axis Anchor**
`a` = descriptive * ontology = **"Observed Reality"**
**Step 2: Projection of Contributors (L)**
1. `constraint` * `fact` = *boundary condition* -> `p_1` = **"Physical Limit"**
2. `configuration` * `context` = *setting* -> `p_2` = **"Current State"**
3. `outcome` * `model` = *simulation result* -> `p_3` = **"Digital Twin"**
4. `substantiation` * `principle` = *axiom* -> `p_4` = **"Ground Truth"**
**Step 3: Centroid Attractor**
`u` = **"Baseline Configuration"**

#### Cell C(3,2): Descriptive / Epistemology
**Step 1: Axis Anchor**
`a` = descriptive * epistemology = **"Recorded Information"**
**Step 2: Projection of Contributors (L)**
1. `constraint` * `evidence` = *limitation proof* -> `p_1` = **"Constraint Log"**
2. `configuration` * `traceability` = *history* -> `p_2` = **"Change Log"**
3. `outcome` * `verification` = *results confirmation* -> `p_3` = **"Test Report"**
4. `substantiation` * `justification` = *empirical support* -> `p_4` = **"Data Proof"**
**Step 3: Centroid Attractor**
`u` = **"System Record"**

#### Cell C(3,3): Descriptive / Praxeology
**Step 1: Axis Anchor**
`a` = descriptive * praxeology = **"Process History"**
**Step 2: Projection of Contributors (L)**
1. `constraint` * `signal` = *alert* -> `p_1` = **"Error Log"**
2. `configuration` * `analysis` = *setup review* -> `p_2` = **"Diagnostic"**
3. `outcome` * `method` = *effect* -> `p_3` = **"Output Metric"**
4. `substantiation` * `governance` = *audit* -> `p_4` = **"Compliance Report"**
**Step 3: Centroid Attractor**
`u` = **"Activity Log"**

#### Cell C(3,4): Descriptive / Axiology
**Step 1: Axis Anchor**
`a` = descriptive * axiology = **"Measured Value"**
**Step 2: Projection of Contributors (L)**
1. `constraint` * `accuracy` = *tolerance* -> `p_1` = **"Variance Limit"**
2. `configuration` * `relevance` = *applicability* -> `p_2` = **"Utilization Rate"**
3. `outcome` * `validation` = *success* -> `p_3` = **"Benefit Realization"**
4. `substantiation` * `prudence` = *safety check* -> `p_4` = **"Risk Register"**
**Step 3: Centroid Attractor**
`u` = **"Impact Assessment"**

### Final Matrix C

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **normative** | Constitutive Standard | Compliance Verification | Standard Operating Procedure | Quality Assurance |
| **operative** | Operational Entity | Technical Specification | Workflow Execution | Performance Metric |
| **descriptive** | Baseline Configuration | System Record | Activity Log | Impact Assessment |

---

## 3. Derivation of Matrix F

### Construction Logic
**Matrix Operation:** Hadamard Product (`⊙`)
`F_raw(i,j) = J(i,j) * C(i,j)`
`J` is Matrix B truncated (rows: data, information, knowledge).

### Row 1: Normative
#### F(1,1): `fact` * `Constitutive Standard` = **"Provision"**
#### F(1,2): `evidence` * `Compliance Verification` = **"Audit Artifact"**
#### F(1,3): `signal` * `Standard Operating Procedure` = **"Procedural Trigger"**
#### F(1,4): `accuracy` * `Quality Assurance` = **"Calibration Data"**

### Row 2: Operative
#### F(2,1): `context` * `Operational Entity` = **"State Vector"**
#### F(2,2): `traceability` * `Technical Specification` = **"Change Control ID"**
#### F(2,3): `analysis` * `Workflow Execution` = **"Process Diagnostics"**
#### F(2,4): `relevance` * `Performance Metric` = **"KPI Alignment"**

### Row 3: Descriptive
#### F(3,1): `model` * `Baseline Configuration` = **"Schema Definition"**
#### F(3,2): `verification` * `System Record` = **"Integrity Check"**
#### F(3,3): `method` * `Activity Log` = **"Forensic Analysis"**
#### F(3,4): `validation` * `Impact Assessment` = **"Effectiveness Review"**

### Final Matrix F

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **normative** | Provision | Audit Artifact | Procedural Trigger | Calibration Data |
| **operative** | State Vector | Change Control ID | Process Diagnostics | KPI Alignment |
| **descriptive** | Schema Definition | Integrity Check | Forensic Analysis | Effectiveness Review |

---

## 4. Derivation of Matrix D

### Construction Logic
**Matrix Operation:** Addition (`+`) with Scalar Multiplication
`L_D(i,j) = A(i,j) + ("resolution" * F(i,j))`

### Row 1: Normative
**Axis:** `r = normative`
1. **D(1,1):** `obligation` + ("resolution" * `Provision`)
   - Projections: "Legal Duty" + "Statutory Effect" -> **"Effective Mandate"**
2. **D(1,2):** `requirements` + ("resolution" * `Audit Artifact`)
   - Projections: "Design Constraint" + "Compliance Proof" -> **"Certified Requirement"**
3. **D(1,3):** `congruence` + ("resolution" * `Procedural Trigger`)
   - Projections: "Alignment Check" + "Authorized Start" -> **"Validated Protocol"**
4. **D(1,4):** `sufficiency` + ("resolution" * `Calibration Data`)
   - Projections: "Adequacy Limit" + "Toleranced Fit" -> **"Qualified Assurance"**

### Row 2: Operative
**Axis:** `r = operative`
1. **D(2,1):** `directive` + ("resolution" * `State Vector`)
   - Projections: "Command Signal" + "Goal Vector" -> **"Steering Command"**
2. **D(2,2):** `design` + ("resolution" * `Change Control ID`)
   - Projections: "Schematic" + "Patch Definition" -> **"Current Build"**
3. **D(2,3):** `implementation` + ("resolution" * `Process Diagnostics`)
   - Projections: "Process Instance" + "Tuning Action" -> **"Adaptive Execution"**
4. **D(2,4):** `decision` + ("resolution" * `KPI Alignment`)
   - Projections: "Go/No-Go" + "Threshold Adjustment" -> **"Control Decision"**

### Row 3: Descriptive
**Axis:** `r = descriptive`
1. **D(3,1):** `constraint` + ("resolution" * `Schema Definition`)
   - Projections: "Hard Limit" + "Fixed Format" -> **"Immutable Constraint"**
2. **D(3,2):** `configuration` + ("resolution" * `Integrity Check`)
   - Projections: "Parameter Set" + "Verified Setup" -> **"Stable Configuration"**
3. **D(3,3):** `outcome` + ("resolution" * `Forensic Analysis`)
   - Projections: "Final State" + "Explained Variance" -> **"Settled Outcome"**
4. **D(3,4):** `substantiation` + ("resolution" * `Effectiveness Review`)
   - Projections: "Evidence Log" + "Benefit Confirmation" -> **"Validated ROI"**

### Final Matrix D

| | **mandate** | **specification** | **execution** | **warrant** |
|---|---|---|---|---|
| **normative** | Effective Mandate | Certified Requirement | Validated Protocol | Qualified Assurance |
| **operative** | Steering Command | Current Build | Adaptive Execution | Control Decision |
| **descriptive** | Immutable Constraint | Stable Configuration | Settled Outcome | Validated ROI |

---

## 5. Derivation of Matrix X

### Construction Logic
**Matrix Operation:** Matrix Multiplication (`·`)
`L_X(i,j) = Σ_k (K(i,k) * J(k,j))`
`K` is `D` Transposed.

### Row 1: Mandate
**Axis:** `r = mandate`
1. **X(1,1) Ontology:** `Effective Mandate`*`fact` + `Steering Command`*`context` + `Immutable Constraint`*`model`
   - Centroid: **"Jurisdiction"**
2. **X(1,2) Epistemology:** `Effective Mandate`*`evidence` + `Steering Command`*`traceability` + `Immutable Constraint`*`verification`
   - Centroid: **"Regulatory Registry"**
3. **X(1,3) Praxeology:** `Effective Mandate`*`signal` + `Steering Command`*`analysis` + `Immutable Constraint`*`method`
   - Centroid: **"Governance Procedure"**
4. **X(1,4) Axiology:** `Effective Mandate`*`accuracy` + `Steering Command`*`relevance` + `Immutable Constraint`*`validation`
   - Centroid: **"Fiduciary Duty"**

### Row 2: Specification
**Axis:** `r = specification`
1. **X(2,1) Ontology:** `Certified Requirement`*`fact` + `Current Build`*`context` + `Stable Configuration`*`model`
   - Centroid: **"System Definition"**
2. **X(2,2) Epistemology:** `Certified Requirement`*`evidence` + `Current Build`*`traceability` + `Stable Configuration`*`verification`
   - Centroid: **"Configuration Management"**
3. **X(2,3) Praxeology:** `Certified Requirement`*`signal` + `Current Build`*`analysis` + `Stable Configuration`*`method`
   - Centroid: **"Build Process"**
4. **X(2,4) Axiology:** `Certified Requirement`*`accuracy` + `Current Build`*`relevance` + `Stable Configuration`*`validation`
   - Centroid: **"Release Criteria"**

### Row 3: Execution
**Axis:** `r = execution`
1. **X(3,1) Ontology:** `Validated Protocol`*`fact` + `Adaptive Execution`*`context` + `Settled Outcome`*`model`
   - Centroid: **"Operational Status"**
2. **X(3,2) Epistemology:** `Validated Protocol`*`evidence` + `Adaptive Execution`*`traceability` + `Settled Outcome`*`verification`
   - Centroid: **"Telemetry"**
3. **X(3,3) Praxeology:** `Validated Protocol`*`signal` + `Adaptive Execution`*`analysis` + `Settled Outcome`*`method`
   - Centroid: **"Runtime Operations"**
4. **X(3,4) Axiology:** `Validated Protocol`*`accuracy` + `Adaptive Execution`*`relevance` + `Settled Outcome`*`validation`
   - Centroid: **"Performance Efficiency"**

### Row 4: Warrant
**Axis:** `r = warrant`
1. **X(4,1) Ontology:** `Qualified Assurance`*`fact` + `Control Decision`*`context` + `Validated ROI`*`model`
   - Centroid: **"Certification"**
2. **X(4,2) Epistemology:** `Qualified Assurance`*`evidence` + `Control Decision`*`traceability` + `Validated ROI`*`verification`
   - Centroid: **"Attestation"**
3. **X(4,3) Praxeology:** `Qualified Assurance`*`signal` + `Control Decision`*`analysis` + `Validated ROI`*`method`
   - Centroid: **"Audit Procedure"**
4. **X(4,4) Axiology:** `Qualified Assurance`*`accuracy` + `Control Decision`*`relevance` + `Validated ROI`*`validation`
   - Centroid: **"Value Realization"**

### Final Matrix X

| | **ontology** | **epistemology** | **praxeology** | **axiology** |
|---|---|---|---|---|
| **mandate** | Jurisdiction | Regulatory Registry | Governance Procedure | Fiduciary Duty |
| **specification** | System Definition | Configuration Management | Build Process | Release Criteria |
| **execution** | Operational Status | Telemetry | Runtime Operations | Performance Efficiency |
| **warrant** | Certification | Attestation | Audit Procedure | Value Realization |

---

## 6. Derivation of Matrix E

### Construction Logic
**Matrix Operation:** Matrix Multiplication (`·`)
`L_E(i,j) = Σ_k (G(i,k) * T(k,j))`
`G` is `X` Truncated (rows: mandate, spec, exec). `T` is `J` Transposed.

### Row 1: Mandate
**Axis:** `r = mandate`
1. **E(1,1) Data:** Sum of (`Jurisdiction`*`fact`, `Regulatory Registry`*`evidence`, `Governance Procedure`*`signal`, `Fiduciary Duty`*`accuracy`)
   - Centroid: **"Statutory Registry"**
2. **E(1,2) Information:** Sum of (`Jurisdiction`*`context`, `Regulatory Registry`*`traceability`, `Governance Procedure`*`analysis`, `Fiduciary Duty`*`relevance`)
   - Centroid: **"Regulatory Guidance"**
3. **E(1,3) Knowledge:** Sum of (`Jurisdiction`*`model`, `Regulatory Registry`*`verification`, `Governance Procedure`*`method`, `Fiduciary Duty`*`validation`)
   - Centroid: **"Legal Doctrine"**

### Row 2: Specification
**Axis:** `r = specification`
1. **E(2,1) Data:** Sum of (`System Definition`*`fact`, `Config Management`*`evidence`, `Build Process`*`signal`, `Release Criteria`*`accuracy`)
   - Centroid: **"Configuration Data"**
2. **E(2,2) Information:** Sum of (`System Definition`*`context`, `Config Management`*`traceability`, `Build Process`*`analysis`, `Release Criteria`*`relevance`)
   - Centroid: **"System Architecture"**
3. **E(2,3) Knowledge:** Sum of (`System Definition`*`model`, `Config Management`*`verification`, `Build Process`*`method`, `Release Criteria`*`validation`)
   - Centroid: **"Solution Design"**

### Row 3: Execution
**Axis:** `r = execution`
1. **E(3,1) Data:** Sum of (`Operational Status`*`fact`, `Telemetry`*`evidence`, `Runtime Ops`*`signal`, `Perf Efficiency`*`accuracy`)
   - Centroid: **"Operational Metrics"**
2. **E(3,2) Information:** Sum of (`Operational Status`*`context`, `Telemetry`*`traceability`, `Runtime Ops`*`analysis`, `Perf Efficiency`*`relevance`)
   - Centroid: **"Performance Analytics"**
3. **E(3,3) Knowledge:** Sum of (`Operational Status`*`model`, `Telemetry`*`verification`, `Runtime Ops`*`method`, `Perf Efficiency`*`validation`)
   - Centroid: **"Adaptive Control"**

### Final Matrix E

| | **data** | **information** | **knowledge** |
|---|---|---|---|
| **mandate** | Statutory Registry | Regulatory Guidance | Legal Doctrine |
| **specification** | Configuration Data | System Architecture | Solution Design |
| **execution** | Operational Metrics | Performance Analytics | Adaptive Control |