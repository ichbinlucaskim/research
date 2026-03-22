# Papers — Note-Taking Standard

This folder contains one subfolder per paper.
Every paper gets the same structured note. No exceptions.

The goal is not to summarize. The goal is to extract what is
architecturally useful, identify what the paper does not address,
and connect it to the rest of the reading list.

A note that cannot answer "how does this change how I would design
a system tomorrow" is incomplete.

---

## Folder Structure

```
papers/
├── README.md                        # This file
├── react-yao-2022/
│   ├── note.md                      # Your structured note (required)
│   ├── figures/                     # Key diagrams you redrew or annotated
│   └── refs.md                      # Papers this one cites that you should read next
├── chain-of-thought-wei-2022/
│   └── note.md
└── ...
```

Folder naming convention: `{short-title}-{first-author}-{year}`
Example: `lats-2023`, `memgpt-packer-2023`, `vllm-kwon-2023`

---

## note.md Template

Copy this exactly. Fill every section. Do not delete sections because
they feel hard to fill — that difficulty is the signal that you have
not understood the paper yet.

---

```markdown
# {Full Paper Title}

{Authors} | {Venue} | {Year} | {Link to paper}

Read: {YYYY-MM-DD}
Status: {Reading / Done / Needs Revisit}
Section: {Which section of the main README this belongs to}

---

## One-Line Claim

What does this paper claim to do, in one sentence?
Write this in your own words. Do not copy the abstract.

---

## Problem Being Solved

What specific limitation or gap does this paper address?
What was the state of the field before this paper, and why was
that insufficient?

Be concrete. Name the prior work being improved upon.

---

## Core Contribution

What is the single most important thing this paper introduces?
This could be:
- A new architecture or component
- A new training method
- A new benchmark or evaluation method
- A formal framework or taxonomy
- An empirical finding that changes assumptions

If there are multiple contributions, rank them. What would still
matter if everything else were stripped away?

---

## Architecture / Method

Describe how it works mechanically.

If there is a loop or pipeline, write it out step by step:
  Step 1: ...
  Step 2: ...
  Step 3: ...

If there are key design decisions (why did they choose X over Y),
explain the reasoning. This is often buried in ablation sections.

Include a diagram if one helps. Either reference a figure from the
paper or draw your own in ASCII or in the figures/ subfolder.

---

## Key Results

What did they actually show? Be specific about numbers and tasks.

Format:
- Task: {name}
- Baseline: {method} at {score}
- This paper: {method} at {score}
- Conditions: {dataset, model size, any important caveats}

If the result is benchmark-specific, note whether the benchmark
has known limitations or whether the improvement has been
reproduced elsewhere.

---

## Limitations and What It Does Not Address

This section is as important as the results section.

What assumptions does the method rely on?
What task types or conditions would cause it to fail?
What did the authors explicitly say they did not test?
What did the authors not say, but you suspect is a problem?

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| {paper name} | {this paper improves on / is improved by / contradicts / complements} |

After reading this paper, which papers in the reading list
should you re-read or read next? Why?

---

## Implementation Angles

Three specific ideas for how this paper's contribution could be
applied in your experiments or projects.

Each one should be concrete enough that you could start building
it tomorrow.

1. {Experiment or project idea}: {one sentence on what you would build
   and what you would measure or demonstrate}

2. {Experiment or project idea}: {same format}

3. {Experiment or project idea}: {same format}

---

## Open Questions

What do you still not understand after reading this?
What would you need to run to verify or challenge the claims?

List these. Come back to them after running related experiments.

---

## Revision Notes

{YYYY-MM-DD}: {What changed in your understanding after running
an experiment or reading a related paper}
```

---

## Quality Standard

A note is complete when it can do the following:

- Explain the paper's contribution to someone who has not read it,
  in under two minutes, without looking at your notes
- Identify at least one specific thing the paper does not solve
  that matters for your research
- Produce at least one concrete experiment idea

If any of these three are missing, the note is not done.

---

## Cross-Reference Index

Maintain this table at the bottom of this README as you add notes.
It gives you a quick map of how papers connect.

| Paper | Improves on | Improved by | Key concept introduced |
|---|---|---|---|
| Chain-of-Thought (Wei, 2022) | Standard prompting | Self-Consistency, ToT, ReAct | Explicit step-by-step reasoning |
| ReAct (Yao, 2022) | CoT | Reflexion, LATS | Interleaved reasoning and action |
| Self-Consistency (Wang, 2023) | CoT | Aggregation methods | Multiple path sampling + majority vote |
| Tree of Thoughts (Yao, 2023) | ReAct | LATS | Tree search over reasoning steps |
| LATS (2023) | ToT + ReAct | — | MCTS + reflection in agent planning |
| Reflexion (Shinn, 2023) | ReAct | ReflAct | Verbal reinforcement via self-reflection |
| CoALA (2023) | — | — | Working/Episodic/Semantic/Procedural memory taxonomy |
| MemGPT (Packer, 2023) | RAG | — | OS-style virtual context for agents |
| Self-RAG (Asai, 2023) | Naive RAG | — | Selective, self-evaluated retrieval |
| RAPTOR (Sarthi, 2024) | Flat chunk RAG | — | Recursive tree-indexed summarization |
| AutoGen (Wu, 2023) | — | — | Conversable multi-agent abstraction |
| MetaGPT (Hong, 2023) | AutoGen | — | SOP-structured role-based agents |
| vLLM (Kwon, 2023) | Orca batching | — | PagedAttention, KV cache paging |
| DSPy (Khattab, 2023) | Manual prompting | — | Compiled, optimizable prompt programs |