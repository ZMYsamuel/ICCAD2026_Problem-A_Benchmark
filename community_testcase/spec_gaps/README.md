## Design

Hand-crafted small combinational circuit (10 gates) whose structure deliberately exercises three §4.3 transformation patterns from the contest problem statement that are not covered by the existing community testcases:

- **High-fanout net** (`hi`, fanout 4) — target for "Insert buffers wherever needed so that no gate drives more than N loads" (`buffer balancing` / fanout reduction).
- **Two buffers with prefix `BUF_`** (`BUF_main`, `BUF_aux`) — target for "Insert AND gates before all buffers with certain naming patterns" (`gate insertion based on naming patterns`).
- **Two dangling gates** (`DANGLE_NOT`, `DANGLE_AND`) — target for "Removing dangling gates."

### Module signature

```verilog
module spec_gaps (a, b, c, d, e, f, out0, out1);
  input a, b, c, d, e, f;
  output out0, out1;
```

### Topology

```
a → BUF_main → hi ─┬─→ AND_a (w2) ─┐
                   ├─→ AND_b (w3) ──┐    \
                   ├─→ OR_a  (w4) ─┐│    \
                   └─→ NOT_a (w5) ─┘│     → FINAL_AND → out0
                                    ─┘
b → BUF_aux  → w1 ──┘                 → FINAL_XOR → out1

e → DANGLE_NOT → dangle1 ─┐
                          ├→ DANGLE_AND → dangle2   (never reaches a PO)
f ────────────────────────┘
```

## Questions

1. Set testcase / 2. Load — basic ops.
3. Netlist summary — free-form ack with hand-checkable numbers (PI=6, PO=2, 10 gates with the breakdown shown above).
4. **Fanout of `hi`** = 4. Direct consumers: AND_a, AND_b, OR_a, NOT_a. By inspection of the design.
5. **Instances with `BUF_` prefix** = {BUF_main, BUF_aux}.
6. **Dangling gates** = {DANGLE_NOT, DANGLE_AND}. Their outputs (`dangle1`, `dangle2`) connect to no other gate and to no PO.
7. **Fanout reduction (spec §4.3)** — insert buffers so net `hi` drives ≤ 2 loads. Functional equivalence required.
8. **New fanout of `hi`** after reduction = 2 (the design's spec).
9. **Dangling removal (spec §4.3)** — drop the 2-gate dangling subcircuit; equivalence must hold trivially because they were unobservable.
10. New gate count — depends on how many fanout buffers were inserted in prompt 7, so `status: review_pending` (verify whatever the system reports against an independent fanout-tree calculation during manual review).
11. **Naming-pattern gate insertion (spec §4.3)** — wrap each `BUF_*` with `AND(x, 1'b1) → BUF`. Functional equivalence preserved because AND(x, 1) = x.
12. Write final design.

## Contributor

ZMYsamuel — testcase authored 2026-05-14. Design hand-crafted to exercise spec §4.3 transformations.
