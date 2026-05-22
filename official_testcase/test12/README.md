# test12 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test12.v` (103034 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test12.
2. Please load the design from the file test12.v located in the directory testcase/test12/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether a combinational path from n24[0] to n26[0] exists that does not traverse node n86984.
5. Verify whether a path connecting input n24[1] to output n26[1] exists while avoiding n87234.
6. List every path originating at primary input n24[1] and terminating at primary output n26[1].
7. Provide a complete enumeration of paths between n24[2] and n26[0].
8. Compute the maximum logic depth from input n24[0] to output n26[0].
9. Determine the longest combinational path depth from n24[1] to n26[1].
10. Determine the number of gates driven by g0.
11. Please write the current design to the output file test12_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
