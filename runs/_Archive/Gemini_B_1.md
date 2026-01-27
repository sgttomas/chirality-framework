# The Chirality Framework

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

1. **Axis anchor (latent coordinate frame):** For every cell compute:
   `a := r * c`  
   The product must be written out for each cell.
   
2. **Coordinate-conditioned projection of matrix label:** Let the label for that matrix be `L`
   For every cell compute: 
   `u := L * a`  
   For each cell the product `L *a` must be written out.

---

# Matrix Generations

## Matrix C (Formulation)

### Parameters
* **L (Lens):** Formulation
* **Rows (r):** [normative, operative, descriptive]
* **Columns (c):** [ontology, epistemology, praxeology, axiology]

### Step-by-Step Construction: `I(r, c, L)`

#### Row 1: Normative (The "Ought")

**Cell (1,1): Normative × Ontology**
* **Axis Anchor (`a`):** `normative` * `ontology` = *The standard of being / The ideal existence*
* **Interpretation (`u`):** `formulation` * *The standard of being* = **Concept**
    * *Reasoning:* Formulating the fundamental nature of what "should be" establishes the core Concept.

**Cell (1,2): Normative × Epistemology**
* **Axis Anchor (`a`):** `normative` * `epistemology` = *The standard of knowing / Rules of truth*
* **Interpretation (`u`):** `formulation` * *The standard of knowing* = **Schema**
    * *Reasoning:* Formulating the rules by which information is organized and validated creates a Schema.

**Cell (1,3): Normative × Praxeology**
* **Axis Anchor (`a`):** `normative` * `praxeology` = *The standard of action / Rules of conduct*
* **Interpretation (`u`):** `formulation` * *The standard of action* = **Policy**
    * *Reasoning:* Formulating the prescriptive rules for behavior results in Policy.

**Cell (1,4): Normative × Axiology**
* **Axis Anchor (`a`):** `normative` * `axiology` = *The standard of value / Measure of worth*
* **Interpretation (`u`):** `formulation` * *The standard of value* = **Criteria**
    * *Reasoning:* Formulating the benchmark for what is considered valuable defines Criteria.

#### Row 2: Operative (The "Doing")

**Cell (2,1): Operative × Ontology**
* **Axis Anchor (`a`):** `operative` * `ontology` = *Functional existence / The working structure*
* **Interpretation (`u`):** `formulation` * *Functional existence* = **Design**
    * *Reasoning:* Formulating how a thing exists in a working capacity is Design.

**Cell (2,2): Operative × Epistemology**
* **Axis Anchor (`a`):** `operative` * `epistemology` = *Functional knowing / How we know while working*
* **Interpretation (`u`):** `formulation` * *Functional knowing* = **Method**
    * *Reasoning:* Formulating the practical application of knowledge is Method.

**Cell (2,3): Operative × Praxeology**
* **Axis Anchor (`a`):** `operative` * `praxeology` = *Functional action / The mechanism of doing*
* **Interpretation (`u`):** `formulation` * *Functional action* = **Procedure**
    * *Reasoning:* Formulating the specific steps of execution is Procedure.

**Cell (2,4): Operative × Axiology**
* **Axis Anchor (`a`):** `operative` * `axiology` = *Functional value / Value in use*
* **Interpretation (`u`):** `formulation` * *Value in use* = **Function**
    * *Reasoning:* Formulating the utility or purpose served by the entity is its Function.

#### Row 3: Descriptive (The "Is")

**Cell (3,1): Descriptive × Ontology**
* **Axis Anchor (`a`):** `descriptive` * `ontology` = *Observed existence / Reality as seen*
* **Interpretation (`u`):** `formulation` * *Observed existence* = **State**
    * *Reasoning:* Formulating the description of current existence defines its State.

**Cell (3,2): Descriptive × Epistemology**
* **Axis Anchor (`a`):** `descriptive` * `epistemology` = *Observed knowledge / Recorded facts*
* **Interpretation (`u`):** `formulation` * *Observed knowledge* = **Data**
    * *Reasoning:* Formulating observed facts into a shareable format results in Data.

