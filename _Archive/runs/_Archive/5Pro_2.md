Reference spec (attached):  ￼

Given matrices

Matrix A (Activity structure)

	guiding	applying	judging	reflecting
normative	principle	conduct	evaluation	integrity
operative	procedure	methods	criteria	adaptation
descriptive	observation	documentation	assessment	understanding

Matrix B (Knowledge structure)

	ontology	epistemology	axiology	praxeology
data	fact	evidence	significance	signal
information	taxonomy	provenance	relevance	protocol
knowledge	architecture	framework	interpretation	principle
wisdom	ground	insight	purpose	measure

Inner-dimension alignment for the dot product

For L_C(i,j) = Σ_k (A(i,k) * B(k,j)), the shared inner dimension is 4, so we pair by position:
	1.	k=1: A.guiding  ↔  B.data
	2.	k=2: A.applying ↔  B.information
	3.	k=3: A.judging  ↔  B.knowledge
	4.	k=4: A.reflecting ↔  B.wisdom

⸻

Step 1 — Build the intermediate collection-valued matrix L_C

Each cell is a collection of 4 semantic products (ordered by k for construction; interpreted as a set later).

row \ col	ontology	epistemology	axiology	praxeology
normative	principlefact → axiomconducttaxonomy → behavioral taxonomyevaluationarchitecture → architectural appraisalintegrityground → ethical grounding	principleevidence → warrantconductprovenance → accountabilityevaluationframework → benchmarkingintegrityinsight → moral clarity	principlesignificance → imperativeconductrelevance → proprietyevaluationinterpretation → critiqueintegritypurpose → fidelity	principlesignal → directiveconductprotocol → complianceevaluationprinciple → standards auditintegritymeasure → integrity metric
operative	procedurefact → operating rulemethodstaxonomy → method taxonomycriteriaarchitecture → design constraintsadaptationground → anchored flexibility	procedureevidence → testingmethodsprovenance → source trackingcriteriaframework → rubricadaptationinsight → informed adjustment	proceduresignificance → prioritizationmethodsrelevance → method selectioncriteriainterpretation → interpretive standardsadaptationpurpose → goal alignment	proceduresignal → signal processingmethodsprotocol → standard methodcriteriaprinciple → decision ruleadaptationmeasure → feedback loop
descriptive	observationfact → empirical findingdocumentationtaxonomy → catalogassessmentarchitecture → structural analysisunderstandingground → foundational grasp	observationevidence → corroborationdocumentationprovenance → audit trailassessmentframework → diagnostic modelunderstandinginsight → realization	observationsignificance → saliencedocumentationrelevance → curationassessmentinterpretation → sensemakingunderstandingpurpose → intent	observationsignal → detectiondocumentationprotocol → logassessmentprinciple → reasoned judgmentunderstandingmeasure → calibration

At this point, nothing may flow downstream because each cell is list-valued (collection-valued).

⸻

Step 2 — Interpret each cell with I(r, c, L) to get atomic (un-lensed) C

Below, for each cell:
	•	a := r * c (axis anchor; latent frame)
	•	L is treated as a set (duplicates removed; order-insensitive)
	•	For each t ∈ L, compute p_t := a * t
	•	Choose a single atomic u (no axis tokens, compact noun phrase) as I(r,c,L)

Normative row

C[normative, ontology]
	•	Axis anchor: a := normative * ontology = ethical realism
	•	Intermediate set: L = { axiom, behavioral taxonomy, architectural appraisal, ethical grounding }
	•	Projections:
	•	ethical realism * axiom = ethical axiom
	•	ethical realism * behavioral taxonomy = ethical typology
	•	ethical realism * architectural appraisal = ethical model review
	•	ethical realism * ethical grounding = grounded ethics
	•	Interpreted atomic output: I(...) = ethical worldview

C[normative, epistemology]
	•	Axis anchor: a := normative * epistemology = moral reasoning
	•	Intermediate set: L = { warrant, accountability, benchmarking, moral clarity }
	•	Projections:
	•	moral reasoning * warrant = reasoned justification
	•	moral reasoning * accountability = responsible judgment
	•	moral reasoning * benchmarking = ethical benchmarking
	•	moral reasoning * moral clarity = principled clarity
	•	Interpreted atomic output: I(...) = justified judgment

C[normative, axiology]
	•	Axis anchor: a := normative * axiology = value judgment
	•	Intermediate set: L = { imperative, propriety, critique, fidelity }
	•	Projections:
	•	value judgment * imperative = binding imperative
	•	value judgment * propriety = ethical propriety
	•	value judgment * critique = evaluative critique
	•	value judgment * fidelity = principled fidelity
	•	Interpreted atomic output: I(...) = value discernment

C[normative, praxeology]
	•	Axis anchor: a := normative * praxeology = ethical practice
	•	Intermediate set: L = { directive, compliance, standards audit, integrity metric }
	•	Projections:
	•	ethical practice * directive = action guidance
	•	ethical practice * compliance = conscientious compliance
	•	ethical practice * standards audit = ethical audit
	•	ethical practice * integrity metric = measured integrity
	•	Interpreted atomic output: I(...) = integrity governance

⸻

Operative row

C[operative, ontology]
	•	Axis anchor: a := operative * ontology = working model
	•	Intermediate set: L = { operating rule, method taxonomy, design constraints, anchored flexibility }
	•	Projections:
	•	working model * operating rule = process rule
	•	working model * method taxonomy = method map
	•	working model * design constraints = design specification
	•	working model * anchored flexibility = adaptive model
	•	Interpreted atomic output: I(...) = workable system design

C[operative, epistemology]
	•	Axis anchor: a := operative * epistemology = methodical inquiry
	•	Intermediate set: L = { testing, source tracking, rubric, informed adjustment }
	•	Projections:
	•	methodical inquiry * testing = experimental method
	•	methodical inquiry * source tracking = evidence traceability
	•	methodical inquiry * rubric = scoring rubric
	•	methodical inquiry * informed adjustment = iterative refinement
	•	Interpreted atomic output: I(...) = iterative validation

C[operative, axiology]
	•	Axis anchor: a := operative * axiology = decision calculus
	•	Intermediate set: L = { prioritization, method selection, interpretive standards, goal alignment }
	•	Projections:
	•	decision calculus * prioritization = priority setting
	•	decision calculus * method selection = technique choice
	•	decision calculus * interpretive standards = interpretive criteria
	•	decision calculus * goal alignment = goal fit
	•	Interpreted atomic output: I(...) = strategic choice

