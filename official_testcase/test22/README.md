# test22 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test22.v` (2187 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test22.
2. Please load the design from the file test22.v located in the directory testcase/test22/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Insert buffers wherever needed so that no gate drives more than 4 loads. Make sure nothing changes functionally.
5. Reduce the critical path depth through restructuring. Make sure nothing changes functionally.
6. Please write the current design to the output file test22_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
