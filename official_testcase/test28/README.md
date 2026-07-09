# test28 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test28.v` (17381 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test28.
2. Please load the design from the file test28.v located in the directory testcase/test28/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Reconstruct the entire netlist using only AND and NOT gates while preserving functional equivalence.
5. Sweep out dangling gates. Make sure nothing changes functionally.
6. Find all back-to-back inverter pairs and collapse them into a wire. Ensure functional equivalence is preserved.
7. Minimize the maximum logic depth of the design, ensuring the netlist remains AND and NOT only. Make sure nothing changes functionally. The cost function is the maximum logic depth of the final design; smaller is better.
8. Please write the current design to the output file test28_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
