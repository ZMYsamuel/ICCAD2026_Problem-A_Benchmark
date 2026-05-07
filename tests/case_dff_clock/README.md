# case_dff_clock — Sequential / clock-domain analysis on demo_circuit

## Design

Same `demo_circuit` (10 gates + 1 DFF). See `case_demo01/README.md`.

## Questions

5 questions exercising contest §4.2 sequential and clock-domain queries:

| # | Question | Tests |
|---|----------|-------|
| 3 | DFF enumeration | List of DFF instances → [FF1] |
| 4 | Per-DFF metadata: clock + reset | clk + rst_n |
| 5 | Per-DFF metadata: data input net | n6 (with the upstream gate context) |
| 6 | Clock-domain comparison (trivial self-case) | YES |
| 7 | Distinct clock domain count | 1 |

This case is intentionally minimal because demo_circuit only has one DFF in one clock domain. A future contributor could add `case_multi_clock` with two DFFs on different clocks to stress the comparison logic.

## Notes for reviewers

- Q5: depending on system convention, the data input might be reported as net name `n6` or as the driving gate name `U7`. Both are acceptable; the golden gives the net name primarily and mentions U7 for context.
- Q6: the question intentionally asks `FF1 vs FF1` (self-comparison) since the design has only one DFF. The contest example "Does dff1 and dff2 under the same clock domain?" presumes two DFFs.

## Contributor

Maintainer (bootstrap, derived from contest §4.2 clock-domain example).
