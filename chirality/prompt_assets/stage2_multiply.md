## Input
- Raw k-products: {{raw_products}}

## Semantic Operations

Semantic operations are the actions you perform as an LLM to resolve meanings from the given prompt. Your task is all about **semantics** and nothing else.  This is about finding the right words, not performing the right mechanical actions that result in incoherence.  As such, these definitions for semantic operations are crucial to understand and correctly implement with the LLM doing the work of resolving meanings.

### Semantic Multiplication “ * “

Semantic multiplication (denoted by * ) means the semantics of the terms are resolved by combining the meaning of words into a coherent word or statement that represents the semantic intersection of those words (the meaning when combined together, not just adjoining the terms). This can even be done when the concept is a highly abstract word pairing because you are an LLM.

Examples:
"sufficient" * "reason" = "justification"
"desire" * "limitation" = “restraint”
“ocean" * "sofa" = “waterbed”
“clock" * "book" = “planner”
“fire" * "whisper" = “ember”
“language” * “  ?   " = "understanding”;  answer = "interpretation"
“deliverable" * "knowledge" * "documentation" = manual
“iterative" * "guiding" = “development”
"precision" * "durability" = "reliability"
"probability" * "consequence" = "risk"

### Semantic Addition “ + “

Semantic addition (denoted by + ) means simply concatenating words or sentence fragments together to form a longer statement. 
Example:
"faisal" + "has" + "seven" + "balloons" = faisal has seven balloons

There should not be an " + " operators remaining once the concatenation is done.

### Order of Operations

To resolve the final word string follow this order of operations:

1. Apply semantic multiplication first, 
2. then semantic addition 

## Output Format
Semantic Multiplication (*) resolves "Raw k-products" into a single, concise, intersection concept by combining the meanings under the active lenses; treat each word pair as a typed meet over sense-disambiguated labels, perform multiplication before any addition, and produce one head term or brief noun phrase that a domain expert in knowledge work would accept as the shared semantic core (not a list, not a paraphrase of inputs).

The answer should use the best words to concisely and coherently express the combined meaning, and the aim of generating reliable knowledge; do not add examples, caveats, meta-commentary, or lists—output one polished statement that best encompasses the meaning.