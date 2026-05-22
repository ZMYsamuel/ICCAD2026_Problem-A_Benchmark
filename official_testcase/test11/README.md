# test11 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test11.v` (1833 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test11.
2. Please load the design from the file test11.v located in the directory testcase/test11/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n29 to n31[0] exists that does not traverse node n1552.
5. Verify whether a path connecting input n30 to output n31[1] exists while avoiding n1592.
6. List every path originating at primary input n30 and terminating at primary output n31[1].
7. Provide a complete enumeration of paths between n0[0] and n31[0].
8. Compute the maximum logic depth from input n29 to output n31[0].
9. Determine the longest combinational path depth from n30 to n31[1].
10. Please write the current design to the output file test11_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
