# test09 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test09.v` (2220 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test09.
2. Please load the design from the file test09.v located in the directory testcase/test09/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n0 to n117[0] exists that does not traverse node n1816.
5. Verify whether a path connecting input n1 to output n117[1] exists while avoiding n1646.
6. List every path originating at primary input n1 and terminating at primary output n117[1].
7. Provide a complete enumeration of paths between n2 and n117[0].
8. Please write the current design to the output file test09_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
