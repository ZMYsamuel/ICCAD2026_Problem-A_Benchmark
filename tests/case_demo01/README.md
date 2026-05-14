# case_demo01 — Mixed analysis + transform on demo_circuit

## Design

Compact gate-level circuit (10 combinational gates + 1 DFF) deliberately constructed to exercise multiple analysis categories simultaneously. Module name: `demo_circuit`.

```
   a ──┬──[U1: AND]──n1──┬──[G_mid: OR]──n3──┬──[U4: NAND]──n4──[U5: BUF]──out0
   b ──┘                 │                    │
   c ──[U2: NOT]──n2─────┘────────────────────┘

   a ──┬──[U6: XOR]──n5──[U7: AND]──n6──[FF1: DFF]──q1──[U8: BUF]──out1
   b ──┘                        c ──┘

   n4, q1 ──[U9: NOR]──n7──[U10: NOT]──out2
```

Key properties:

- Total gates: 10 (AND=2, NOT=2, OR=1, NAND=1, BUF=2, XOR=1, NOR=1) plus 1 DFF.
- Max depth a→out0 = 4 (longest combinational path).
- Global max combinational depth = 5 (any of a/b/c → out2).
- out2's combinational cone (6 gates) is largest; out1's cone (1 gate) is smallest because FF1 acts as a boundary.

## Questions

The 16 questions exercise:

| #   | Type      | What it tests                               |
| --- | --------- | ------------------------------------------- |
| 1   | basic     | testcase initialization (per contest §3.3)  |
| 2   | basic     | design loading                              |
| 3   | analysis  | netlist summary (PI/PO/gate counts)         |
| 4–5 | analysis  | per-PI to PO depth                          |
| 6   | analysis  | global max depth across all PI-PO pairs     |
| 7–8 | analysis  | path properties (must-pass-through)         |
| 9   | analysis  | path enumeration with negative constraint   |
| 10  | analysis  | cone size of a single PO                    |
| 11  | analysis  | filter POs by cone-size threshold           |
| 12  | analysis  | fanin / fanout of an internal net           |
| 13  | analysis  | DFF enumeration                             |
| 14  | analysis  | clock domain comparison                     |
| 15  | transform | buffer insertion (preserve_all equivalence) |
| 16  | basic     | design write-out                            |

## Notes for reviewers

- Q5 has multiple equally-long paths (c → U2 → G_mid → U4 → U5 and c → U2 → U4 → U5 are 4 and 3 gates respectively; max is 4 via the G_mid branch). Golden gives the longer one.
- Q8 the existence-counterexample in the golden is the path Q9 directly produces; that's intentional — it's the same fact framed differently.
- Q14 is technically asking the trivial case (FF1 vs FF1 — always same domain). The contest's example phrasing was "Does dff1 and dff2 under the same clock domain?", but for a single-DFF design this is the smallest valid version.

## Contributor

Maintainer (initial bootstrap, derived from Week-4 demo_gate.v + Week-5 demo questions).