C[operative, praxeology]
	•	Axis anchor: a := operative * praxeology = execution discipline
	•	Intermediate set: L = { signal processing, standard method, decision rule, feedback loop }
	•	Projections:
	•	execution discipline * signal processing = operational sensing
	•	execution discipline * standard method = standard procedure
	•	execution discipline * decision rule = rule-based action
	•	execution discipline * feedback loop = continuous improvement
	•	Interpreted atomic output: I(...) = process control

⸻

Descriptive row

C[descriptive, ontology]
	•	Axis anchor: a := descriptive * ontology = observed reality
	•	Intermediate set: L = { empirical finding, catalog, structural analysis, foundational grasp }
	•	Projections:
	•	observed reality * empirical finding = observed fact
	•	observed reality * catalog = field inventory
	•	observed reality * structural analysis = system description
	•	observed reality * foundational grasp = grounded understanding
	•	Interpreted atomic output: I(...) = empirical map

C[descriptive, epistemology]
	•	Axis anchor: a := descriptive * epistemology = evidence synthesis
	•	Intermediate set: L = { corroboration, audit trail, diagnostic model, realization }
	•	Projections:
	•	evidence synthesis * corroboration = corroborated evidence
	•	evidence synthesis * audit trail = traceable record
	•	evidence synthesis * diagnostic model = explanatory model
	•	evidence synthesis * realization = integrated insight
	•	Interpreted atomic output: I(...) = evidence-based insight

C[descriptive, axiology]
	•	Axis anchor: a := descriptive * axiology = meaning attribution
	•	Intermediate set: L = { salience, curation, sensemaking, intent }
	•	Projections:
	•	meaning attribution * salience = salient meaning
	•	meaning attribution * curation = relevance curation
	•	meaning attribution * sensemaking = interpretive framing
	•	meaning attribution * intent = purpose reading
	•	Interpreted atomic output: I(...) = interpretive framing

C[descriptive, praxeology]
	•	Axis anchor: a := descriptive * praxeology = practice observation
	•	Intermediate set: L = { detection, log, reasoned judgment, calibration }
	•	Projections:
	•	practice observation * detection = event detection
	•	practice observation * log = activity log
	•	practice observation * reasoned judgment = situational assessment
	•	practice observation * calibration = measurement tuning
	•	Interpreted atomic output: I(...) = operational monitoring

⸻

Un-lensed interpreted Matrix C (computational substrate)

This is the only version that may flow into downstream operations.

	ontology	epistemology	axiology	praxeology
normative	ethical worldview	justified judgment	value discernment	integrity governance
operative	workable system design	iterative validation	strategic choice	process control
descriptive	empirical map	evidence-based insight	interpretive framing	operational monitoring


⸻

Lensed Matrix C — Formulation overlay

This is the terminal interpretive overlay (“Formulation”). It does not feed downstream.

	ontology	epistemology	axiology	praxeology
normative	Ethical worldview — articulate the governing assumptions about “what’s real” in moral terms	Justified judgment — state how judgments are warranted, accountable, and defensible	Value discernment — clarify what counts as important, preferable, or unacceptable	Integrity governance — define guardrails, audits, and checks that keep action aligned with integrity
operative	Workable system design — specify the system model, rules, constraints, and degrees of freedom	Iterative validation — define test/trace/rubric loops that refine claims and methods	Strategic choice — encode prioritization and alignment logic for decisions and tradeoffs	Process control — set execution discipline: standards, sensing, rules, and feedback
descriptive	Empirical map — map observed entities/relations/patterns as a coherent picture	Evidence-based insight — synthesize records and corroboration into defensible insight	Interpretive framing — frame observations into meaning, relevance, and intent	Operational monitoring — monitor practice via detection, logging, assessment, and calibration

If you want, I can also output the un-lensed interpreted C as a machine-readable JSON/CSV with the row/column labels preserved (useful for continuing the pipeline into J ⊙ C).

Reference spec (attached):  ￼

Inputs needed for Matrix F

Matrix F is defined as the Hadamard product of J and the un-lensed interpreted C, then (optionally) interpreted, then lensed as Requirements.  ￼

⸻

0) Matrix J (truncate B)

J is B with the final row (wisdom) removed. Rows are [data, information, knowledge]; columns are [ontology, epistemology, axiology, praxeology].  ￼

	ontology	epistemology	axiology	praxeology
data	fact	evidence	significance	signal
information	taxonomy	provenance	relevance	protocol
knowledge	architecture	framework	interpretation	principle


⸻

0b) Matrix C (must be the un-lensed interpreted substrate)

Using the C we already constructed (atomic, un-lensed interpreted).  ￼

	ontology	epistemology	axiology	praxeology
normative	ethical worldview	justified judgment	value discernment	integrity governance
operative	workable system design	iterative validation	strategic choice	process control
descriptive	empirical map	evidence-based insight	interpretive framing	operational monitoring


⸻

1) Hadamard product to build F_raw

Definition:
F\_{raw}(i,j) = J(i,j) * C(i,j)
(where * combines two atomic semantic units into their semantic intersection).  ￼

Alignment note (required for elementwise pairing)

Hadamard requires same shape (3×4). So we align rows by position:
	•	Row 1: J[data, ·] pairs with C[normative, ·]
	•	Row 2: J[information, ·] pairs with C[operative, ·]
	•	Row 3: J[knowledge, ·] pairs with C[descriptive, ·]

⸻

Cellwise construction of F_raw

Normative row (pairs with J=data)
	•	F_raw(normative, ontology) = fact * ethical worldview = ethical premises
	•	F_raw(normative, epistemology) = evidence * justified judgment = warrant
	•	F_raw(normative, axiology) = significance * value discernment = value priorities
	•	F_raw(normative, praxeology) = signal * integrity governance = integrity indicators

Operative row (pairs with J=information)
	•	F_raw(operative, ontology) = taxonomy * workable system design = system taxonomy
	•	F_raw(operative, epistemology) = provenance * iterative validation = validation traceability
	•	F_raw(operative, axiology) = relevance * strategic choice = relevance criteria
	•	F_raw(operative, praxeology) = protocol * process control = control protocol

