# Experiments — Design and Documentation Standard

This folder contains controlled experiments that compare architectures,
patterns, and strategies against each other under identical conditions.

An experiment that cannot be reproduced by someone else reading the
folder is not an experiment. It is a script with notes.

The standard here is: another engineer should be able to read your
experiment folder, re-run it on different hardware or a different
model, and get results that either confirm or meaningfully challenge
yours.

---

## Folder Structure

```
experiments/
├── README.md                         # This file
├── react-vs-cot/
│   ├── README.md                     # Experiment design doc (required)
│   ├── setup.py                      # Environment and data setup
│   ├── run_cot.py                    # Baseline implementation
│   ├── run_react.py                  # Experimental implementation
│   ├── evaluate.py                   # Shared evaluation logic
│   ├── results/
│   │   ├── raw/                      # All raw outputs, never edited
│   │   └── summary.md                # Interpreted results (required)
│   └── logs/                         # Full execution logs
└── ...
```

Each experiment lives in its own folder.
The folder name matches the experiment name in the main README.

---

## README.md Template (Experiment Design Doc)

This document is written before running any code.
Writing it forces you to commit to a hypothesis and measurement plan
before you see results. Do not modify it after the experiment starts
except in the designated revision section at the bottom.

---

```markdown
# Experiment: {Name}

Status: {Designed / Running / Done / Abandoned}
Started: {YYYY-MM-DD}
Completed: {YYYY-MM-DD}
Related papers: {list}
Related projects: {list}

---

## Motivation

Why does this experiment exist?

Name the specific architectural question or design decision you are
trying to answer. This should be a question you would actually face
when building a system, not a question about reproducing a paper result.

Good: "When building the bug-triage pipeline, should I use ReAct or
CoT? Under what conditions does the tool-calling overhead of ReAct
pay off?"

Bad: "Does ReAct outperform CoT?"

---

## Hypothesis

State exactly what you predict will happen and why.

Format:
  H1: {What you expect to observe}
  Reasoning: {Why you expect this, based on the papers you have read}

  H2: {Alternative outcome you consider plausible}
  Reasoning: {Why this could also be true}

If you cannot state a hypothesis, you have not read the relevant
papers carefully enough. Go back and read them.

---

## Task Design

Describe the task used for comparison.

Requirements for a valid task:
- It must be specific enough that outputs can be evaluated without
  ambiguity about what counts as correct
- It must be complex enough that the strategies being compared have
  room to differ
- It must be representative of a real use case in your project list

Task name: {name}
Task description: {what the agent is asked to do}
Input format: {what the input looks like}
Output format: {what a correct output looks like}
Number of test cases: {N}
How test cases were selected: {random sample / curated / synthetic / from benchmark}

If you are using a public benchmark (SWE-bench, AgentBench, etc.),
state which subset and why.

---

## Strategies Being Compared

Name each strategy. Describe it precisely enough that someone else
could implement it without asking you questions.

| Strategy | Description | Key design choices |
|---|---|---|
| {name} | {what it does mechanically} | {prompt structure, tool access, memory, model} |
| {name} | {same format} | {same format} |

Anything that differs between strategies must be listed here.
Anything that is held constant must be documented in the Setup section.

---

## What Is Held Constant

List every variable that is identical across all strategies.

- Model: {name and version}
- Model temperature: {value}
- Maximum tokens per call: {value}
- Retrieval corpus (if applicable): {description}
- Tool set (if applicable): {list of tools available to all strategies}
- Evaluation judge (if applicable): {LLM-as-judge model and prompt}
- Hardware: {GPU / CPU, memory}
- Random seed: {value}

If you cannot hold something constant, document why and how you
controlled for it.

---

## Metrics

Define every metric before running the experiment.
Do not add metrics after seeing results.

| Metric | Definition | How it is measured | Why it matters |
|---|---|---|---|
| {name} | {precise definition} | {automated / human / LLM judge} | {what decision it informs} |

Primary metric: the single metric that determines which strategy wins
if they conflict on others.

Secondary metrics: everything else.

Failure mode metric: what you measure to understand how each strategy
fails, not just how well it succeeds.

---

## Evaluation Protocol

How are outputs judged?

If using automated evaluation: write the exact prompt used for
LLM-as-Judge here, or reference the file containing it.

If using human evaluation: describe the rubric and who is evaluating.

If using benchmark scoring: reference the exact evaluation script.

Document any edge cases in how you handle ties, refusals, or
malformed outputs.

---

## Setup and Reproduction Instructions

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...

# 3. Run setup (downloads data, builds index, etc.)
python setup.py

# 4. Run all strategies
python run_cot.py --output results/raw/cot.json
python run_react.py --output results/raw/react.json

# 5. Evaluate
python evaluate.py --results results/raw/ --output results/summary.md
```

