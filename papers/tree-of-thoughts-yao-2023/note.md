# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan | NeurIPS 2023 | 2023 | Link: https://arxiv.org/pdf/2305.10601.pdf

---

## One-Line Claim

Reformulate problem-solving as search over a tree of intermediate "thoughts," where the model can generate multiple continuations from any state, evaluate which look promising, and backtrack from dead ends — turning reasoning from a one-shot chain into a deliberate exploration process.

---

## Problem Being Solved

Both greedy CoT and Self-Consistency have a structural limitation: they reason linearly. Even Self-Consistency's N paths are N independent linear chains — none of them can explore a direction, find it unpromising, and backtrack to try something else.

Many real problems require exactly this: you start solving in a direction, realize it won't work, and need to try a different approach from an earlier decision point. Humans do this constantly — it is called deliberate problem solving. CoT cannot do it because once a step is committed to text, the generation continues forward with no return path.

The paper frames this as a missing search dimension. CoT collapses reasoning into token-level search within a single path. ToT lifts reasoning to thought-level search across a tree of paths, where each node is a coherent intermediate reasoning state.

---

## Core Contribution

A framework with four components that work together:

**1. Thought decomposition** — define what a "thought" is for the specific task. A thought is a coherent intermediate unit that meaningfully advances the solution. For arithmetic: one equation. For creative writing: one paragraph of an outline. For a planning task: one action step. Defining this well is task-specific and is the main design work in applying ToT.

**2. Thought generation** — at each node, generate k candidate next thoughts (k = branching factor, typically 2–5). Two strategies:
- *Sample*: generate k thoughts independently from the same prompt at temperature > 0.
- *Propose*: prompt the model to generate k diverse thoughts in a single call ("generate 3 different next steps").

**3. State evaluation** — at each node, assess how promising this reasoning state is. Two strategies:
- *Value*: ask the model to score the state 1–10 or classify it as sure/likely/impossible.
- *Vote*: ask the model to compare multiple states and pick the best one.
This is a key difference from Self-Consistency: ToT uses the model to evaluate intermediate states, not just final answers.

**4. Search algorithm** — how to traverse the tree:
- *BFS (breadth-first)*: expand all nodes at the current depth before going deeper. Good for tasks where you need to compare many alternatives at each step. Keeps a fixed beam of the top-b states at each level.
- *DFS (depth-first)*: explore one path fully, then backtrack. Good for tasks where paths are long but most dead ends are caught early.

---

## Architecture / Method

The full ToT loop for BFS (the most common variant):

```
Initialize: tree = {root: initial problem state}
For each depth level d from 1 to max_depth:
    For each node in current frontier (top-b nodes from previous level):
        Generate k thoughts → k new candidate states
        Evaluate each new state with LLM value/vote prompt
    Keep top-b states by value score → new frontier
Return: best final state in frontier
```

**Cost calculation**: with branching factor k=3, beam width b=5, depth d=3, and value estimation:
- Thought generation: b × k × d = 45 LLM calls
- State evaluation: b × k × d = 45 LLM calls (one per candidate)
- Total: ~90 LLM calls vs. 1 for greedy CoT and N=10 for Self-Consistency

This is a large cost multiplier. ToT is expensive and should be reserved for tasks where the problem genuinely requires exploration.

**Key prompt designs for the experiment:**

*Thought generation prompt:*
```
Given the current problem state: [state]
Generate [k] different possible next steps. Each step should be
meaningfully different from the others. Format: Step 1: ... Step 2: ... Step 3: ...
```

*State evaluation prompt:*
```
Problem: [original problem]
Current reasoning state: [state]
Rate the likelihood that this reasoning path leads to a correct solution.
Score: 1 (dead end) to 10 (highly promising). Explain your score briefly.
```

---

## Key Results

| Task | CoT | Self-Consistency | ToT | Notes |
|---|---|---|---|---|
| Game of 24 | 4.0% | 9.0% | 74.0% | BFS, k=5, b=5 |
| Creative Writing (coherence) | 6.9 / 10 | — | 7.2 / 10 | Human eval, BFS |
| Mini-Crosswords (success) | 0% | — | 20% | DFS with backtracking |

