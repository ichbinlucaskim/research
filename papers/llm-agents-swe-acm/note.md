# LLM-Based Multi-Agent Systems for Software Engineering

Junda He, Christoph Treude, David Lo | ACM TOSEM | 2024 | Link: https://arxiv.org/pdf/2404.04834.pdf

Read: —
Status: Not Started
Section: A

---

## One-Line Claim

A systematic literature review that maps every stage of the software engineering lifecycle to specific multi-agent patterns, showing which SE tasks benefit most from multi-agent collaboration and why single-agent approaches fall short there.

---

## Problem Being Solved

Software engineering is not a single task — it is a pipeline of distinct activities: requirements gathering, system design, implementation, code review, testing, and maintenance. Each activity has different information needs, different verification criteria, and different failure modes. Before this paper, most multi-agent SE work tackled just one of these activities (usually code generation) without a unified view of how agents should be composed across the full pipeline. The paper asks: which parts of SE are actually improved by multi-agent collaboration, and what does that collaboration look like at each stage?

---

## Core Contribution

A structured mapping of the SE lifecycle to multi-agent patterns, based on a review of 100+ papers from 2022–2024:

**Requirements and Design**: Multi-agent debate patterns improve ambiguity resolution. Having a requirements agent generate a specification, a design agent critique it for implementation feasibility, and a domain agent flag missing constraints catches errors that a single agent misses because it lacks the perspective shifts.

**Code Generation**: Single-agent generation is strong for isolated functions. Multi-agent collaboration (Planner → Coder → Reviewer) outperforms on tasks that require maintaining consistency across multiple files or modules. The primary benefit is the reviewer agent catching issues that the generator agent cannot see because it is in a local reasoning context.

**Code Review**: Multi-agent is the clearest win here. A single agent reviewing its own generation has blind spots. Separating the generator and reviewer agents (even using the same base model) produces more and different bug detections. Adding a specialist agent per bug category (security, performance, style) further improves coverage.

**Testing**: Test generation benefits from a multi-agent structure where a specification agent reads the code intent, a test generator agent writes cases, and a coverage analyzer agent checks what is missing. Single-agent test generation tends to write easy-to-pass tests rather than adversarial ones.

**Debugging and Maintenance**: Multi-agent is valuable for root cause analysis: a fault localizer agent, a hypothesis generator, and a patch verifier working in sequence outperform a single agent doing all three. The key is that each agent can reason over its narrow task without the cognitive overhead of tracking the full context.

---

## Architecture / Method

The paper is a systematic literature review using PRISMA methodology: database search, screening by title and abstract, inclusion/exclusion criteria, and full-text review. The outcome is a taxonomy of multi-agent patterns for each SE stage, plus a set of open research challenges for each.

The most practically useful output is the per-stage agent role specification. For code review, for example, the paper identifies four distinct agent roles that appear across the reviewed systems and describes what each role's inputs, outputs, and success criteria are. This is directly usable as a design template when building code-review-agent-v0.

---

## Key Results

- Code review and testing show the largest and most consistent gains from multi-agent approaches. These tasks are inherently adversarial (find problems in something) and benefit from perspective separation.
- Code generation gains from multi-agent diminish for simple tasks. For a single function, a single agent with CoT is as good or better. Multi-agent overhead only pays off at module or system scale.
- Most surveyed multi-agent SE systems have no evaluation beyond functional correctness. Latency, cost, and failure mode analysis are almost universally missing.
- The Planner → Coder → Reviewer pattern (some variant of this three-agent structure) appears in roughly 60% of the reviewed code generation papers.
- Human-in-the-loop systems consistently outperform fully autonomous ones on complex tasks, but the gap narrows as task complexity decreases toward well-scoped, well-defined work.

---

## Limitations and What It Does Not Address

- The review covers published academic systems, which skew toward research prototypes. Industry deployments of multi-agent SE systems are not covered.
- Evaluation methodology is inconsistent across the reviewed papers, making direct comparison unreliable. The paper flags this but cannot fix it.
- The SE pipeline focus means the paper says little about agent infrastructure: how agents share code context, how they handle large codebases that exceed context windows, or how they manage state across long editing sessions.
- Most reviewed systems assume a fresh codebase. How multi-agent patterns apply to maintenance tasks on large, legacy codebases is largely unexplored.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [AutoGen (Wu, 2023)](../autogen-wu-2023/note.md) | Most reviewed papers in this survey use AutoGen-style conversable agent patterns |
| [MetaGPT (Hong, 2023)](../metagpt-hong-2023/note.md) | The Planner/Engineer/QA role structure in MetaGPT maps directly to the code generation multi-agent pattern identified here |
| [SWE-bench (Jimenez, 2024)](../swe-bench-jimenez-2024/note.md) | The benchmark this survey's code generation findings should be evaluated against |
| [Reflexion (Shinn, 2023)](../reflexion-shinn-2023/note.md) | The reviewer-agent pattern is a structured implementation of the reflection concept from Reflexion |
| [ReAct (Yao, 2022)](../react-yao-2022/note.md) | Single-agent baseline that the multi-agent systems in this survey are implicitly competing against |

---

## Implementation Angles

1. **code-review-agent-v0 design**: Use the paper's four-role code review structure (generator, reviewer, specialist, synthesizer) as the starting architecture. The paper provides enough detail to directly specify agent prompts per role.

2. **Task-appropriate architecture**: Apply the paper's finding that single-agent is sufficient for simple isolated functions, and multi-agent only pays off at module scale. Use this to decide dynamically which architecture to invoke based on diff size in code-review-agent-v0.

3. **Evaluation template**: The paper's finding that evaluation is the field's weakest point is a direct prompt to design evaluation for every project from day one. Use SWE-bench as the external benchmark and LLM-as-Judge for the components SWE-bench does not cover.

---

## Open Questions

- The paper shows that code review benefits most from multi-agent. Is this because the task is inherently dual (generate + verify) or because the existing single-agent code review prompts are just undertrained? A direct experiment with a well-tuned single-agent reviewer would clarify.
- How do these findings change for models trained specifically on code (CodeLlama, DeepSeek Coder) vs. general-purpose models? Most reviewed papers use GPT-4 or similar general models.

---

## Revision Notes

