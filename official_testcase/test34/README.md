# test34 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test34.v` (26701 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test34.
2. Please load the design from the file test34.v located in the directory testcase/test34/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Try to insert buffers on the clock signal n0 to reduce its fanout so no single driver has more than 4 loads. Ensure the design functionality does not change.
5. What is the maximum fanout of n0 now?
6. Check whether the current netlist is functionally equivalent to the netlist as last loaded from disk.
7. Write the logic expression for n30 using only the primary input names.
8. Does a combinational path from n2 to n30 exist that avoids n4552?
9. Rewrite all XNOR gates using only NOR and NOT gates. Ensure the design functionality does not change.
10. Report the total NOR gate count after replacing all XNOR gates.
11. Please insert a BUF gate on signal n2 so that each load of n2 is driven through a dedicated buffer. Ensure the design functionality does not change.
12. How many BUF gates were added by the buffer insertion just performed?
13. Perform fanout optimization across the netlist with maximum fanout 4. Ensure functional equivalence is preserved.
14. Confirm that the design is still functionally equivalent to the original.
15. What is the maximum combinational depth from any primary input to any primary output in the entire design?
16. Which output bit has the deepest fanin logic cone?
17. What is the fanout of primary input n0? List every gate that n0 drives directly.
18. Reconstruct the entire netlist using only AND and NOT gates while preserving functional equivalence. Ensure the design functionality does not change.
19. How many AND gates are now in the reconstructed netlist?
20. Please write the current design to the output file test34_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
