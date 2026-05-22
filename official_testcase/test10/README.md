# test10 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test10.v` (5452 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test10.
2. Please load the design from the file test10.v located in the directory testcase/test10/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n12 to n25[0] exists that does not traverse node n1127.
5. Verify whether a path connecting input n13 to output n25[1] exists while avoiding n4156.
6. List every path originating at primary input n13 and terminating at primary output n25[1].
7. Provide a complete enumeration of paths between n14 and n25[0].
8. Compute the maximum logic depth from input n12 to output n25[0].
9. Please write the current design to the output file test10_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