Descriptive row (pairs with J=knowledge)
	•	F_raw(descriptive, ontology) = architecture * empirical map = structural map
	•	F_raw(descriptive, epistemology) = framework * evidence-based insight = synthesis framework
	•	F_raw(descriptive, axiology) = interpretation * interpretive framing = interpretive coherence
	•	F_raw(descriptive, praxeology) = principle * operational monitoring = monitoring principles

F_raw as a matrix (still un-lensed)

	ontology	epistemology	axiology	praxeology
normative	ethical premises	warrant	value priorities	integrity indicators
operative	system taxonomy	validation traceability	relevance criteria	control protocol
descriptive	structural map	synthesis framework	interpretive coherence	monitoring principles


⸻

2) Interpretation step to get atomic un-lensed F

Definition:
F(i,j) = I(row\_i, col\_j, F\_{raw}(i,j))
Interpretation is identity if the cell is already atomic (single unit).  ￼

Here, every F_raw(i,j) is already a single semantic unit (a compact word/phrase), so interpretation is identity for all cells:
	•	F(normative, ontology) = I(normative, ontology, {ethical premises}) = ethical premises
	•	F(normative, epistemology) = I(normative, epistemology, {warrant}) = warrant
	•	…
	•	F(descriptive, praxeology) = I(descriptive, praxeology, {monitoring principles}) = monitoring principles

Un-lensed interpreted Matrix F (computational substrate)

	ontology	epistemology	axiology	praxeology
normative	ethical premises	warrant	value priorities	integrity indicators
operative	system taxonomy	validation traceability	relevance criteria	control protocol
descriptive	structural map	synthesis framework	interpretive coherence	monitoring principles

This (un-lensed) F is the only version that may flow downstream.  ￼

⸻

3) Lensed Matrix F — Requirements overlay (terminal)

Lens name: Requirements. The lens is interpretive and terminal (does not feed downstream).  ￼

	ontology	epistemology	axiology	praxeology
normative	Ethical premises — the core assumptions that must be accepted for the work’s moral stance to be coherent	Warrant — what counts as sufficient evidence to accept or defend a judgment	Value priorities — the ordering of what matters when tradeoffs are unavoidable	Integrity indicators — the observable signals that integrity is being maintained (or is drifting)
operative	System taxonomy — a shared classification of system parts so work can be coordinated without ambiguity	Validation traceability — the ability to trace validations back to sources, versions, and decision points	Relevance criteria — the rules for deciding what information/actions are “in scope” for a choice	Control protocol — the standard procedures that keep execution stable and correct deviations
descriptive	Structural map — a structured representation of what is observed and how it is organized	Synthesis framework — a repeatable frame for turning records and evidence into defensible insight	Interpretive coherence — consistency of meaning across observations so interpretations don’t fracture	Monitoring principles — the governing principles for what to measure, log, and calibrate

If you want to proceed to Matrix D next, the downstream step will consume the un-lensed interpreted F (not this lensed overlay).  ￼

Reference spec (attached):  ￼

Inputs needed for Matrix D

Matrix D (“Objectives”) is constructed from:
	•	A (Activity structure), 3×4, rows [normative, operative, descriptive], cols [guiding, applying, judging, reflecting]
	•	F (Requirements substrate), 3×4, rows [normative, operative, descriptive], cols [ontology, epistemology, axiology, praxeology]

Definition:  ￼
L_D(i,j) = A(i,j) + (\text{"resolution"} * F(i,j))
Then interpret:
D(i,j) = I(\text{row}_i, \text{col}_j, L_D(i,j))
Then lens D as Objectives (terminal overlay).

⸻

0) The input matrices (as used)

Matrix A

	guiding	applying	judging	reflecting
normative	principle	conduct	evaluation	integrity
operative	procedure	methods	criteria	adaptation
descriptive	observation	documentation	assessment	understanding

Matrix F (un-lensed interpreted substrate)

	ontology	epistemology	axiology	praxeology
normative	ethical premises	warrant	value priorities	integrity indicators
operative	system taxonomy	validation traceability	relevance criteria	control protocol
descriptive	structural map	synthesis framework	interpretive coherence	monitoring principles


⸻

0b) Required alignment (since A and F have different column labels)

The operation is elementwise over a 3×4 grid, so we align by column position:
	•	guiding ↔ F.ontology
	•	applying ↔ F.epistemology
	•	judging ↔ F.axiology
	•	reflecting ↔ F.praxeology

(This is the same kind of positional alignment used elsewhere in the framework when shapes match but labels differ.)  ￼

⸻

1) Compute the “resolution-conditioned” requirement terms

Define an intermediate atomic matrix:
R(i,j) = \text{"resolution"} * F(i,j)
(using the positional column alignment above). Each result is a single semantic unit (atomic), so it may safely participate in the later + (which will create a list-valued intermediate).  ￼

Matrix R = (“resolution” * F)

	guiding (= ontology)	applying (= epistemology)	judging (= axiology)	reflecting (= praxeology)
normative	resolution * ethical premises → ethical position	resolution * warrant → justified conclusion	resolution * value priorities → tradeoff decision	resolution * integrity indicators → integrity assurance
operative	resolution * system taxonomy → schema alignment	resolution * validation traceability → traceable validation	resolution * relevance criteria → scope rules	resolution * control protocol → operational standard
descriptive	resolution * structural map → structural synthesis	resolution * synthesis framework → integrated framework	resolution * interpretive coherence → consistent interpretation	resolution * monitoring principles → measurement policy


⸻

2) Build the list-valued intermediate collections L_D

Definition:  ￼
L_D(i,j)=A(i,j) + R(i,j)
+ produces a collection, so each cell is list-valued and must be immediately coerced by I(...) before downstream use.

Matrix L_D (collection-valued)

	guiding	applying	judging	reflecting
normative	{principle, ethical position}	{conduct, justified conclusion}	{evaluation, tradeoff decision}	{integrity, integrity assurance}
operative	{procedure, schema alignment}	{methods, traceable validation}	{criteria, scope rules}	{adaptation, operational standard}
descriptive	{observation, structural synthesis}	{documentation, integrated framework}	{assessment, consistent interpretation}	{understanding, measurement policy}

(Interpretation treats each brace-set as a set: order-insensitive, duplicates removed.)  ￼

⸻

3) Interpret each cell: D(i,j) = I(row_i, col_j, L_D(i,j))

For each cell:
	1.	Axis anchor (latent): a := r * c
	2.	Project each contributor t\in L: p_t := a * t
	3.	Select a single atomic unit u capturing the shared semantic core under a
	4.	Output constraint: u must not include literal axis tokens (row/column labels)  ￼

