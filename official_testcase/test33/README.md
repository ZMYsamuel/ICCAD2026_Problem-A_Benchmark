# test33 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test33.v` (72418 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test33.
2. Please load the design from the file test33.v located in the directory testcase/test33/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Find all paths of length 0 (direct wire connections from PI to PO).
5. Convert every XNOR gate in this design to an equivalent NOR-only circuit. Ensure the design functionality does not change.
6. How many NOR gates are now in the design after the XNOR-to-NOR conversion?
7. Check if there are any dangling gates in this design that do not contribute to any primary output. Remove them if found. Ensure the design functionality does not change.
8. How many dangling gates were removed?
9. Try to restructure the logic cone of output n8 using only NAND and NOT gates while preserving functional equivalence. Ensure the design functionality does not change.
10. How many NAND gates are now in the restructured cone of output n8?
11. Check whether internal signals n55146 and n55104 are functionally equivalent for all input combinations. Report yes or no.
12. List every path originating at primary input n3 and terminating at primary output n9.
13. Does output n8 depend on input n1? Report yes or no.
14. Attempt to reduce the depth of the cone of n8 to 4. If no improvement is possible, report the cone is already optimized.
15. Check whether the current netlist is functionally equivalent to the netlist as last loaded from disk.
16. Determine whether wire n55104 is a cut between any primary input and any primary output. Report yes or no.
17. Please list all the primary inputs of this design with their bit widths.
18. Try to merge any pairs of gates in this design that compute the same Boolean function on the same inputs (structural duplicates). Ensure the design functionality does not change.
19. How many gates were merged as structural duplicates?
20. Please write the current design to the output file test33_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