**Cell (3,3): Descriptive × Praxeology**
* **Axis Anchor (`a`):** `descriptive` * `praxeology` = *Observed action / Behavior history*
* **Interpretation (`u`):** `formulation` * *Observed action* = **Log**
    * *Reasoning:* Formulating the record of actions taken produces a Log.

**Cell (3,4): Descriptive × Axiology**
* **Axis Anchor (`a`):** `descriptive` * `axiology` = *Observed value / Measured worth*
* **Interpretation (`u`):** `formulation` * *Observed value* = **Metric**
    * *Reasoning:* Formulating the output value in a descriptive way creates a Metric.

### Matrix C Output

| | Ontology | Epistemology | Praxeology | Axiology |
| :--- | :--- | :--- | :--- | :--- |
| **Normative** | Concept | Schema | Policy | Criteria |
| **Operative** | Design | Method | Procedure | Function |
| **Descriptive** | State | Data | Log | Metric |

---

## Matrix F (Requirements)

### Parameters
* **L (Lens):** Requirements
* **Rows (r):** [normative, operative, descriptive]
* **Columns (c):** [ontology, epistemology, praxeology, axiology]

### Step-by-Step Construction: `I(r, c, L)`

#### Row 1: Normative (The "Must Be")

**Cell (1,1): Normative × Ontology**
* **Axis Anchor (`a`):** `normative` * `ontology` = *The standard of existence / The bounded reality*
* **Interpretation (`u`):** `requirements` * *The standard of existence* = **Scope**
    * *Reasoning:* A requirement defining the strict boundaries of what exists within the project is the Scope.

**Cell (1,2): Normative × Epistemology**
* **Axis Anchor (`a`):** `normative` * `epistemology` = *The standard of knowing / Authoritative truth*
* **Interpretation (`u`):** `requirements` * *The standard of knowing* = **Standard**
    * *Reasoning:* A requirement that sets the rules for information validity or format is a Standard.

**Cell (1,3): Normative × Praxeology**
* **Axis Anchor (`a`):** `normative` * `praxeology` = *The standard of action / Obligatory conduct*
* **Interpretation (`u`):** `requirements` * *The standard of action* = **Mandate**
    * *Reasoning:* A requirement that compels a specific course of action is a Mandate.

**Cell (1,4): Normative × Axiology**
* **Axis Anchor (`a`):** `normative` * `axiology` = *The standard of value / Required worth*
* **Interpretation (`u`):** `requirements` * *The standard of value* = **Grade**
    * *Reasoning:* A requirement establishing the necessary level or class of quality is a Grade.

#### Row 2: Operative (The "Will Do")

**Cell (2,1): Operative × Ontology**
* **Axis Anchor (`a`):** `operative` * `ontology` = *Functional existence / The working part*
* **Interpretation (`u`):** `requirements` * *Functional existence* = **Feature**
    * *Reasoning:* A requirement describing a functional part of the system is a Feature.

**Cell (2,2): Operative × Epistemology**
* **Axis Anchor (`a`):** `operative` * `epistemology` = *Functional knowing / Operational data flow*
* **Interpretation (`u`):** `requirements` * *Functional knowing* = **Interface**
    * *Reasoning:* A requirement describing how the system receives or recognizes information is an Interface.

**Cell (2,3): Operative × Praxeology**
* **Axis Anchor (`a`):** `operative` * `praxeology` = *Functional action / The working ability*
* **Interpretation (`u`):** `requirements` * *Functional action* = **Capability**
    * *Reasoning:* A requirement defining what the system must be able to do is a Capability.

**Cell (2,4): Operative × Axiology**
* **Axis Anchor (`a`):** `operative` * `axiology` = *Functional value / Value in operation*
* **Interpretation (`u`):** `requirements` * *Functional value* = **Performance**
    * *Reasoning:* A requirement defining the efficiency or utility of the operation is Performance.

#### Row 3: Descriptive (The "Given")