Expected runtime: {N} minutes on {hardware description}
Estimated API cost: {dollar amount}

---

## Results

Fill this section after running. Do not fill it before.

### Quantitative Results

| Strategy | Primary metric | Secondary metric 1 | Secondary metric 2 | Failure rate |
|---|---|---|---|---|
| {name} | {value} | {value} | {value} | {value} |
| {name} | {value} | {value} | {value} | {value} |

### Failure Mode Analysis

For each strategy, describe the most common failure pattern.

Strategy {name}:
- Most common failure type: {description}
- Example input that triggers it: {example}
- Frequency: {N out of M test cases}

### Surprising Findings

What did you observe that you did not predict?
What would you have designed differently if you had known this first?

---

## Conclusion

Answer the motivating question stated at the top of this document.

Be specific. Do not write "ReAct is better than CoT."
Write "On the bug triage task with access to a code search tool,
ReAct outperformed CoT by X points on resolution accuracy at 1.4x
the token cost. CoT was faster and cheaper on input types that did
not require tool calls."

Design recommendation:
Given these results, what would you do differently when building
the related project? State this as a concrete design decision.

---

## What This Experiment Does Not Answer

What follow-up questions did this experiment raise that it did
not answer?

List at least two. These become candidates for future experiments.

---

## Revision Notes

{YYYY-MM-DD}: {What changed in your understanding, what you would
do differently, or what a follow-up experiment revealed}
```

---

## Standards for Raw Results

Everything in `results/raw/` is immutable once written.

Never edit a raw output file. If you re-run an experiment, create
a new timestamped subdirectory: `results/raw/2025-06-14/`

Raw output files must include:
- The exact input passed to the model
- The exact output received
- Timestamp
- Model name and version
- Token count (input and output)
- Latency in milliseconds
- Any tool calls made and their responses

Without this, you cannot debug failures or compare runs.

---

## Experiment Dependency Map

Some experiments should be run before others because their results
inform the design of later ones. This is the intended order.

```
Experiment Group 1 — Core Patterns (run first — establishes intuitions)
  react-vs-cot
  react-vs-reflexion-vs-fusemind
  reasoning-evolution
  multi-agent-patterns

Experiment Group 2 — Memory and Retrieval (depends on Group 1 intuitions)
  rag-comparison
  rag-retriever-strategies
  self-rag-vs-naive-rag
  memory-architecture
  raptor-vs-flat-rag

Experiment Group 3 — Reliability and Aggregation (depends on Group 1 + 2)
  aggregation-reliability
  llm-as-judge-pipeline
  monitoring-ops

Experiment Group 4 — Tool Use and Action Space (can run in parallel with Group 2-3)
  tool-use-strategies
  code-vs-json-action-space
  dspy-vs-manual-prompting

Experiment Group 5 — Inference and Systems (requires infrastructure setup)
  inference-serving-comparison
  latency-cost-profiling
  speculative-decoding-impact
  context-window-scaling

Experiment Group 6 — Safety (run after Group 3 and 4)
  guard-agent
  prompt-injection-defense
```

Rationale: You need empirical intuition about how individual agents
fail (Group 1) before you can design meaningful aggregation experiments
(Group 3). You need retrieval benchmarks (Group 2) before building
memory-augmented systems. Inference experiments (Group 5) require a
working agent loop to profile, which comes from Groups 1 and 2.

---

## Common Mistakes

These are the mistakes that make experiments uninterpretable.

Changing the task mid-experiment.
If your task definition changes after you start, restart.
Mixing results from different task definitions produces noise, not signal.

Not logging failures.
A 70% success rate tells you little. The 30% failure cases tell you
everything about where the architecture breaks. Log them all.

Optimizing the baseline too little.
If you are comparing ReAct against CoT, the CoT baseline should be
your best effort at CoT, not a minimal implementation. A weak baseline
makes every alternative look good and teaches you nothing.

Treating token cost as an afterthought.
Every experiment should report cost. An agent that is 5% more accurate
at 3x the cost is a different tradeoff than one that is 5% more
accurate at 1.1x the cost. Both are valid findings. Only one is
deployable.

Over-indexing on average performance.
Report the distribution, not just the mean. An agent with high average
performance and a long tail of catastrophic failures is a different
system from one with moderate average performance and a tight failure
distribution. Production systems care about the tail.