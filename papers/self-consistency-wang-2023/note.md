# Self-Consistency Improves Chain of Thought Reasoning in Language Models

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, Denny Zhou | ICLR 2023 | 2023 | Link: https://arxiv.org/pdf/2203.11171.pdf

---

## One-Line Claim

Instead of taking one CoT reasoning path and trusting it, sample many diverse paths and take the majority vote on the final answer — this reliably improves accuracy on reasoning tasks without any additional training, by treating reasoning as an ensemble problem.

---

## Problem Being Solved

Greedy CoT (temperature=0, single path) has a specific failure mode: if the model takes a wrong turn at any step in the chain, the error propagates to the final answer with no correction mechanism. The chain is deterministic and brittle — one bad step means a wrong answer.

The insight behind Self-Consistency is that this is actually a sampling problem, not a model capability problem. Most reasoning tasks have one correct answer reachable by many different valid paths. A model that is capable enough to get the answer right sometimes, but not always, will get it right on most paths if you ask enough times. Wrong answers, by contrast, tend to scatter across many different wrong values rather than converging on a single wrong answer. Majority vote over many samples therefore amplifies correct signals and cancels out noise.

---

## Core Contribution

Replace greedy decoding with this three-step process:

1. **Sample N reasoning paths** using the same CoT prompt, but with temperature > 0 (typically 0.7–1.0) to get diverse paths. Each sample generates a complete chain plus a final answer.
2. **Extract the final answer** from each sample. Only the final answer matters for voting — the intermediate steps are discarded.
3. **Take the majority vote** across all N final answers. The most common answer wins.

No fine-tuning, no additional model, no architecture change. Just sample more and vote.

**Key insight about why diverse paths help**: a correct answer can be reached many ways (different arithmetic orderings, different intermediate decompositions, different phrasings). A wrong answer is usually specific — you make a specific arithmetic error or misidentify a specific fact. Correct answers cluster; wrong answers scatter. This is the statistical foundation for why majority vote over N samples systematically outperforms a single sample.

---

## Architecture / Method

**Implementation parameters for the experiment:**

- N (number of samples): the paper tests N = 5, 10, 20, 40. Performance improves up to about N=20–40 and then plateaus. For the reasoning-evolution experiment, start with N=10 as a reasonable cost/accuracy tradeoff, then test N=20 if budget allows.
- Temperature: 0.5–1.0. Too low and you get near-identical paths (defeating the purpose). Too high and paths become incoherent. 0.7 is the standard starting point.
- Answer extraction: the final answer must be consistently formatted so it can be parsed. Instruct the model to always end with "The answer is X" and parse that. If answers are free-form text (not a number or choice), you need an LLM judge to cluster similar answers before voting — this adds cost.
- Voting: for classification or numeric answers, exact string match. For open-ended answers, semantic clustering via embedding similarity or an LLM judge.

**Prompt template** — same as greedy CoT, only the decoding changes:
```python
answers = []
for _ in range(N):
    response = llm(prompt, temperature=0.7)
    answer = extract_final_answer(response)
    answers.append(answer)

final_answer = majority_vote(answers)
```

**Cost**: N× the cost of a single CoT call. N=10 costs 10× greedy CoT. This is the fundamental tradeoff — accuracy vs. cost. The reasoning-evolution experiment should measure whether the accuracy gain at N=10 is worth the 10× cost increase over greedy CoT.

---

## Key Results

| Task | Greedy CoT | Self-Consistency (N=40) | Model |
|---|---|---|---|
| GSM8K | 56.5% | 74.4% | PaLM 540B |
| GSM8K | 46.9% | 67.0% | GPT-3 175B |
| SVAMP | 66.0% | 86.0% | PaLM 540B |
| AQuA | 36.0% | 52.0% | PaLM 540B |
| StrategyQA | 73.9% | 82.8% | PaLM 540B |
| CommonsenseQA | 78.4% | 81.8% | PaLM 540B |

**The N curve**: improvements are steep from N=1 to N=10, then slower from N=10 to N=20, then marginal from N=20 to N=40. For most tasks, N=10–20 captures 80–90% of the total Self-Consistency gain. This means N=40 is rarely worth it relative to N=20.

**Compared to fine-tuning**: Self-Consistency at N=40 with PaLM 540B outperforms supervised fine-tuning on several benchmarks. This is the headline claim — a prompting method beats training on in-domain data.

---

## Limitations and What It Does Not Address

- **Linear cost scaling**: N samples = N× cost. There is no shortcut. If your task budget is tight, Self-Consistency becomes impractical at N > 5–10.
- **Flat sampling, no exploration**: Self-Consistency samples N paths independently with no information sharing between them. If all paths get stuck on the same wrong reasoning pattern (a systematic error rather than random noise), majority vote cannot help. It reduces variance but not bias.
- **Answer convergence required**: Self-Consistency only works cleanly when answers can be compared and counted. For open-ended generation tasks (write a summary, generate code), there is no natural majority vote — you need a judge to evaluate and aggregate, which is a different and harder problem.
- **No backtracking within a path**: each individual path is still a linear CoT chain. If the correct answer requires exploring and abandoning a wrong approach mid-chain, Self-Consistency does not help. ToT was built specifically to address this.
- **Does not address grounding**: same as CoT — still no external retrieval or tool use.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [Chain-of-Thought (Wei, 2022)](../chain-of-thought-wei-2022/note.md) | Direct predecessor: Self-Consistency is built on top of CoT and fixes its single-path brittleness |
| [Tree of Thoughts (Yao, 2023)](../tree-of-thoughts-yao-2023/note.md) | ToT addresses the flat-sampling limitation: instead of N independent paths, explore a structured tree with backtracking |
| [LATS (2023)](../lats-2023/note.md) | LATS incorporates a value function to guide sampling intelligently, instead of sampling blindly and voting |
| [Reliable Decision-Making](../reliable-decision-making/note.md) | The multi-agent aggregation methods in that paper are a direct generalization of the majority vote idea from Self-Consistency |
| [LLM-as-a-Judge (Zheng, 2023)](../llm-as-judge-zheng-2023/note.md) | When Self-Consistency is extended to open-ended tasks, LLM-as-Judge becomes the aggregation mechanism |

---

## Implementation Angles

1. **Strategy 2 in reasoning-evolution**: implement Self-Consistency as N=10 samples at temperature=0.7 with majority vote. Compare directly against greedy CoT on the same 15 test cases. Measure: accuracy, tokens per correct answer (cost efficiency), and how often the majority vote differs from the single best sample.

2. **Saturation curve**: run Self-Consistency at N=1, 3, 5, 10, 20 on a subset of 5 test cases and plot accuracy vs. N. Find the knee of the curve — the N at which accuracy plateaus. This tells you the minimum N worth running and is a reusable calibration for any aggregation-based experiment.

3. **Bias vs. variance diagnosis**: when Self-Consistency fails (majority vote is wrong), check whether the wrong answer got a plurality (systematic bias — all paths make the same error) or whether answers scattered evenly with no majority (high variance on a hard task). These failure modes point to different fixes: bias requires ToT/LATS, high variance requires more samples.

---

## Open Questions

- The paper shows that wrong answers scatter while correct answers cluster. Does this hold for open-ended synthesis tasks (like the ones in reasoning-evolution), or does it only hold for tasks with a small, enumerable answer space?
- Self-Consistency improves reliability but also increases latency proportionally. For the experiment, is there a latency budget where N=10 becomes impractical for interactive use cases?

---

## Revision Notes

