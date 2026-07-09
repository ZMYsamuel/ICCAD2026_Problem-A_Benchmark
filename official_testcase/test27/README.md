# test27 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test27.v` (6318 lines — official 0706 re-synthesis)

## Prompts

1. This is the beginning of a new testcase. The case name is test27.
2. Please load the design from the file test27.v located in the directory testcase/test27/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Decompose all XOR gates in the fanin cone of n15 into AND, OR, and NOT gates without changing functionality.
5. Find all back-to-back inverter pairs and collapse them into a wire. Make sure nothing changes functionally.
6. Delete all gates that do not contribute to any primary output. Make sure nothing changes functionally.
7. Optimize the logic to minimize maximum path depth, ensuring the cone of n15 contains only AND, OR, and NOT gates. Make sure nothing changes functionally. The cost function is the maximum logic depth of the final design; smaller is better.
8. Please write the current design to the output file test27_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.

> **Netlist updated 2026-07-09** to the official `A_Testcase_20260706` release (re-synthesized by Cadence Genus; module ports unchanged, internal structure and gate counts changed). Submissions committed before this date were produced against the 0510/0610 netlist and are **not comparable** for netlist-dependent answers (gate counts, depths, path/cone queries).
