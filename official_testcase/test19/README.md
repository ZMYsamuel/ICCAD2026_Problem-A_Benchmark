# test19 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test19.v` (785 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test19.
2. Please load the design from the file test19.v located in the directory testcase/test19/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n3 to n17[0] exists that does not traverse node n269.
5. Verify whether a path connecting input n4 to output n17[1] exists while avoiding n269.
6. List every path originating at primary input n4 and terminating at primary output n17[1].
7. Provide a complete enumeration of paths between n5 and n17[0].
8. Compute the maximum logic depth from input n3 to output n17[0].
9. Determine the longest combinational path depth from n4 to n17[1].
10. Calculate the critical path depth between n5 and n17[0].
11. Determine the number of gates driven by g0.
12. Enumerate the immediate successors of gate g0.
13. Compute the transitive fanin cone of output n17[0].
14. Compute the transitive fanout cone of input n3.
15. Determine whether signals n296 and n269 are functionally equivalent.
16. Verify that n273 and n275 produce identical logic values for all inputs.
17. Check functional equivalence between internal signals n270 and n243.
18. Please write the current design to the output file test19_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