**Game of 24** is the landmark result: given 4 numbers, find an arithmetic expression that equals 24. This requires systematic exploration of possible orderings — CoT fails almost entirely because there is no structure in a linear chain for this task. ToT's tree search finds valid combinations by exploring and pruning.

**Mini-Crosswords**: CoT gets 0% because a wrong letter in one cell propagates to all crossing words. DFS with backtracking is exactly what is needed — fill a letter, check for contradictions, backtrack if stuck.

These are tasks specifically chosen because they require exploration. ToT does not universally beat Self-Consistency — on straightforward reasoning tasks with clear structure, Self-Consistency's simpler sampling is competitive at lower cost.

---

## Limitations and What It Does Not Address

- **Task-specific thought design required**: defining what a "thought" is and what a good state evaluation prompt looks like is task-specific manual work. ToT is not plug-and-play — it requires significant prompt engineering for each new task type.
- **High cost**: 90+ LLM calls for a single problem is only viable when the task genuinely cannot be solved another way. For most tasks, Self-Consistency at N=10 is more cost-efficient.
- **Evaluation quality depends on the model**: the state evaluator is the LLM itself. If the model cannot reliably score intermediate reasoning states (which is hard for novel problems), the tree search degrades to expensive random search.
- **No external environment feedback**: state values are estimated by the model, not by executing the solution. For tasks where you can actually run code or query a database, real feedback would be far more reliable than model self-evaluation.
- **No reflection or learning**: ToT explores the tree and finds a solution but discards the search history. If the same problem structure comes up again, it starts over. LATS was built specifically to address this.

---

## Connections to Other Papers

| Paper | Relationship |
|---|---|
| [Chain-of-Thought (Wei, 2022)](../chain-of-thought-wei-2022/note.md) | CoT is a degenerate ToT: a tree with branching factor 1 and depth = chain length, no backtracking |
| [Self-Consistency (Wang, 2023)](../self-consistency-wang-2023/note.md) | Self-Consistency is a flat ToT: N paths of depth 1, all from the root, with majority vote instead of tree search |
| [LATS (2023)](../lats-2023/note.md) | LATS replaces ToT's BFS/DFS with MCTS, adds reflection on failed nodes, and integrates tool use — the full upgrade |
| [ReAct (Yao, 2022)](../react-yao-2022/note.md) | ReAct grounds individual reasoning steps in tool calls; ToT applies the same depth-over-breadth logic to the search structure |

---

## Implementation Angles

1. **Strategy 3 in reasoning-evolution**: implement ToT as BFS with k=3 (branching factor), b=3 (beam width), depth=3, using the model as its own state evaluator. For the paper synthesis task, define a "thought" as one claim about the connection between the two papers. Measure accuracy, total LLM calls, wall-clock time, and token cost — expect this to be significantly higher than CoT or Self-Consistency.

2. **Branching factor sensitivity**: run ToT with k=2, k=3, k=5 on the same 5 test cases. The Game of 24 result used k=5 but most tasks reach diminishing returns at k=3. Finding the minimum k that achieves 90% of ToT's max accuracy is essential for cost control.

3. **Failure mode analysis**: when ToT fails, check whether (a) all branches were wrong (the problem requires a capability the model lacks regardless of search), (b) the correct branch was generated but rated low by the evaluator (evaluation quality failure), or (c) the correct branch was pruned because beam width b was too small (beam search failure). Each has a different fix.

---

## Open Questions

- The paper tests ToT on tasks specifically designed for tree search (Game of 24, crosswords). For the open-ended synthesis tasks in reasoning-evolution, is the exploration actually helpful, or does the model produce similarly-valued branches that dilute rather than improve the search?
- State evaluation is the weakest component: the model scores its own intermediate states. How often is a state that the model scores low actually the correct path? Measuring evaluator accuracy separately from search accuracy would clarify this.

---

## Revision Notes