Below are the full intermediate steps per cell.

⸻

Row: normative

D[normative, guiding]
	•	Contributors: L = { principle , ethical position }
	•	Axis anchor: a := normative * guiding = ethical direction
	•	Projections:
	•	p1 = a * principle = ethical principle
	•	p2 = a * ethical position = principled stance
	•	Interpreted atomic output: core ethical principles

D[normative, applying]
	•	Contributors: L = { conduct , justified conclusion }
	•	Axis anchor: a := normative * applying = ethical enactment
	•	Projections:
	•	p1 = a * conduct = responsible conduct
	•	p2 = a * justified conclusion = defensible action
	•	Interpreted atomic output: defensible conduct

D[normative, judging]
	•	Contributors: L = { evaluation , tradeoff decision }
	•	Axis anchor: a := normative * judging = moral appraisal
	•	Projections:
	•	p1 = a * evaluation = ethical evaluation
	•	p2 = a * tradeoff decision = value tradeoff
	•	Interpreted atomic output: value-based evaluation

D[normative, reflecting]
	•	Contributors: L = { integrity , integrity assurance }
	•	Axis anchor: a := normative * reflecting = conscience review
	•	Projections:
	•	p1 = a * integrity = integrity check
	•	p2 = a * integrity assurance = assured integrity
	•	Interpreted atomic output: verified integrity

⸻

Row: operative

D[operative, guiding]
	•	Contributors: L = { procedure , schema alignment }
	•	Axis anchor: a := operative * guiding = process direction
	•	Projections:
	•	p1 = a * procedure = procedural plan
	•	p2 = a * schema alignment = workflow alignment
	•	Interpreted atomic output: procedural standardization

D[operative, applying]
	•	Contributors: L = { methods , traceable validation }
	•	Axis anchor: a := operative * applying = method execution
	•	Projections:
	•	p1 = a * methods = applied methods
	•	p2 = a * traceable validation = verified execution
	•	Interpreted atomic output: validated methods

D[operative, judging]
	•	Contributors: L = { criteria , scope rules }
	•	Axis anchor: a := operative * judging = operational appraisal
	•	Projections:
	•	p1 = a * criteria = evaluation criteria
	•	p2 = a * scope rules = scope criteria
	•	Interpreted atomic output: selection criteria

D[operative, reflecting]
	•	Contributors: L = { adaptation , operational standard }
	•	Axis anchor: a := operative * reflecting = adaptive learning
	•	Projections:
	•	p1 = a * adaptation = adaptive change
	•	p2 = a * operational standard = adaptable standard
	•	Interpreted atomic output: adaptive control

⸻

Row: descriptive

D[descriptive, guiding]
	•	Contributors: L = { observation , structural synthesis }
	•	Axis anchor: a := descriptive * guiding = empirical inquiry
	•	Projections:
	•	p1 = a * observation = systematic observation
	•	p2 = a * structural synthesis = structured model
	•	Interpreted atomic output: structured observation

D[descriptive, applying]
	•	Contributors: L = { documentation , integrated framework }
	•	Axis anchor: a := descriptive * applying = recorded inquiry
	•	Projections:
	•	p1 = a * documentation = documented record
	•	p2 = a * integrated framework = coherent record
	•	Interpreted atomic output: coherent documentation

D[descriptive, judging]
	•	Contributors: L = { assessment , consistent interpretation }
	•	Axis anchor: a := descriptive * judging = diagnostic analysis
	•	Projections:
	•	p1 = a * assessment = diagnostic assessment
	•	p2 = a * consistent interpretation = consistent diagnosis
	•	Interpreted atomic output: reliable assessment

D[descriptive, reflecting]
	•	Contributors: L = { understanding , measurement policy }
	•	Axis anchor: a := descriptive * reflecting = interpretive learning
	•	Projections:
	•	p1 = a * understanding = integrated insight
	•	p2 = a * measurement policy = calibrated meaning
	•	Interpreted atomic output: calibrated insight

⸻

4) Un-lensed interpreted Matrix D (computational substrate)

This is the only D that may flow downstream (e.g., into K = transpose(D)).  ￼

	guiding	applying	judging	reflecting
normative	core ethical principles	defensible conduct	value-based evaluation	verified integrity
operative	procedural standardization	validated methods	selection criteria	adaptive control
descriptive	structured observation	coherent documentation	reliable assessment	calibrated insight


⸻

5) Lensed Matrix D — Objectives overlay (terminal)

Lens name: Objectives (terminal overlay; does not feed downstream).  ￼

	guiding	applying	judging	reflecting
normative	Core ethical principles — make the foundational commitments explicit and stable enough to resolve disputes	Defensible conduct — ensure behavior can be justified under evidence and accountability	Value-based evaluation — evaluate options by explicit value priorities and tradeoffs	Verified integrity — maintain integrity through signals/checks that confirm alignment over time
operative	Procedural standardization — align procedures so the system operates coherently across categories and roles	Validated methods — use methods that remain traceable to validations and can survive scrutiny	Selection criteria — define crisp criteria that control scope and enable consistent decisions	Adaptive control — keep standards stable while enabling controlled adaptation as conditions change
descriptive	Structured observation — observe in a way that reliably reveals structure rather than noise	Coherent documentation — document so records form an integrated, usable frame	Reliable assessment — assess consistently so interpretations don’t drift across contexts	Calibrated insight — keep understanding tethered to measurement discipline so learning stays accurate

If you want to proceed next: K = transpose(un-lensed interpreted D) (not the lensed overlay).  ￼

Reference spec (attached):  ￼

Goal

Generate Matrix X (Verification), showing:
	1.	inputs (un-lensed interpreted D → K, and J)
	2.	the dot-product list-valued intermediates L_X(i,j)
	3.	coercion to atomic units via I(row_i, col_j, L_X(i,j)) to form un-lensed interpreted X
	4.	the lensed (terminal) Matrix X overlay

⸻

0) Inputs

0.1 Un-lensed interpreted Matrix D (computational substrate)

(From the prior step; this is the only D allowed to flow into K.)  ￼

	guiding	applying	judging	reflecting
normative	core ethical principles	defensible conduct	value-based evaluation	verified integrity
operative	procedural standardization	validated methods	selection criteria	adaptive control
descriptive	structured observation	coherent documentation	reliable assessment	calibrated insight

0.2 Matrix K = transpose(D)