**Cell (3,1): Descriptive × Ontology**
* **Axis Anchor (`a`):** `descriptive` * `ontology` = *Observed existence / The surrounding reality*
* **Interpretation (`u`):** `requirements` * *Observed existence* = **Context**
    * *Reasoning:* A requirement that describes the necessary environment or state of the world is the Context.

**Cell (3,2): Descriptive × Epistemology**
* **Axis Anchor (`a`):** `descriptive` * `epistemology` = *Observed knowledge / Accepted facts*
* **Interpretation (`u`):** `requirements` * *Observed knowledge* = **Assumption**
    * *Reasoning:* A requirement based on facts believed to be true (but not controlled) is an Assumption.

**Cell (3,3): Descriptive × Praxeology**
* **Axis Anchor (`a`):** `descriptive` * `praxeology` = *Observed action / User behavior*
* **Interpretation (`u`):** `requirements` * *Observed action* = **Scenario**
    * *Reasoning:* A requirement described through a narrative of external action is a Scenario (or Use Case).

**Cell (3,4): Descriptive × Axiology**
* **Axis Anchor (`a`):** `descriptive` * `axiology` = *Observed value / External limits*
* **Interpretation (`u`):** `requirements` * *Observed value* = **Constraint**
    * *Reasoning:* A requirement that describes a limitation on value (budget, time, physics) is a Constraint.

### Matrix F Output

| | Ontology | Epistemology | Praxeology | Axiology |
| :--- | :--- | :--- | :--- | :--- |
| **Normative** | Scope | Standard | Mandate | Grade |
| **Operative** | Feature | Interface | Capability | Performance |
| **Descriptive** | Context | Assumption | Scenario | Constraint |

---

## Matrix D (Objectives)

### Parameters
* **L (Lens):** Objectives
* **Rows (r):** [normative, operative, descriptive]
* **Columns (c):** [mandate, specification, execution, warrant]

### Step-by-Step Construction: `I(r, c, L)`

#### Row 1: Normative (The Ideal Goal)

**Cell (1,1): Normative × Mandate**
* **Axis Anchor (`a`):** `normative` * `mandate` = *The obligation of the rule / Binding authority*
* **Interpretation (`u`):** `objectives` * *Binding authority* = **Compliance**
    * *Reasoning:* The objective regarding a normative mandate is to achieve Compliance.

**Cell (1,2): Normative × Specification**
* **Axis Anchor (`a`):** `normative` * `specification` = *The standard of definition / The perfect model*
* **Interpretation (`u`):** `objectives` * *The standard of definition* = **Conformity**
    * *Reasoning:* The objective regarding a normative specification is strictly adherence or Conformity.

**Cell (1,3): Normative × Execution**
* **Axis Anchor (`a`):** `normative` * `execution` = *The standard of doing / Right action*
* **Interpretation (`u`):** `objectives` * *The standard of doing* = **Integrity**
    * *Reasoning:* The objective of normative execution (doing things "right") is Integrity.

**Cell (1,4): Normative × Warrant**
* **Axis Anchor (`a`):** `normative` * `warrant` = *The standard of justification / Rightful backing*
* **Interpretation (`u`):** `objectives` * *The standard of justification* = **Legitimacy**
    * *Reasoning:* The objective of establishing a normative warrant is to ensure Legitimacy.

#### Row 2: Operative (The Functional Goal)

**Cell (2,1): Operative × Mandate**
* **Axis Anchor (`a`):** `operative` * `mandate` = *Functional obligation / Working orders*
* **Interpretation (`u`):** `objectives` * *Functional obligation* = **Alignment**
    * *Reasoning:* The objective of an operative mandate is ensuring the work is in Alignment with the goal.

**Cell (2,2): Operative × Specification**
* **Axis Anchor (`a`):** `operative` * `specification` = *Functional definition / Technical detail*
* **Interpretation (`u`):** `objectives` * *Functional definition* = **Precision**
    * *Reasoning:* The objective of an operative specification is to achieve Precision in the build.

**Cell (2,3): Operative × Execution**
* **Axis Anchor (`a`):** `operative` * `execution` = *Functional doing / The work flow*
* **Interpretation (`u`):** `objectives` * *Functional doing* = **Efficiency**
    * *Reasoning:* The primary objective of operative execution is Efficiency.

