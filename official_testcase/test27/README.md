# test27 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test27.v` (6341 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test27.
2. Please load the design from the file test27.v located in the directory testcase/test27/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Insert buffers wherever needed so that no gate drives more than 4 loads. Make sure nothing changes functionally.
5. Optimize the logic to minimize maximum path depth. Make sure nothing changes functionally.
6. Delete all gates that do not contribute to any primary output. Make sure nothing changes functionally.
7. Decompose all XOR gates in the fanin cone of n15 into AND, OR, and NOT gates without changing functionality.
8. Try to optimize n15 to at most 4 levels deep. Make sure nothing changes functionally.
9. Find all back-to-back inverter pairs and collapse them into a wire. Ensure functional equivalence is preserved.
10. For each output with depth greater than 4, optimize its cone to meet the depth constraint. Ensure the design functionality does not change.
11. Please write the current design to the output file test27_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
