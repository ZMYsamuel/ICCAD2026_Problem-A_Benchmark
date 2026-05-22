# test07 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test07.v` (1057 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test07.
2. Please load the design from the file test07.v located in the directory testcase/test07/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n0[0] to n5 exists that does not traverse node n95.
5. Verify whether a path connecting input n0[1] to output n6 exists while avoiding n94.
6. Please write the current design to the output file test07_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