**Cell (2,4): Operative × Warrant**
* **Axis Anchor (`a`):** `operative` * `warrant` = *Functional justification / Proof of capacity*
* **Interpretation (`u`):** `objectives` * *Functional justification* = **Assurance**
    * *Reasoning:* The objective of an operative warrant (testing/checking) is to provide Assurance.

#### Row 3: Descriptive (The Observable Goal)

**Cell (3,1): Descriptive × Mandate**
* **Axis Anchor (`a`):** `descriptive` * `mandate` = *Observed obligation / Requirement tracking*
* **Interpretation (`u`):** `objectives` * *Observed obligation* = **Visibility**
    * *Reasoning:* The objective regarding the description of mandates is to maintain Visibility (knowing what is asked).

**Cell (3,2): Descriptive × Specification**
* **Axis Anchor (`a`):** `descriptive` * `specification` = *Observed definition / Recorded detail*
* **Interpretation (`u`):** `objectives` * *Observed definition* = **Completeness**
    * *Reasoning:* The objective regarding the description of specifications is ensuring Completeness.

**Cell (3,3): Descriptive × Execution**
* **Axis Anchor (`a`):** `descriptive` * `execution` = *Observed doing / Result output*
* **Interpretation (`u`):** `objectives` * *Observed doing* = **Yield**
    * *Reasoning:* The objective of descriptive execution (what actually came out) is the Yield.

**Cell (3,4): Descriptive × Warrant**
* **Axis Anchor (`a`):** `descriptive` * `warrant` = *Observed justification / The audit trail*
* **Interpretation (`u`):** `objectives` * *Observed justification* = **Traceability**
    * *Reasoning:* The objective of descriptive warrants (records of proof) is Traceability.

### Matrix D Output

| | Mandate | Specification | Execution | Warrant |
| :--- | :--- | :--- | :--- | :--- |
| **Normative** | Compliance | Conformity | Integrity | Legitimacy |
| **Operative** | Alignment | Precision | Efficiency | Assurance |
| **Descriptive** | Visibility | Completeness | Yield | Traceability |

---

## Matrix X (Verification)

### Parameters
* **L (Lens):** Verification
* **Rows (r):** [mandate, specification, execution, warrant]
* **Columns (c):** [ontology, epistemology, praxeology, axiology]

### Step-by-Step Construction: `I(r, c, L)`

#### Row 1: Mandate (Verifying the Requirements)

**Cell (1,1): Mandate × Ontology**
* **Axis Anchor (`a`):** `mandate` * `ontology` = *The reality of the requirement / The defined order*
* **Interpretation (`u`):** `verification` * *The defined order* = **Review**
    * *Reasoning:* Verifying that the mandate exists, is defined, and is captured correctly is a Review.

**Cell (1,2): Mandate × Epistemology**
* **Axis Anchor (`a`):** `mandate` * `epistemology` = *The logic of the requirement / Consistency*
* **Interpretation (`u`):** `verification` * *The logic of the requirement* = **Analysis**
    * *Reasoning:* Verifying the internal logic and consistency of the requirements requires Analysis.

**Cell (1,3): Mandate × Praxeology**
* **Axis Anchor (`a`):** `mandate` * `praxeology` = *The action of the requirement / Doability*
* **Interpretation (`u`):** `verification` * *The action of the requirement* = **Feasibility**
    * *Reasoning:* Verifying if the mandate can actually be performed is a Feasibility study.

**Cell (1,4): Mandate × Axiology**
* **Axis Anchor (`a`):** `mandate` * `axiology` = *The value of the requirement / Correctness of intent*
* **Interpretation (`u`):** `verification` * *The value of the requirement* = **Validation**
    * *Reasoning:* Verifying that the mandate asks for the "right thing" (value alignment) is Validation.

#### Row 2: Specification (Verifying the Design)

**Cell (2,1): Specification × Ontology**
* **Axis Anchor (`a`):** `specification` * `ontology` = *The reality of the design / The model artifacts*
* **Interpretation (`u`):** `verification` * *The model artifacts* = **Inspection**
    * *Reasoning:* Verifying the design artifacts (drawings, docs) against standards is an Inspection.

