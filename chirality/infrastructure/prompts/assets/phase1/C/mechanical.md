## What is the Chirality Framework?

The Chirality Framework is a meta-ontological, system-agnostic methodology for mapping the solution space to a problem statement in the context of knowledge work. 

## What is it used for?

It is used to create a structured set of semantic relationships that have coherent meaning across the problem solving process and can be used as “semantic anchors” to guide an LLM across stages of solving a problem, traversing a “semantic valley”.

## Your Role as the LLM within the Chirality Framework

Clearly show how the elements transform according to the instructions.  There is a time to combine together statements precisely according to a strict procedure, and a time to interpret those statements within a given context.  Those times will be clearly identified by the user’s prompts.

## Semantic Operations

Semantic operations are the heart of the Chirality Framework. All the structure and specific details of format for the construction of the components in the framework are about **semantics** and nothing else.  This is about finding the right words, not performing the right mechanical actions that result in incoherence.  As such, these definitions for semantic operations are crucial to understand and correctly implement with the LLM doing the work of resolving meanings.

To provide an interpretation of these semantic dot product operators use the following definitions. 

### Semantic Multiplication “ * “

Semantic multiplication (denoted by * ) means the semantics of the terms are resolved by combining the meaning of words into a coherent word or statement that represents the semantic intersection of those words (the meaning when combined together, not just adjoining the terms). This can even be done when the concept is a highly abstract word pairing because you are an LLM.

Examples:
"sufficient" * "reason" = "justification"
"precision" * "durability" = "reliability"
"probability" * "consequence" = "risk"

### Semantic Addition “ + “

Semantic addition (denoted by + ) means simply concatenating words or sentence fragments together to form a longer statement. 
Example:
"faisal" + "has" + "seven" + "balloons" = faisal has seven balloons

### Order of Operations

First is ‘semantic multiplication’, second is ‘semantic addition’.

## The Semantic Valley: Sequence of Stations

The framework follows a logical progression of stations to generate reliable knowledge (semantic valley): if problem statement, then requirements, then objectives, then verification, then validation, then evaluation, then assessment, then implementation, then reflection and resolution.

1.  [A] · [B] = [C] : Problem Statement
2.  [C] ⊙ [J] = [F] : Requirements
3.  [A] + [F] = [D] : Objectives
4.  [K] · [J] = [X] : Verification
5.  [X]      -> [Z] : Validation
6.  [G] · [T] = [E] : Evaluation
7.  [R] × [E] = [M] : Assessment
8.  [M] × [X] = [W] : Implementation
9.  [W] × [P] = [U] : Reflection
10. [U] × [H] = [N] : Resolution

Next step is to begin the procedure for computing Matrix C.

----

## Canonical Matrix Definitions

I'm going to define some matrices that are used as ontologies for the problem solving space in knowledge work.  A semantic matrix applies modal ontologies to rows and columns, and the intersections all reflect the combined meaning of those two modalities.  Then the elements of a semantic matrix as situated in their respective ontology and instantiated in a particular subject.

## Matrix A
[A]
Size: 3x4
Station: Problem Statement
Column names: ['guiding', 'applying', 'judging', 'reflecting']
Row names: [‘normative’, ‘operative’, ‘iterative’]
Elements:
        [
            ["objectives", "actions", "benchmarks", "feedback"],
            ["standards", "methods", "criteria", "adaptation"],
            ["developments", "coordination", "evaluation", "refinement"],
        ]

          
## Matrix B 
[B]
Size: 4x4
Station: Problem Statement
Column names: [‘necessity (vs contingency)’, ‘sufficiency’, ‘completeness’, ‘consistency’]
Row names: [‘data', 'information', 'knowledge', 'wisdom']
Elements: [
            ["necessary", "sufficient", "complete", "consistent"],
            ["contingent", "actionable", "contextual", "congruent"],
            ["purposeful", "effective", "comprehensive", "coherent"],
            ["constitutive", "optimal", "holistic", "principled"],
          ]

----

## Constructing Matrix C 
## Matrix {{matrix_id}} 
[{{matrix_id}}]
{{station}}
Dimensions: {{n_rows}} × {{n_cols}} 
Row labels: {{rows_json}}
Column labels: {{cols_json}}
Elements:

[A] · [B] = [C]

This introduces the operator " · " as a semantic matrix dot product.

Matrix C is first made by the purely combinatorial first step of joining the elements of [A] and [B] in this manner: 

[
[A(1,1) * B(1,1) + A(1,2) * B(2,1) + A(1,3) * B(3,1) + A(1,4) * B(4,1)]
[A(1,1) * B(1,2) + A(1,2) * B(2,2) + A(1,3) * B(3,2) + A(1,4) * B(4,2)]
[A(1,1) * B(1,3) + A(1,2) * B(2,3) + A(1,3) * B(3,3) + A(1,4) * B(4,3)]
[A(1,1) * B(1,4) + A(1,2) * B(2,4) + A(1,3) * B(3,4) + A(1,4) * B(4,4)]

[A(2,1) * B(1,1) + A(2,2) * B(2,1) + A(2,3) * B(3,1) + A(2,4) * B(4,1)]
[A(2,1) * B(1,2) + A(2,2) * B(2,2) + A(2,3) * B(3,2) + A(2,4) * B(4,2)]
[A(2,1) * B(1,3) + A(2,2) * B(2,3) + A(2,3) * B(3,3) + A(2,4) * B(4,3)]
[A(2,1) * B(1,4) + A(2,2) * B(2,4) + A(2,3) * B(3,4) + A(2,4) * B(4,4)]

[A(3,1) * B(1,1) + A(3,2) * B(2,1) + A(3,3) * B(3,1) + A(3,4) * B(4,1)]
[A(3,1) * B(1,2) + A(3,2) * B(2,2) + A(3,3) * B(3,2) + A(3,4) * B(4,2)]
[A(3,1) * B(1,3) + A(3,2) * B(2,3) + A(3,3) * B(3,3) + A(3,4) * B(4,3)]
[A(3,1) * B(1,4) + A(3,2) * B(2,4) + A(3,3) * B(3,4) + A(3,4) * B(4,4)]
]

Generate this purely mechanical construction of word pairs and concatenations complete with the semantic operators in place ( * , + )

### Output format
Return **only** valid JSON in this shape:

{{json_tail}}