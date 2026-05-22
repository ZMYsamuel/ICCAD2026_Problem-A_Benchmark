# test37 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test37.v` (52640 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test37.
2. Please load the design from the file test37.v located in the directory testcase/test37/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Report the number of each gate type in the cone of n8.
5. Try to restructure the logic cone of output n8 using only NAND and NOT gates while preserving functional equivalence. Ensure the design functionality does not change.
6. How many NAND gates are now in the restructured cone of output n8?
7. Prune the netlist of unused gates. Make sure nothing changes functionally.
8. Check whether the current netlist is functionally equivalent to the netlist as last loaded from disk.
9. List all register-to-register paths in this design through combinational logic.
10. How many primary inputs and primary outputs does this design have?
11. List all primary outputs of this design with their bit widths.
12. List all gates with one or more inputs tied to 1'b1.
13. Try to restructure the logic cone of output n9 using only NOR and NOT gates while preserving functional equivalence. Ensure the design functionality does not change.
14. How many NOR gates are now in the restructured cone of output n9?
15. What Boolean function does output n8 compute? Express it in terms of the primary inputs.
16. Check if there are any floating inputs or unconnected output ports in this design.
17. How many floating signals were found?
18. Report every gate connected to the output of g0.
19. Check whether the function at n8 is symmetric with respect to inputs n3 and n4[0].
20. Please write the current design to the output file test37_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