**Cell (2,2): Specification × Epistemology**
* **Axis Anchor (`a`):** `specification` * `epistemology` = *The logic of the design / Theoretical behavior*
* **Interpretation (`u`):** `verification` * *Theoretical behavior* = **Simulation**
    * *Reasoning:* Verifying how the design *should* behave based on its logic is Simulation.

**Cell (2,3): Specification × Praxeology**
* **Axis Anchor (`a`):** `specification` * `praxeology` = *The action of the design / The mechanism*
* **Interpretation (`u`):** `verification` * *The mechanism* = **Prototyping**
    * *Reasoning:* Verifying the mechanism works in a limited/early capacity is Prototyping.

**Cell (2,4): Specification × Axiology**
* **Axis Anchor (`a`):** `specification` * `axiology` = *The value of the design / Predicted outcome*
* **Interpretation (`u`):** `verification` * *Predicted outcome* = **Assessment**
    * *Reasoning:* Verifying the predicted value or risk profile of the design is an Assessment.

#### Row 3: Execution (Verifying the Build)

**Cell (3,1): Execution × Ontology**
* **Axis Anchor (`a`):** `execution` * `ontology` = *The reality of the build / The physical object*
* **Interpretation (`u`):** `verification` * *The physical object* = **Examination**
    * *Reasoning:* Verifying the physical attributes (dimensions, materials) of the execution is Examination.

**Cell (3,2): Execution × Epistemology**
* **Axis Anchor (`a`):** `execution` * `epistemology` = *The knowledge of the build / Output data*
* **Interpretation (`u`):** `verification` * *Output data* = **Testing**
    * *Reasoning:* Verifying the system by stimulating it and observing data is Testing.

**Cell (3,3): Execution × Praxeology**
* **Axis Anchor (`a`):** `execution` * `praxeology` = *The action of the build / Operations*
* **Interpretation (`u`):** `verification` * *Operations* = **Demonstration**
    * *Reasoning:* Verifying that the system performs its functions in a real-world context is a Demonstration.

**Cell (3,4): Execution × Axiology**
* **Axis Anchor (`a`):** `execution` * `axiology` = *The value of the build / Conformity to worth*
* **Interpretation (`u`):** `verification` * *Conformity to worth* = **Qualification**
    * *Reasoning:* Verifying that the execution meets the necessary quality or regulatory tier is Qualification.

#### Row 4: Warrant (Verifying the Proof)

**Cell (4,1): Warrant × Ontology**
* **Axis Anchor (`a`):** `warrant` * `ontology` = *The reality of the proof / The certificate*
* **Interpretation (`u`):** `verification` * *The certificate* = **Certification**
    * *Reasoning:* Verifying the existence and status of the warrant itself is Certification.

**Cell (4,2): Warrant × Epistemology**
* **Axis Anchor (`a`):** `warrant` * `epistemology` = *The knowledge of the proof / The evidence trail*
* **Interpretation (`u`):** `verification` * *The evidence trail* = **Audit**
    * *Reasoning:* Verifying the history and validity of the evidence is an Audit.

**Cell (4,3): Warrant × Praxeology**
* **Axis Anchor (`a`):** `warrant` * `praxeology` = *The action of the proof / Checking the check*
* **Interpretation (`u`):** `verification` * *Checking the check* = **Witnessing**
    * *Reasoning:* Verifying the act of verification (watching the test happen) is Witnessing.

**Cell (4,4): Warrant × Axiology**
* **Axis Anchor (`a`):** `warrant` * `axiology` = *The value of the proof / Confidence*
* **Interpretation (`u`):** `verification` * *Confidence* = **Acceptance**
    * *Reasoning:* The final verification of the warrant's value—acknowledging it is sufficient—is Acceptance.

### Matrix X Output

