# Experiment: Reasoning Evolution — 24 Game

Experiment Group: 1
Status: Designed
Started: —
Completed: —
Related papers: Chain-of-Thought, Self-Consistency, Tree of Thoughts, LATS
Related projects: planner-researcher-writer

---

## Motivation

This is a comprehension experiment, not a research experiment. Goal: understand
the character of each reasoning strategy by watching it succeed and fail on the
same task.

All four papers share a structural gap: each fixes a single strategy and measures
performance. None ask which strategy is appropriate given task difficulty or
compute budget. Before designing experiments that address that gap, the strategies
themselves must be understood from the inside — what they do, where they break,
and at what cost.

The 24 Game is the canonical task for this lineage. Yao et al. (ToT, 2023) use it
as their primary benchmark because it demands trial-and-error: there is no
universal solving strategy, and early wrong choices cascade. This makes it a
natural differentiator between strategies that commit to a single path and
strategies that explore.

Published results on GPT-4 (from the original papers) establish the ceiling:
- IO prompting:            7.3%   (ToT paper, Table 2)
- CoT prompting:           4.0%   (ToT paper, Table 2)
- CoT + Self-Consistency:  9.0%   (ToT paper, Table 2)
- ToT (b=5, BFS):         74.0%   (ToT paper, Table 2)
- LATS (n=5, MCTS):       outperforms ToT on Game of 24 (LATS paper, Table 7)

This experiment runs the same strategies on a local 7B model. Absolute accuracy
will be lower. The goal is not to match GPT-4 numbers — it is to observe whether
the relative ordering holds and where each strategy structurally collapses at
smaller scale.

---

## Hypothesis

H1: Reasoning accuracy follows the lineage ordering (CoT < SC < ToT < LATS)
on hard problems, but converges toward zero for all strategies when model scale
is insufficient to generate valid intermediate arithmetic steps.

H2: The cost differential between strategies (measured in LLM calls and total
tokens) is as large or larger at 7B scale as at GPT-4 scale, because the 7B
model requires more exploration to reach valid solutions — making the
accuracy-to-cost tradeoff sharper, not milder.

---

## Task Design

Task name: Game of 24
Task description: Given 4 integers, produce an arithmetic expression using
exactly those 4 numbers (each used exactly once) and the operators +, -, *, /
that evaluates to 24.
Input format: List of 4 integers, e.g. [4, 9, 10, 13]
Output format: A valid arithmetic expression equal to 24,
e.g. "(10 - 4) * (13 - 9)" = 24
Number of test cases: 20
How test cases were selected: Taken from 4nums.com indices 901-1000, the same
subset used in Yao et al. (ToT, 2023). That subset is sorted hard-to-solve by
human solving time and is the canonical benchmark for this task. 20 cases are
sampled: indices 901-910 (harder end) and 990-999 (slightly less hard), to
observe within-hard variance without running 100 cases at LATS cost on local
hardware.

---

## Strategies Being Compared

| Strategy         | Description                                              | Key design choices                                                                    |
|------------------|----------------------------------------------------------|---------------------------------------------------------------------------------------|
| CoT              | Single-pass reasoning with 3 intermediate equations      | 5-shot exemplars per ToT paper. Temperature 0.0. One call per problem.                |
| Self-Consistency | 10 independent CoT samples, majority vote on final answer | Temperature 0.8 per SC paper. n=10 samples. Majority vote on final expression.       |
| ToT              | BFS with LM-based state evaluation and pruning           | b=5 candidates per step per ToT paper. 3 BFS steps. Evaluator: sure/maybe/impossible. |
| LATS             | MCTS with value function, self-reflection, backprop      | n=5 sampled nodes per expansion, w=1 exploration weight, λ=0.5 self-consistency weight — all from LATS paper appendix. |

---

## What Is Held Constant

- Model: Llama 3.1 8B (local, via Ollama)
- Model temperature: 0.0 for CoT, ToT evaluation steps, LATS value function /
  0.8 for SC sampling (Wang et al. 2023) / 1.0 for ToT thought generation and
  LATS expansion (per ToT paper default)
