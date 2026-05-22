# test13 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test13.v` (338 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test13.
2. Please load the design from the file test13.v located in the directory testcase/test13/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n2 to n5[0] exists that does not traverse node n58.
5. Verify whether a path connecting input n3 to output n5[1] exists while avoiding n208.
6. List every path originating at primary input n3 and terminating at primary output n5[1].
7. Provide a complete enumeration of paths between n4 and n5[0].
8. Compute the maximum logic depth from input n2 to output n5[0].
9. Determine the longest combinational path depth from n3 to n5[1].
10. Calculate the critical path depth between n4 and n5[0].
11. Determine the number of gates driven by g0.
12. Please write the current design to the output file test13_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