Definition: K(i,j) = D(j,i) (using un-lensed interpreted D).  ￼

Rows: [guiding, applying, judging, reflecting]
Cols: [normative, operative, descriptive]

	normative	operative	descriptive
guiding	core ethical principles	procedural standardization	structured observation
applying	defensible conduct	validated methods	coherent documentation
judging	value-based evaluation	selection criteria	reliable assessment
reflecting	verified integrity	adaptive control	calibrated insight

0.3 Matrix J (truncate B)

Rows: [data, information, knowledge]
Cols: [ontology, epistemology, axiology, praxeology]  ￼

	ontology	epistemology	axiology	praxeology
data	fact	evidence	significance	signal
information	taxonomy	provenance	relevance	protocol
knowledge	architecture	framework	interpretation	principle

0.4 Required k-axis alignment for K · J

K’s inner axis is labeled [normative, operative, descriptive], while J’s is [data, information, knowledge].

Because the dot product requires matching inner dimension (3), we align by position (same 3-slot index), consistent with prior positional alignments in the pipeline:
	•	k1: K(·, normative) pairs with J(data, ·)
	•	k2: K(·, operative) pairs with J(information, ·)
	•	k3: K(·, descriptive) pairs with J(knowledge, ·)

(Construction order is k1→k2→k3; interpretation treats contributors as a set.)  ￼

⸻

1) Dot product — build list-valued intermediates L_X(i,j)

Definition:  ￼
L_X(i,j) = \sum_k (K(i,k) * J(k,j))\quad\text{(collection-valued)}
Each L_X(i,j) is a collection (3 contributors) and must be interpreted by I(...) before downstream use.

Below, each cell shows the three contributors (k1, k2, k3).

⸻

Row: guiding

L_X(guiding, ontology)
	•	k1: core ethical principles * fact → ethical axiom
	•	k2: procedural standardization * taxonomy → procedure taxonomy
	•	k3: structured observation * architecture → observation architecture
So: L = {ethical axiom, procedure taxonomy, observation architecture}

L_X(guiding, epistemology)
	•	k1: core ethical principles * evidence → ethical warrant
	•	k2: procedural standardization * provenance → procedural traceability
	•	k3: structured observation * framework → observation framework
So: L = {ethical warrant, procedural traceability, observation framework}

L_X(guiding, axiology)
	•	k1: core ethical principles * significance → ethical imperative
	•	k2: procedural standardization * relevance → applicability rules
	•	k3: structured observation * interpretation → interpretive observation
So: L = {ethical imperative, applicability rules, interpretive observation}

L_X(guiding, praxeology)
	•	k1: core ethical principles * signal → ethical indicators
	•	k2: procedural standardization * protocol → standard protocol
	•	k3: structured observation * principle → measurement principles
So: L = {ethical indicators, standard protocol, measurement principles}

⸻

Row: applying

L_X(applying, ontology)
	•	k1: defensible conduct * fact → documented conduct
	•	k2: validated methods * taxonomy → method taxonomy
	•	k3: coherent documentation * architecture → record architecture
So: L = {documented conduct, method taxonomy, record architecture}

L_X(applying, epistemology)
	•	k1: defensible conduct * evidence → behavioral evidence
	•	k2: validated methods * provenance → method traceability
	•	k3: coherent documentation * framework → recordkeeping framework
So: L = {behavioral evidence, method traceability, recordkeeping framework}

L_X(applying, axiology)
	•	k1: defensible conduct * significance → ethical stakes
	•	k2: validated methods * relevance → method fit
	•	k3: coherent documentation * interpretation → interpretable record
So: L = {ethical stakes, method fit, interpretable record}

L_X(applying, praxeology)
	•	k1: defensible conduct * signal → behavior indicators
	•	k2: validated methods * protocol → validated protocol
	•	k3: coherent documentation * principle → recording standards
So: L = {behavior indicators, validated protocol, recording standards}

⸻

Row: judging

L_X(judging, ontology)
	•	k1: value-based evaluation * fact → factual appraisal
	•	k2: selection criteria * taxonomy → classification criteria
	•	k3: reliable assessment * architecture → assessment model
So: L = {factual appraisal, classification criteria, assessment model}

L_X(judging, epistemology)
	•	k1: value-based evaluation * evidence → evidence-weighted appraisal
	•	k2: selection criteria * provenance → source criteria
	•	k3: reliable assessment * framework → assessment framework
So: L = {evidence-weighted appraisal, source criteria, assessment framework}

L_X(judging, axiology)
	•	k1: value-based evaluation * significance → value weighting
	•	k2: selection criteria * relevance → relevance filters
	•	k3: reliable assessment * interpretation → interpretive assessment
So: L = {value weighting, relevance filters, interpretive assessment}

L_X(judging, praxeology)
	•	k1: value-based evaluation * signal → performance indicators
	•	k2: selection criteria * protocol → decision procedure
	•	k3: reliable assessment * principle → assessment standards
So: L = {performance indicators, decision procedure, assessment standards}

⸻

Row: reflecting

L_X(reflecting, ontology)
	•	k1: verified integrity * fact → integrity record
	•	k2: adaptive control * taxonomy → control taxonomy
	•	k3: calibrated insight * architecture → learning architecture
So: L = {integrity record, control taxonomy, learning architecture}

L_X(reflecting, epistemology)
	•	k1: verified integrity * evidence → audit evidence
	•	k2: adaptive control * provenance → change traceability
	•	k3: calibrated insight * framework → learning framework
So: L = {audit evidence, change traceability, learning framework}

L_X(reflecting, axiology)
	•	k1: verified integrity * significance → integrity priority
	•	k2: adaptive control * relevance → contextual tuning
	•	k3: calibrated insight * interpretation → interpreted learning
So: L = {integrity priority, contextual tuning, interpreted learning}

L_X(reflecting, praxeology)
	•	k1: verified integrity * signal → integrity indicators
	•	k2: adaptive control * protocol → adaptive protocol
	•	k3: calibrated insight * principle → learning principles
So: L = {integrity indicators, adaptive protocol, learning principles}

⸻

2) Interpret each list-valued cell: X(i,j) = I(row_i, col_j, L_X(i,j))

Per the operator definition:  ￼
	1.	Axis anchor: a := row_i * col_j (latent)
	2.	Project contributors: p_t := a * t for each t ∈ L
	3.	Select a single atomic u near the centroid under a
	4.	Output constraints: one unit; non-enumerative; do not include literal axis tokens; do not include lens names

