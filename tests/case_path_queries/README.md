# case_path_queries — Path-property analysis on demo_circuit

## Design

Same `demo_circuit` as case_demo01 (10 gates + 1 DFF). See its README for topology.

## Questions

7 questions, all from contest §4.2 path-property category:

| # | Question | Tests |
|---|----------|-------|
| 3 | every-path-through (positive case, single fanin) | a→out0 thru G_mid → YES |
| 4 | every-path-through (positive case, sibling input) | b→out0 thru G_mid → YES |
| 5 | every-path-through (negative case, fanout split) | c→out0 thru G_mid → NO (c→U2 has two outgoing edges) |
| 6 | every-path-through (positive case, convergence) | c→out2 thru U4 → YES |
| 7 | not-thru with no possible path | a→out0 not-thru U1 → impossible |
| 8 | not-thru returning a concrete witness path | c→out0 not-thru G_mid → c→U2→U4→U5→out0 |
| 9 | enumerate gates on any path | a→out2 path-gates: 5 |

This case stresses the system on **negative results** (questions 5 and 7) — these are easy to get wrong because saying "yes" satisfies most surface heuristics.

## Notes for reviewers

- Q9 has 1 path from a to out2 because U1's output (n1) only fanouts to G_mid. Path: a→U1→G_mid→U4→U9→U10→out2. The set of gates on that path is the answer.
- Q5's reasoning depends on the fact that net `n2` (U2's output) has fanout to both G_mid and U4. This is the kind of fanout-split corner case the contest mentions in §4.2.
- Q7's "no such path" answer is acceptable as either an explicit "no such path" message or a structured `{found: false}` representation — wording is flexible.

## Contributor

Maintainer (bootstrap, derived from contest §4.2 example queries).
