## Design

ISCAS85 benchmark `c17` — the canonical "smallest non-trivial gate-level circuit." Originally from F. Brglez et al., "Combinational Profiles of Sequential Benchmark Circuits," ISCAS 1985.

- **Module**: `c17`
- **Primary inputs (5)**: N1, N2, N3, N6, N7
- **Primary outputs (2)**: N22, N23
- **Gates (6)**: all NAND2

Topology (every gate is `NAND2 (output, in_a, in_b)`):
```
NAND2_1 (N10, N1, N3)
NAND2_2 (N11, N3, N6)
NAND2_3 (N16, N2, N11)
NAND2_4 (N19, N11, N7)
NAND2_5 (N22, N10, N16)
NAND2_6 (N23, N16, N19)
```

Notable:
- **N3 has fanout 2** (drives NAND2_1 and NAND2_2).
- **N11 has fanout 2** (drives NAND2_3 and NAND2_4) — internal high-fanout node.
- **N16 has fanout 2** (drives NAND2_5 and NAND2_6) — feeds both POs.
- **Depth(N22) = 2**, **depth(N23) = 3**.

## Questions

This testcase mixes basic ops with analysis questions that exercise structural reasoning over a circuit small enough to verify by hand. Particular focus on the **signal-pair equivalence pattern** from problem statement §4.2 ("Do signals a and b such that (a & b) == z?") — implemented here as the NAND variant, with a trivial structural witness.

1. Set testcase, basic ack.
2. Load design.
3. Free-form netlist summary — verified by hand (matches comment block in design.v).
4. **Gate count by type** — deterministic, all 6 are NAND.
5. **Max depth N1→N22 = 2** — by hand: N1 → NAND2_1 → NAND2_5 → N22.
6. **Max depth N3→N23 = 3** — by hand: N3 → NAND2_2 → NAND2_3 → NAND2_6 (or via NAND2_4), longest path.
7. Path from N3 to N22 — any valid path (multiple exist). Status `review_pending` because there are multiple correct answers.
8. **Every path N3→N22 passes through NAND2_5** — `true`, because NAND2_5 is the only gate driving N22.
9. **Fanout of N11** — direct readout from netlist: {NAND2_3, NAND2_4}.
10. **Fanin cone of N22** — 4 gates (NAND2_5, NAND2_1, NAND2_3, NAND2_2).
11. **(Spec §4.2 pattern) Signal-pair equiv: ∃ (a, b) such that NAND(a, b) ≡ N22** — trivially yes because the netlist literally encodes `N22 = NAND(N10, N16)`. Witness: (N10, N16).
12. Write design.

## Contributor

ZMYsamuel — testcase authored 2026-05-14. Design from public-domain ISCAS85 benchmark suite.
