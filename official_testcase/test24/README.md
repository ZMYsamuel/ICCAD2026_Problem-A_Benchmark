# test24 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test24.v` (17212 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test24.
2. Please load the design from the file test24.v located in the directory testcase/test24/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Remove all dangling gates that do not contribute to any primary output. Ensure functional equivalence is preserved.
5. Rename gate g0 to renamed_gate. Ensure functional equivalence is preserved.
6. Optimize the logic to minimize maximum path depth. Ensure functional equivalence is preserved. The cost function is the maximum logic depth of the final design; smaller is better.
7. Please write the current design to the output file test24_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
