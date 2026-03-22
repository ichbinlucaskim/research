# Projects — Design and Documentation Standard

This folder contains small end-to-end systems built by combining
patterns validated in experiments.

A project is not a demo. It is a deliberately scoped system with
a real use case, a defined architecture, a measurable quality bar,
and a record of what broke and why.

The constraint is: a minimum working version within one day to one week.
If a project cannot reach minimum working state in a week, it is
too large. Break it down.

---

## Folder Structure

```
projects/
├── README.md                         # This file
├── research-operator-v0/
│   ├── README.md                     # Project design doc (required)
│   ├── architecture.md               # System design with component diagram
│   ├── src/                          # Source code
│   │   ├── agents/                   # Individual agent definitions
│   │   ├── tools/                    # Tool implementations
│   │   ├── memory/                   # Memory and retrieval layer
│   │   └── main.py                   # Entry point
│   ├── evals/
│   │   ├── cases/                    # Evaluation test cases
│   │   ├── run_eval.py               # Evaluation script
│   │   └── results/                  # Eval outputs, never edited
│   ├── logs/                         # Execution logs from real use
│   ├── postmortems/                  # Failure analysis docs
│   └── CHANGELOG.md                  # What changed and why
└── ...
```

---

## README.md Template (Project Design Doc)

Write this before writing any code.
The design doc is the most important artifact in the project folder.
A well-written design doc forces every ambiguity into the open before
you have written code that embeds the ambiguity.

---

```markdown
# Project: {Name}

Status: {Designing / Building / Minimum Version Done / Active Use / Deprecated}
Started: {YYYY-MM-DD}
Minimum version target: {YYYY-MM-DD}
Related experiments: {list}

---

## Problem Statement

What problem does this system solve?

Write this from the perspective of what you actually need it to do,
not from the perspective of what patterns you want to practice.

Good: "I spend 30-60 minutes per paper extracting implementation ideas.
This system should reduce that to under 5 minutes without losing
the architectural insight."

Bad: "Practice building a Retriever + Summarizer + Applicator pipeline."

Include: who uses it, what triggers its use, what success looks like
from the user's perspective.

---

## Scope

### In scope for minimum version

List the exact capabilities the minimum version must have.
Be specific. Vague scope is the primary cause of projects that never
reach minimum version.

- {Capability 1}: {precise description of what it does and does not do}
- {Capability 2}: {same format}

### Out of scope for minimum version

List things you explicitly decided not to build yet.
This section is as important as the in-scope list.
Writing it forces you to make decisions rather than letting scope drift.

- {Feature}: {why it is deferred, what it would require to add later}

### Success criteria for minimum version

How do you know when minimum version is done?

State this as observable behavior, not as a list of features.

"The system can take any arxiv URL, produce a structured note in
the papers/ template format, and score above 4/5 on a rubric
evaluation across 10 test papers. Runtime under 60 seconds per paper."

---

## Architecture

### Component Overview

List every component and its responsibility.

| Component | Responsibility | Input | Output |
|---|---|---|---|
| {name} | {what it does} | {type} | {type} |

### Control Flow

Describe the sequence of steps for the primary use case.

Step 1: {what happens}
Step 2: {what happens, including which component handles it}
Step 3: ...

If there are branches (conditional logic, retry loops, fallbacks),
describe them explicitly.

### Agent Roles

For each agent in the system:

Agent: {name}
Role: {one sentence}
Model: {which model, and why this model for this role}
Tools available: {list}
Memory access: {what it can read and write}
Prompt strategy: {CoT / ReAct / ReflAct / other, and why}
Max context: {token budget for this agent}
Failure behavior: {what happens if it fails or produces low-confidence output}

### Memory and Retrieval Design

What does the system need to remember?
Map each memory type to the CoALA taxonomy:

- Working memory: {what is in context right now, how it is managed}
- Episodic memory: {past interactions stored, format, retrieval method}
- Semantic memory: {knowledge base, index type, update frequency}
- Procedural memory: {learned workflows or policies, if any}

If the system uses RAG, specify:
- Retrieval strategy: {dense / sparse / hybrid}
- Chunk size and overlap
- Embedding model
- Re-ranking method (if any)
- When retrieval is triggered (always / selective / Self-RAG style)

### Tool Definitions

For each tool:

Tool: {name}
What it does: {one sentence}
Input schema: {parameters}
Output schema: {what it returns}
Failure mode: {what happens when the external call fails}
Cost: {API cost or latency estimate per call}

---

## Design Decisions

Document every significant decision and the reasoning behind it.
This section grows as the project evolves.

This is not a list of features. It is a record of forks in the road.

Format:
Decision: {What you decided}
Alternatives considered: {What else you could have done}
Reasoning: {Why you chose this option}
Revisit condition: {What evidence would make you switch to an alternative}

Example:
Decision: Use ReAct for the Researcher agent, CoT for the Summarizer.
Alternatives considered: ReAct for both; CoT for both.
Reasoning: Researcher needs tool calls and can benefit from interleaved
reasoning. Summarizer has all context available and adding tool call
overhead would increase latency without benefit.
Revisit condition: If Summarizer produces low-quality output on
long papers where key info is spread across many pages, switch to
ReAct with a search-within-document tool.

---

## Evaluation Design

How do you measure whether the system is working?

### Evaluation cases

Minimum: 10 test cases for minimum version.
Each case must have:
- A specific input
- A description of what a good output looks like
- A scoring rubric with at least 3 criteria and a 1-5 scale for each

Store cases in `evals/cases/`.

### Automated vs. human evaluation

For each criterion in your rubric, specify:
- Whether it is evaluated by LLM-as-Judge, automated scoring, or human review
- If LLM-as-Judge: the exact judge prompt used
- If automated: the exact metric and script

### Evaluation cadence

When do you run evals?
- After minimum version is working: full eval on all cases
- After each significant change: full eval
- During active use: log real outputs, sample and score weekly

---

## Instrumentation Requirements

Every project must log the following from the first working version.
Do not add logging later. Design it in from the start.

Per agent call:
- Timestamp
- Agent name
- Input (full)
- Output (full)
- Model name and version
- Input token count
- Output token count
- Latency in milliseconds
- Tool calls made and their results
- Any errors or retries

System-level per run:
- Total wall-clock time
- Total tokens across all agents
- Total estimated cost
- Whether the run succeeded, partially succeeded, or failed
- If failed: which component failed and the error message

Store logs in `logs/` with one file per day: `logs/YYYY-MM-DD.jsonl`

---

## Known Limitations

What does this system not handle well?
Write this before you have encountered the failures.
Come back and update it as you find them.

---

## Postmortems

When a meaningful failure occurs, write a postmortem in
`postmortems/YYYY-MM-DD-{description}.md`

Postmortem format:
- What happened (observable behavior)
- What the system was supposed to do
- Root cause (which component, which design decision)
- Contributing factors
- What changed as a result

Do not write postmortems only for dramatic failures.
Write them whenever the system's behavior surprises you.
Surprises are the signal that your mental model is wrong.

---

## CHANGELOG

Maintain a CHANGELOG.md at the project root.
Every meaningful change to architecture, prompts, tools, or retrieval
strategy gets an entry.

Format:
{YYYY-MM-DD}
Changed: {what changed}
Reason: {why}
Effect on eval: {did eval scores change, and in which direction}

Without this, you will not be able to identify which change
caused a regression or an improvement.
```

