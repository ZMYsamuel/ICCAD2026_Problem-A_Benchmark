# case_optimize — Optimization with redundant AND chain

## Design

`redundant_and`: 4-gate implementation of y = a&b, deliberately bloated.

```
a, b ─[U1: AND]─ t1 ─[U2: AND]─ t2 ─[U3: AND]─ t3 ─[U4: BUF]─ y
       a───────────^   b───────────^
```

Boolean derivation:
```
t1 = a & b
t2 = t1 & a  =  (a&b) & a  =  a&b  (idempotence: x&x = x)
t3 = t2 & b  =  (a&b) & b  =  a&b  (idempotence)
y  = t3      =  a&b
```

So the entire 4-gate cone is redundant and should collapse to a single `AND` gate plus the buffer (or just a single AND wired directly to y) under ABC's resyn2 optimization.

## Questions

8 questions exercising contest §4.3 transform-and-verify flow:

| # | Question | Tests |
|---|----------|-------|
| 3–4 | Pre-optimization metrics | depth=4, gate_count=4 |
| 5 | The actual transform task | optimize cone preserving function |
| 6–7 | Post-optimization metrics | depth=1, gate_count=1 (or possibly 2 if a buffer survives) |
| 8 | Write-out | confirms post-edit state is persistable |

## Notes for reviewers

- ABC's `resyn2` script is the canonical optimization pipeline. The exact post-optimization gate naming will vary (ABC re-names after AIG round-trip), but the **structural property** — gate count drops from 4 to 1 (or 1 AND + BUF = 2), depth drops from 4 to 1 — must hold.
- Q6/Q7 golden allows for "1 or 2" gates because ABC may or may not strip the trailing BUF. A system reporting 2 gates with depth 1 is also acceptable, as long as functional equivalence holds (which the verifier confirms).
- This case directly exercises **EQUIVALENCE_EXPECTATION: preserve_all** in the transform agent. The verifier should pass on every truth-table row (a,b) ∈ {00, 01, 10, 11}.

## Contributor

Maintainer (bootstrap, derived from contest §4.3 "Reduce gate count" example).
