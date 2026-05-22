# test15 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test15.v` (247 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test15.
2. Please load the design from the file test15.v located in the directory testcase/test15/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n0[0] to n3 exists that does not traverse node n207.
5. Verify whether a path connecting input n0[1] to output n4 exists while avoiding n29.
6. List every path originating at primary input n0[1] and terminating at primary output n4.
7. Provide a complete enumeration of paths between n0[2] and n3.
8. Compute the maximum logic depth from input n0[0] to output n3.
9. Determine the longest combinational path depth from n0[1] to n4.
10. Determine the number of gates driven by g0.
11. Enumerate the immediate successors of gate g0.
12. Compute the transitive fanin cone of output n3.
13. Compute the transitive fanout cone of input n0[0].
14. Please write the current design to the output file test15_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