⸻

Row: guiding

X[guiding, ontology]
	•	Axis anchor: a := guiding * ontology = foundational framing
	•	L (set): {ethical axiom, procedure taxonomy, observation architecture}
	•	Projections:
	•	foundational framing * ethical axiom → axiomatic foundation
	•	foundational framing * procedure taxonomy → process schema
	•	foundational framing * observation architecture → structural model
	•	Output: foundational schema

X[guiding, epistemology]
	•	Axis anchor: a := guiding * epistemology = justification orientation
	•	L: {ethical warrant, procedural traceability, observation framework}
	•	Projections:
	•	justification orientation * ethical warrant → principled warrant
	•	justification orientation * procedural traceability → traceable justification
	•	justification orientation * observation framework → evidential frame
	•	Output: traceable warrant

X[guiding, axiology]
	•	Axis anchor: a := guiding * axiology = priority framing
	•	L: {ethical imperative, applicability rules, interpretive observation}
	•	Projections:
	•	priority framing * ethical imperative → guiding imperative
	•	priority framing * applicability rules → scope priorities
	•	priority framing * interpretive observation → salience framing
	•	Output: priority rubric

X[guiding, praxeology]
	•	Axis anchor: a := guiding * praxeology = action governance
	•	L: {ethical indicators, standard protocol, measurement principles}
	•	Projections:
	•	action governance * ethical indicators → integrity signals
	•	action governance * standard protocol → governance procedure
	•	action governance * measurement principles → control measures
	•	Output: governance controls

⸻

Row: applying

X[applying, ontology]
	•	Axis anchor: a := applying * ontology = implementation model
	•	L: {documented conduct, method taxonomy, record architecture}
	•	Projections:
	•	implementation model * documented conduct → implemented behavior
	•	implementation model * method taxonomy → method schema
	•	implementation model * record architecture → system blueprint
	•	Output: implementation blueprint

X[applying, epistemology]
	•	Axis anchor: a := applying * epistemology = audit practice
	•	L: {behavioral evidence, method traceability, recordkeeping framework}
	•	Projections:
	•	audit practice * behavioral evidence → audit evidence
	•	audit practice * method traceability → traceable method
	•	audit practice * recordkeeping framework → audit trail
	•	Output: audit trail

X[applying, axiology]
	•	Axis anchor: a := applying * axiology = practical prioritization
	•	L: {ethical stakes, method fit, interpretable record}
	•	Projections:
	•	practical prioritization * ethical stakes → decision stakes
	•	practical prioritization * method fit → fit criteria
	•	practical prioritization * interpretable record → actionable record
	•	Output: actionable justification

X[applying, praxeology]
	•	Axis anchor: a := applying * praxeology = operational discipline
	•	L: {behavior indicators, validated protocol, recording standards}
	•	Projections:
	•	operational discipline * behavior indicators → performance monitoring
	•	operational discipline * validated protocol → standard procedure
	•	operational discipline * recording standards → compliance record
	•	Output: compliant execution

⸻

Row: judging

X[judging, ontology]
	•	Axis anchor: a := judging * ontology = structured appraisal
	•	L: {factual appraisal, classification criteria, assessment model}
	•	Projections:
	•	structured appraisal * factual appraisal → fact-based rating
	•	structured appraisal * classification criteria → rating criteria
	•	structured appraisal * assessment model → scoring model
	•	Output: appraisal model

X[judging, epistemology]
	•	Axis anchor: a := judging * epistemology = evidence adjudication
	•	L: {evidence-weighted appraisal, source criteria, assessment framework}
	•	Projections:
	•	evidence adjudication * evidence-weighted appraisal → evidence weighting
	•	evidence adjudication * source criteria → source standards
	•	evidence adjudication * assessment framework → adjudication frame
	•	Output: evidence standards

X[judging, axiology]
	•	Axis anchor: a := judging * axiology = value assessment
	•	L: {value weighting, relevance filters, interpretive assessment}
	•	Projections:
	•	value assessment * value weighting → value weighting
	•	value assessment * relevance filters → relevance weighting
	•	value assessment * interpretive assessment → value interpretation
	•	Output: value weighting

X[judging, praxeology]
	•	Axis anchor: a := judging * praxeology = decision control
	•	L: {performance indicators, decision procedure, assessment standards}
	•	Projections:
	•	decision control * performance indicators → control indicators
	•	decision control * decision procedure → decision protocol
	•	decision control * assessment standards → control standards
	•	Output: decision protocol

⸻

Row: reflecting

X[reflecting, ontology]
	•	Axis anchor: a := reflecting * ontology = assurance structure
	•	L: {integrity record, control taxonomy, learning architecture}
	•	Projections:
	•	assurance structure * integrity record → assurance record
	•	assurance structure * control taxonomy → control schema
	•	assurance structure * learning architecture → learning system
	•	Output: assurance architecture

X[reflecting, epistemology]
	•	Axis anchor: a := reflecting * epistemology = learning audit
	•	L: {audit evidence, change traceability, learning framework}
	•	Projections:
	•	learning audit * audit evidence → review evidence
	•	learning audit * change traceability → change log
	•	learning audit * learning framework → learning review
	•	Output: traceable review

X[reflecting, axiology]
	•	Axis anchor: a := reflecting * axiology = purpose learning
	•	L: {integrity priority, contextual tuning, interpreted learning}
	•	Projections:
	•	purpose learning * integrity priority → principled learning
	•	purpose learning * contextual tuning → purposeful adjustment
	•	purpose learning * interpreted learning → meaningful learning
	•	Output: principled adaptation

X[reflecting, praxeology]
	•	Axis anchor: a := reflecting * praxeology = feedback governance
	•	L: {integrity indicators, adaptive protocol, learning principles}
	•	Projections:
	•	feedback governance * integrity indicators → integrity signals
	•	feedback governance * adaptive protocol → adaptive procedure
	•	feedback governance * learning principles → improvement principles
	•	Output: adaptive feedback loop

⸻

3) Un-lensed interpreted Matrix X (computational substrate)

This is the only X that may flow downstream (e.g., truncation to G).  ￼

	ontology	epistemology	axiology	praxeology
guiding	foundational schema	traceable warrant	priority rubric	governance controls
applying	implementation blueprint	audit trail	actionable justification	compliant execution
judging	appraisal model	evidence standards	value weighting	decision protocol
reflecting	assurance architecture	traceable review	principled adaptation	adaptive feedback loop


