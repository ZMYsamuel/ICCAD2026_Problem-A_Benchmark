# test36 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test36.v` (13953 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test36.
2. Please load the design from the file test36.v located in the directory testcase/test36/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether wire n10239 is a cut between any primary input and any primary output. Report yes or no.
5. Insert buffers wherever needed so that no gate drives more than 4 loads. Make sure nothing changes functionally.
6. Verify functional equivalence between the current design and the original loaded netlist.
7. Report any AND gates with a constant 0 input in this design.
8. Simplify the reported AND gates by propagating their constant 0 input. Ensure the design functionality does not change.
9. How many AND gates were eliminated by constant-0 propagation?
10. What type of gate is g0? Report its gate type and pin connections.
11. What is the maximum logic depth from any primary input to any DFF D-pin in this design?
12. Check whether the function at n11 is symmetric with respect to inputs n3 and n9[0].
13. Try to reconnect input pin A of gate g0 to internal signal n24[0]. Ensure the design functionality does not change.
14. List all gates currently driven by signal n24[0].
15. What is the fanout of primary input n0? List every gate that n0 drives directly.
16. List all flip-flops driven by clock n0.
17. Try to insert buffers on the reset signal n1 to reduce its fanout to at most 4 loads per driver. Ensure the design functionality does not change.
18. What is the maximum fanout of n1 now?
19. Which primary input has the highest fanout in this design?
20. Please write the current design to the output file test36_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