---

## Versioning Standard

Projects use a simple version scheme: v0, v1, v2.

v0: Minimum working version. Proves the architecture is viable.
    Acceptable to have rough edges, limited error handling,
    and manual steps in the workflow.

v1: First reliable version. Handles the common failure modes from v0.
    Evaluation score above your defined threshold on the full eval set.
    Instrumentation complete and logging to files automatically.

v2+: Extended capability. Additional scope items from the out-of-scope list,
    or architectural improvements motivated by postmortem findings.

Never jump straight to v1. Ship v0 first. The failures in v0 inform
every design decision in v1.

---

## Project Dependency Map

Some projects can be started immediately. Others depend on having
run related experiments first. This is the intended order.

```
Phase 1 (can start after Tier 1 experiments)
  research-operator-v0           needs: react-vs-cot, rag-comparison
  planner-researcher-writer      needs: multi-agent-patterns

Phase 2 (requires Tier 2 experiment results)
  personal-note-rag              needs: rag-retriever-strategies,
                                         self-rag-vs-naive-rag,
                                         memory-architecture
  task-memory-agent              needs: memory-architecture

Phase 3 (requires Phase 1 projects working)
  code-review-agent-v0           needs: react-vs-reflexion-vs-fusemind,
                                         tool-use-strategies
  bug-triage-team                needs: multi-agent-patterns,
                                         aggregation-reliability

Phase 4 (requires Phase 1-2 projects and Tier 3 experiments)
  agent-execution-viewer         needs: monitoring-ops, aggregation-reliability
  guard-critic-agent             needs: guard-agent, aggregation-reliability
  experiment-log-analyzer        needs: llm-as-judge-pipeline, monitoring-ops

Phase 5 (requires Tier 5 infrastructure experiments)
  agent-inference-profiler       needs: latency-cost-profiling,
                                         inference-serving-comparison
  streaming-agent-server         needs: inference-serving-comparison,
                                         context-window-scaling
  dspy-optimized-agent           needs: dspy-vs-manual-prompting,
                                         an existing project to optimize
```

The rationale for this ordering: you need empirical results from
experiments before you can make good architectural decisions in
projects. Building a memory-augmented system before you have
measured how different retrieval strategies perform is guessing.

---

## What Makes a Project Different From an Experiment

An experiment tests a specific isolated variable.
A project combines multiple validated patterns into a working system.

An experiment produces a result: "Strategy A outperforms Strategy B
on Task X under Condition Y."

A project produces a tool: something you actually use, that produces
real logs, that has real failures, that teaches you things no
controlled experiment can.

The value of projects is that they expose integration failures:
cases where two individually validated patterns interact badly.
These failures are invisible in experiments because experiments
isolate variables by design.

The failure log from a real project session is one of the most
valuable research artifacts you can produce. Treat it that way.