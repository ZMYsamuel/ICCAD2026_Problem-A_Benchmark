# test14 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test14.v` (17162 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test14.
2. Please load the design from the file test14.v located in the directory testcase/test14/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n61 to n63[0] exists that does not traverse node n4363.
5. Verify whether a path connecting input n0[0] to output n63[1] exists while avoiding n141.
6. List every path originating at primary input n0[0] and terminating at primary output n63[1].
7. Provide a complete enumeration of paths between n0[1] and n63[0].
8. Compute the maximum logic depth from input n61 to output n63[0].
9. Determine the longest combinational path depth from n0[0] to n63[1].
10. Calculate the critical path depth between n0[1] and n63[0].
11. Determine the number of gates driven by g0.
12. Enumerate the immediate successors of gate g0.
13. Please write the current design to the output file test14_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
