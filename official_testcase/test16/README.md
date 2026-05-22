# test16 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test16.v` (18129 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test16.
2. Please load the design from the file test16.v located in the directory testcase/test16/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n6 to n33[0] exists that does not traverse node n16010.
5. Verify whether a path connecting input n7 to output n33[1] exists while avoiding n15819.
6. List every path originating at primary input n7 and terminating at primary output n33[1].
7. Provide a complete enumeration of paths between n8 and n33[0].
8. Compute the maximum logic depth from input n6 to output n33[0].
9. Determine the longest combinational path depth from n7 to n33[1].
10. Calculate the critical path depth between n8 and n33[0].
11. Determine the number of gates driven by g0.
12. Enumerate the immediate successors of gate g0.
13. Compute the transitive fanin cone of output n33[0].
14. Compute the transitive fanout cone of input n6.
15. Please write the current design to the output file test16_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