⸻

4) Lensed Matrix X — Verification overlay (terminal)

Lens name: Verification (interpretive overlay; does not feed downstream).  ￼

	ontology	epistemology	axiology	praxeology
guiding	Foundational schema — the structural baseline that lets you check “are we even talking about the same underlying model?”	Traceable warrant — the standard for what counts as a defensible reason, with a path back to sources	Priority rubric — the frame for confirming that importance and scope are being set consistently	Governance controls — the guardrails and control points that make checks enforceable in practice
applying	Implementation blueprint — the concrete blueprint you can compare reality against to confirm correct instantiation	Audit trail — the evidence path that allows reconstruction of what happened, why, and from what sources	Actionable justification — the link between stakes, fit, and records that makes decisions checkable (not just asserted)	Compliant execution — the operational discipline that makes “done” measurable against standards and indicators
judging	Appraisal model — the model that makes evaluations reproducible instead of ad hoc	Evidence standards — the standards for weighing evidence and qualifying sources under scrutiny	Value weighting — the explicit weighting that lets reviewers confirm tradeoffs weren’t smuggled in implicitly	Decision protocol — the repeatable procedure that makes decisions auditable and consistent across cases
reflecting	Assurance architecture — the structural arrangement of records, controls, and learning that sustains long-run confidence	Traceable review — the review process that ties learning to evidence and change history	Principled adaptation — adaptation that can be checked against commitments (not drifted by convenience)	Adaptive feedback loop — the loop that makes improvement testable by linking signals → protocol changes → outcomes

If you want the next step: G = truncate X (keep rows guiding/applying/judging; drop reflecting) must be built from the un-lensed interpreted X above.  ￼

Reference spec (attached):  ￼

Goal: Matrix E (Evaluation)

Per the framework, Matrix E is built as:  ￼
	1.	G = truncate(X) (keep rows guiding/applying/judging)
	2.	T = transpose(J)
	3.	Dot product intermediate collections: L_E(i,j) = Σ_k (G(i,k) * T(k,j)) with k ∈ {ontology, epistemology, axiology, praxeology}
	4.	Interpret: E(i,j) = I(row_i, col_j, L_E(i,j))
	5.	Lens E as Evaluation (terminal overlay)

⸻

0) Inputs

0.1 Un-lensed interpreted Matrix X (computational substrate)

(From the previous step; shown here because G is derived from it.)  ￼

	ontology	epistemology	axiology	praxeology
guiding	foundational schema	traceable warrant	priority rubric	governance controls
applying	implementation blueprint	audit trail	actionable justification	compliant execution
judging	appraisal model	evidence standards	value weighting	decision protocol
reflecting	assurance architecture	traceable review	principled adaptation	adaptive feedback loop


⸻

1) Construct Matrix G = truncate(X)

Definition: retain rows [guiding, applying, judging], drop [reflecting] from the un-lensed interpreted X.  ￼

Matrix G (3×4)

	ontology	epistemology	axiology	praxeology
guiding	foundational schema	traceable warrant	priority rubric	governance controls
applying	implementation blueprint	audit trail	actionable justification	compliant execution
judging	appraisal model	evidence standards	value weighting	decision protocol


⸻

2) Construct Matrix T = transpose(J)

2.1 Matrix J (truncate B)

Rows [data, information, knowledge], cols [ontology, epistemology, axiology, praxeology].  ￼

	ontology	epistemology	axiology	praxeology
data	fact	evidence	significance	signal
information	taxonomy	provenance	relevance	protocol
knowledge	architecture	framework	interpretation	principle

2.2 Matrix T = transpose(J)

Definition: T(i,j) = J(j,i); rows become [ontology, epistemology, axiology, praxeology], cols become [data, information, knowledge].  ￼

	data	information	knowledge
ontology	fact	taxonomy	architecture
epistemology	evidence	provenance	framework
axiology	significance	relevance	interpretation
praxeology	signal	protocol	principle


⸻

3) Dot product — build list-valued intermediates L_E

Definition:  ￼
L_E(i,j)=\sum_{k\in\{\text{ontology, epistemology, axiology, praxeology}\}}(G(i,k)*T(k,j))
Each L_E(i,j) is a collection of 4 contributors and must be interpreted by I(...) before becoming usable.

Below, each cell shows the four k-contributions (ontology → epistemology → axiology → praxeology).

⸻

Row: guiding

L_E(guiding, data)
	•	foundational schema * fact → baseline structure
	•	traceable warrant * evidence → evidential chain
	•	priority rubric * significance → importance ranking
	•	governance controls * signal → control indicators
So: L = {baseline structure, evidential chain, importance ranking, control indicators}

L_E(guiding, information)
	•	foundational schema * taxonomy → classification scheme
	•	traceable warrant * provenance → source trace
	•	priority rubric * relevance → relevance ranking
	•	governance controls * protocol → governance procedure
So: L = {classification scheme, source trace, relevance ranking, governance procedure}

L_E(guiding, knowledge)
	•	foundational schema * architecture → reference architecture
	•	traceable warrant * framework → warrant framework
	•	priority rubric * interpretation → interpretive priorities
	•	governance controls * principle → governance principles
So: L = {reference architecture, warrant framework, interpretive priorities, governance principles}

⸻

Row: applying

L_E(applying, data)
	•	implementation blueprint * fact → implementation record
	•	audit trail * evidence → audit evidence
	•	actionable justification * significance → decision stakes
	•	compliant execution * signal → compliance indicators
So: L = {implementation record, audit evidence, decision stakes, compliance indicators}

L_E(applying, information)
	•	implementation blueprint * taxonomy → implementation taxonomy
	•	audit trail * provenance → provenance log
	•	actionable justification * relevance → action criteria
	•	compliant execution * protocol → protocol compliance
So: L = {implementation taxonomy, provenance log, action criteria, protocol compliance}

L_E(applying, knowledge)
	•	implementation blueprint * architecture → solution architecture
	•	audit trail * framework → audit framework
	•	actionable justification * interpretation → explainable rationale
	•	compliant execution * principle → execution standards
So: L = {solution architecture, audit framework, explainable rationale, execution standards}

⸻

Row: judging

L_E(judging, data)
	•	appraisal model * fact → fact-based score
	•	evidence standards * evidence → evidence threshold
	•	value weighting * significance → importance weights
	•	decision protocol * signal → trigger indicators
