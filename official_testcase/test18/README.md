# test18 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test18.v` (9613 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test18.
2. Please load the design from the file test18.v located in the directory testcase/test18/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n0[0] to n12 exists that does not traverse node n1038.
5. Verify whether a path connecting input n0[1] to output n13 exists while avoiding n1080.
6. List every path originating at primary input n0[1] and terminating at primary output n13.
7. Provide a complete enumeration of paths between n0[2] and n12.
8. Compute the maximum logic depth from input n0[0] to output n12.
9. Determine the longest combinational path depth from n0[1] to n13.
10. Determine the number of gates driven by g0.
11. Enumerate the immediate successors of gate g0.
12. Compute the transitive fanin cone of output n12.
13. Compute the transitive fanout cone of input n0[0].
14. Determine whether signals n848 and n1080 are functionally equivalent.
15. Verify that n1039 and n1046 produce identical logic values for all inputs.
16. Check functional equivalence between internal signals n1035 and n1029.
17. Please write the current design to the output file test18_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
