# test36 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test36.v` (13953 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test36.
2. Please load the design from the file test36.v located in the directory testcase/test36/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether wire n10239 is a cut between any primary input and any primary output. Report yes or no.
5. Verify functional equivalence between the current design and the original loaded netlist.
6. Report any AND gates with a constant 0 input in this design.
7. Simplify the reported AND gates by propagating their constant 0 input. Ensure the design functionality does not change.
8. How many AND gates were eliminated by constant-0 propagation?
9. What type of gate is g0? Report its gate type and pin connections.
10. What is the maximum logic depth from any primary input to any DFF D-pin in this design?
11. Check whether the function at n11 is symmetric with respect to inputs n3 and n9[0].
12. List all flip-flops driven by clock n0.
13. Which primary input has the highest fanout in this design?
14. Insert buffers wherever needed so that no signal drives more than 16 loads. Make sure nothing changes functionally. The cost function is the total gate count of the final design; smaller is better.
15. What is the maximum fanout of n1 now?
16. What is the fanout of primary input n0? List every gate that n0 drives directly.
17. Please write the current design to the output file test36_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
