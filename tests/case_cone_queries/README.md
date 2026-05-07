# case_cone_queries — Cone-size analysis on demo_circuit

## Design

Same `demo_circuit` (10 gates + 1 DFF). See `case_demo01/README.md` for full topology.

## Questions

7 questions, all from contest §4.2 cone-property category:

| # | Question | Tests |
|---|----------|-------|
| 3 | cone gate count of medium PO | out0 → 5 |
| 4 | cone gate count of largest PO | out2 → 6 |
| 5 | cone gate count crossing a DFF boundary | out1 → 1 (NOT 3, because FF1 acts as boundary) |
| 6 | filter POs by threshold (3) | {out0, out2} |
| 7 | filter POs by tighter threshold (5) | {out2} only |
| 8 | boundary-input enumeration | {a, b, c, DFF_OUT_FF1} |

The interesting property is **Question 5** — a naive system might count "3 gates" (U6, U7, U8) for out1 because those are reachable backwards through the DFF. But under combinational-cone semantics, the DFF terminates the cone, so only U8 is in out1's cone.

## Notes for reviewers

- Q4's golden explicitly enumerates which gates are NOT in out2's cone (U5, U7, U8, U6) — this is for clarity; a system answer that just gives "6" plus the list of cone gates is equally acceptable.
- Q8's mention of `DFF_OUT_FF1` is the canonical name for the virtual node `cada0001_alpha` uses; a system that names it `q1` (the actual q signal of FF1) is also acceptable.

## Contributor

Maintainer (bootstrap, derived from contest §4.2 cone example).
