# test20 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test20.v` (16174 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test20.
2. Please load the design from the file test20.v located in the directory testcase/test20/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n13 to n25[0] exists that does not traverse node n2240.
5. Verify whether a path connecting input n14 to output n25[1] exists while avoiding n13083.
6. List every path originating at primary input n14 and terminating at primary output n25[1].
7. Provide a complete enumeration of paths between n15 and n25[0].
8. Compute the maximum logic depth from input n13 to output n25[0].
9. Determine the longest combinational path depth from n14 to n25[1].
10. Calculate the critical path depth between n15 and n25[0].
11. Determine the number of gates driven by g0.
12. Enumerate the immediate successors of gate g0.
13. Compute the transitive fanin cone of output n25[0].
14. Compute the transitive fanout cone of input n13.
15. Determine whether signals n13082 and n13083 are functionally equivalent.
16. Verify that n2257 and n2184 produce identical logic values for all inputs.
17. Check functional equivalence between internal signals n2233 and n2193.
18. Compute the total gate count of the design.
19. Please write the current design to the output file test20_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