- Maximum tokens per call: 512
- Retrieval corpus (if applicable): N/A
- Tool set (if applicable): arithmetic verifier only — expression is evaluated
  programmatically, not by the model
- Evaluation judge (if applicable): exact match via Python eval(); no LLM judge
- Hardware: local machine, CPU inference
- Random seed: 42

---

## Metrics

| Metric       | Definition                                      | How it is measured                                                         | Why it matters                                           |
|--------------|-------------------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------|
| Accuracy     | % of 20 problems solved correctly               | Python eval() checks expression == 24 and uses each input number once      | Primary indicator — directly comparable to paper Table 2 |
| LLM calls    | Total model calls per problem (mean)            | Counted per run, averaged over 20 problems                                 | Proxy for latency; reveals cost structure of each strategy |
| Total tokens | Total input + output tokens per problem (mean)  | Summed per run via Ollama token counts                                      | Actual compute cost; ToT paper notes 5-100x token overhead vs CoT |
| Collapse rate | % of problems where strategy produces no answer | CoT: empty or non-arithmetic output / SC: all 10 samples invalid / ToT: all branches pruned before depth 3 / LATS: budget exhausted with no valid solution | Reveals structural failure mode, not just accuracy floor |

Primary metric: Accuracy (% of 20 problems solved)
Secondary metrics: LLM calls per problem (mean), total tokens per problem (mean)
Failure mode metric: Collapse rate per strategy

---

## Evaluation Protocol

### Setup and Reproduction Instructions

1. Install dependencies
```bash
pip install ollama
```

2. Pull model
```bash
ollama pull llama3.1:8b
```

3. Fetch test cases (indices 901-910, 990-999 from 4nums.com)
```bash
python scripts/fetch_cases.py
```

4. Run each strategy
```bash
python run_cot.py   --cases data/cases.json --seed 42
python run_sc.py    --cases data/cases.json --seed 42 --n_samples 10
python run_tot.py   --cases data/cases.json --seed 42 --beam 5 --depth 3
python run_lats.py  --cases data/cases.json --seed 42 --n 5 --w 1.0 --lam 0.5
```

5. Evaluate and aggregate
```bash
python evaluate.py --output results/results.json
```

Expected runtime: CoT ~10 min / SC ~40 min / ToT ~90 min / LATS ~3 hrs
Estimated API cost: $0 — all runs local

---

## Results

To be filled after running.

### Quantitative Results

| Strategy         | Accuracy | LLM calls (mean) | Tokens (mean) | Collapse rate |
|------------------|----------|------------------|---------------|---------------|
| CoT              | —        | —                | —             | —             |
| Self-Consistency | —        | —                | —             | —             |
| ToT              | —        | —                | —             | —             |
| LATS             | —        | —                | —             | —             |

Reference (GPT-4, from papers):
CoT: 4% / SC: 9% / ToT b=5: 74% / LATS: exceeds ToT

### Failure Mode Analysis

To be filled after running.

### Surprising Findings

To be filled after running.

---

## Conclusion

To be filled after running.

---

## What This Experiment Does Not Answer

1. Whether these results generalize beyond combinatorial arithmetic tasks.
   The 24 Game isolates search and backtracking — other task types
   (multi-step planning, open-ended QA) may produce different strategy orderings.
2. Whether a larger model (70B, GPT-4) changes the crossover points between
   strategies. The GPT-4 reference numbers suggest ToT becomes strongly
   advantageous at sufficient model scale. Whether that threshold is between
   7B and 70B, or higher, is not answered here.
3. Whether LATS is the current ceiling. The papers were published in 2023.
   Post-2023 approaches — o1-style chain-of-thought with internal search,
   DeepSeek-R1, rStar, process reward model-based search — are not included.
   After this run, the strategy set will be extended and re-run as a new
   experiment: reasoning-CORA.

---

## Revision Notes

All numerical settings (b=5 for ToT, n=5 / w=1 / λ=0.5 for LATS, temperature
0.8 for SC, 5-shot CoT exemplars) are taken directly from the original papers.
GPT-4 reference numbers are from ToT paper Table 2 and LATS paper Table 7.
Test cases use the same 4nums.com source and difficulty range as the ToT paper.