| | Ontology | Epistemology | Praxeology | Axiology |
| :--- | :--- | :--- | :--- | :--- |
| **Mandate** | Review | Analysis | Feasibility | Validation |
| **Specification** | Inspection | Simulation | Prototyping | Assessment |
| **Execution** | Examination | Testing | Demonstration | Qualification |
| **Warrant** | Certification | Audit | Witnessing | Acceptance |

---

## Matrix E (Evaluation)

### Parameters
* **L (Lens):** Evaluation
* **Rows (r):** [mandate, specification, execution]
* **Columns (c):** [data, information, knowledge]

### Step-by-Step Construction: `I(r, c, L)`

#### Row 1: Mandate (Evaluating the Ask)

**Cell (1,1): Mandate × Data**
* **Axis Anchor (`a`):** `mandate` * `data` = *The facts of the requirement / The items requested*
* **Interpretation (`u`):** `evaluation` * *The facts of the requirement* = **Sufficiency**
    * *Reasoning:* Evaluating whether the data of the mandate covers all necessary items determines Sufficiency.

**Cell (1,2): Mandate × Information**
* **Axis Anchor (`a`):** `mandate` * `information` = *The meaning of the requirement / Contextual understanding*
* **Interpretation (`u`):** `evaluation` * *The meaning of the requirement* = **Unambiguity**
    * *Reasoning:* Evaluating the information content of a mandate to ensure it has only one meaning is checking for Unambiguity.

**Cell (1,3): Mandate × Knowledge**
* **Axis Anchor (`a`):** `mandate` * `knowledge` = *The wisdom of the requirement / The "Why"*
* **Interpretation (`u`):** `evaluation` * *The wisdom of the requirement* = **Justification**
    * *Reasoning:* Evaluating the underlying knowledge or reason behind a mandate provides its Justification.

#### Row 2: Specification (Evaluating the Plan)

**Cell (2,1): Specification × Data**
* **Axis Anchor (`a`):** `specification` * `data` = *The facts of the design / Technical figures*
* **Interpretation (`u`):** `evaluation` * *The facts of the design* = **Correctness**
    * *Reasoning:* Evaluating the raw data and figures of a specification against the standard determines Correctness.

**Cell (2,2): Specification × Information**
* **Axis Anchor (`a`):** `specification` * `information` = *The meaning of the design / System logic*
* **Interpretation (`u`):** `evaluation` * *The meaning of the design* = **Compatibility**
    * *Reasoning:* Evaluating how the information within the spec fits together (or fits with others) determines Compatibility.

**Cell (2,3): Specification × Knowledge**
* **Axis Anchor (`a`):** `specification` * `knowledge` = *The wisdom of the design / Engineering synthesis*
* **Interpretation (`u`):** `evaluation` * *The wisdom of the design* = **Maintainability**
    * *Reasoning:* Evaluating the deep design knowledge implies looking forward to future states, which is Maintainability.

#### Row 3: Execution (Evaluating the Result)

**Cell (3,1): Execution × Data**
* **Axis Anchor (`a`):** `execution` * `data` = *The facts of the action / Output values*
* **Interpretation (`u`):** `evaluation` * *The facts of the action* = **Accuracy**
    * *Reasoning:* Evaluating the data resulting from execution against the target determines Accuracy.

**Cell (3,2): Execution × Information**
* **Axis Anchor (`a`):** `execution` * `information` = *The meaning of the action / Process stability*
* **Interpretation (`u`):** `evaluation` * *The meaning of the action* = **Reliability**
    * *Reasoning:* Evaluating the execution pattern over time to ensure consistent meaning is Reliability.

**Cell (3,3): Execution × Knowledge**
* **Axis Anchor (`a`):** `execution` * `knowledge` = *The wisdom of the action / Problem solving*
* **Interpretation (`u`):** `evaluation` * *The wisdom of the action* = **Utility**
    * *Reasoning:* Evaluating the ultimate application of the execution (did it solve the problem?) determines Utility.

### Matrix E Output

| | Data | Information | Knowledge |
| :--- | :--- | :--- | :--- |
| **Mandate** | Sufficiency | Unambiguity | Justification |
| **Specification** | Correctness | Compatibility | Maintainability |
| **Execution** | Accuracy | Reliability | Utility |