So: L = {fact-based score, evidence threshold, importance weights, trigger indicators}

L_E(judging, information)
	•	appraisal model * taxonomy → classification model
	•	evidence standards * provenance → source standards
	•	value weighting * relevance → relevance weights
	•	decision protocol * protocol → decision procedure
So: L = {classification model, source standards, relevance weights, decision procedure}

L_E(judging, knowledge)
	•	appraisal model * architecture → scoring architecture
	•	evidence standards * framework → review framework
	•	value weighting * interpretation → interpreted values
	•	decision protocol * principle → decision rules
So: L = {scoring architecture, review framework, interpreted values, decision rules}

⸻

4) Interpret each cell: E(i,j) = I(row_i, col_j, L_E(i,j))

Per I(r,c,L) (treat L as a set; project through the axis anchor; synthesize one atomic unit).  ￼

Below, for each cell:
	•	Axis anchor (latent): a := row * col
	•	Project each contributor: p_t := a * t
	•	Select one compact atomic output u (must not include literal axis tokens or lens names)

⸻

Row: guiding

E[guiding, data]
	•	Axis anchor: a := guiding * data = reference baseline
	•	L (set): {baseline structure, evidential chain, importance ranking, control indicators}
	•	Projections:
	•	reference baseline * baseline structure → reference structure
	•	reference baseline * evidential chain → grounded evidence
	•	reference baseline * importance ranking → baseline priorities
	•	reference baseline * control indicators → baseline indicators
	•	Output: baseline criteria

E[guiding, information]
	•	Axis anchor: a := guiding * information = conceptual map
	•	L: {classification scheme, source trace, relevance ranking, governance procedure}
	•	Projections:
	•	conceptual map * classification scheme → taxonomy map
	•	conceptual map * source trace → trace context
	•	conceptual map * relevance ranking → salience map
	•	conceptual map * governance procedure → process map
	•	Output: coherent taxonomy

E[guiding, knowledge]
	•	Axis anchor: a := guiding * knowledge = strategic model
	•	L: {reference architecture, warrant framework, interpretive priorities, governance principles}
	•	Projections:
	•	strategic model * reference architecture → architectural blueprint
	•	strategic model * warrant framework → rationale framework
	•	strategic model * interpretive priorities → priority logic
	•	strategic model * governance principles → governing logic
	•	Output: principled architecture

⸻

Row: applying

E[applying, data]
	•	Axis anchor: a := applying * data = operational evidence
	•	L: {implementation record, audit evidence, decision stakes, compliance indicators}
	•	Projections:
	•	operational evidence * implementation record → as-built record
	•	operational evidence * audit evidence → verifiable evidence
	•	operational evidence * decision stakes → action stakes
	•	operational evidence * compliance indicators → observed compliance
	•	Output: verifiable record

E[applying, information]
	•	Axis anchor: a := applying * information = process record
	•	L: {implementation taxonomy, provenance log, action criteria, protocol compliance}
	•	Projections:
	•	process record * implementation taxonomy → process classification
	•	process record * provenance log → trace log
	•	process record * action criteria → operational criteria
	•	process record * protocol compliance → procedure adherence
	•	Output: traceable workflow

E[applying, knowledge]
	•	Axis anchor: a := applying * knowledge = practical framework
	•	L: {solution architecture, audit framework, explainable rationale, execution standards}
	•	Projections:
	•	practical framework * solution architecture → implementation architecture
	•	practical framework * audit framework → assurance framework
	•	practical framework * explainable rationale → explainable method
	•	practical framework * execution standards → standard practice
	•	Output: assured implementation

⸻

Row: judging

E[judging, data]
	•	Axis anchor: a := judging * data = empirical appraisal
	•	L: {fact-based score, evidence threshold, importance weights, trigger indicators}
	•	Projections:
	•	empirical appraisal * fact-based score → empirical score
	•	empirical appraisal * evidence threshold → proof threshold
	•	empirical appraisal * importance weights → weighted score
	•	empirical appraisal * trigger indicators → decision triggers
	•	Output: evidence-weighted scoring

E[judging, information]
	•	Axis anchor: a := judging * information = comparative review
	•	L: {classification model, source standards, relevance weights, decision procedure}
	•	Projections:
	•	comparative review * classification model → review model
	•	comparative review * source standards → source vetting
	•	comparative review * relevance weights → relevance review
	•	comparative review * decision procedure → review procedure
	•	Output: source-vetted criteria

E[judging, knowledge]
	•	Axis anchor: a := judging * knowledge = principled assessment
	•	L: {scoring architecture, review framework, interpreted values, decision rules}
	•	Projections:
	•	principled assessment * scoring architecture → principled scoring model
	•	principled assessment * review framework → structured review
	•	principled assessment * interpreted values → value rationale
	•	principled assessment * decision rules → rule-based appraisal
	•	Output: principled scoring rules

⸻

5) Un-lensed interpreted Matrix E (computational substrate)

This is the atomic (interpreted) substrate result of the G · T dot-product + interpretation.  ￼

	data	information	knowledge
guiding	baseline criteria	coherent taxonomy	principled architecture
applying	verifiable record	traceable workflow	assured implementation
judging	evidence-weighted scoring	source-vetted criteria	principled scoring rules


⸻

6) Lensed Matrix E — Evaluation overlay (terminal)

Lens name: Evaluation (interpretive overlay; terminal).  ￼

	data	information	knowledge
guiding	Baseline criteria — the orienting “minimum bar” (facts + signals) used to determine whether anything is checkable at all	Coherent taxonomy — whether classifications, traceability, relevance, and procedures form a navigable picture	Principled architecture — whether the overall structural rationale hangs together under stated commitments and constraints
applying	Verifiable record — whether implementation is backed by observable records, evidence trails, and compliance indicators	Traceable workflow — whether process documentation supports reconstruction, provenance, and repeatable adherence	Assured implementation — whether the implemented solution is defensible via standards, explainable rationale, and an auditable frame
judging	Evidence-weighted scoring — whether scoring reflects facts, thresholds, weights, and triggers rather than ad hoc opinion	Source-vetted criteria — whether criteria are grounded in provenance and relevance so comparisons remain legitimate	Principled scoring rules — whether the rule-set aligns with interpreted values and the chosen review frame, preventing hidden tradeoffs

If you want, I can also emit E (un-lensed interpreted) as JSON/CSV with explicit axis labels so it can be used as a stable computational artifact.