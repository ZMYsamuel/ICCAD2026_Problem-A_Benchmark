# test17 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test17.v` (3573 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test17.
2. Please load the design from the file test17.v located in the directory testcase/test17/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n7 to n42[0] exists that does not traverse node n1034.
5. Verify whether a path connecting input n8 to output n42[1] exists while avoiding n2116.
6. List every path originating at primary input n8 and terminating at primary output n42[1].
7. Provide a complete enumeration of paths between n9 and n42[0].
8. Compute the maximum logic depth from input n7 to output n42[0].
9. Determine the longest combinational path depth from n8 to n42[1].
10. Calculate the critical path depth between n9 and n42[0].
11. Determine the number of gates driven by g0.
12. Enumerate the immediate successors of gate g0.
13. Compute the transitive fanin cone of output n42[0].
14. Compute the transitive fanout cone of input n7.
15. Determine whether signals n2122 and n2116 are functionally equivalent.
16. Please write the current design to the output file test17_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
