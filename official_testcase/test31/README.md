# test31 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test31.v` (6899 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test31.
2. Please load the design from the file test31.v located in the directory testcase/test31/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine all gates reachable from n2.
5. Find all back-to-back inverter pairs and collapse them into a wire. Ensure functional equivalence is preserved.
6. Prove that the transformed design is equivalent to the pre-transformation netlist.
7. What is the fanout of primary input n0? List every gate that n0 drives directly.
8. Is output n16 always 0 regardless of all inputs? Report yes or no.
9. Report all gates shared between the fanin cones of n16 and n17.
10. Derive the Boolean equation for output n16 in terms of its primary inputs.
11. Report every gate connected to the output of g0.
12. Try to rename internal signal n1289 to renamed_sig and update all references to it. Ensure the design functionality does not change.
13. List all gates that now connect to the renamed signal renamed_sig.
14. Please insert a BUF gate on signal n2 so that each load of n2 is driven through a dedicated buffer. Ensure the design functionality does not change.
15. How many BUF gates were added by the buffer insertion just performed?
16. What is the maximum logic depth from any primary input to any DFF D-pin in this design?
17. How many outputs have a logic depth greater than 4?
18. What type of gate is g0? Report its gate type and pin connections.
19. Check functional equivalence between internal signals n1287 and n2404.
20. Please write the current design to the output file test31_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
