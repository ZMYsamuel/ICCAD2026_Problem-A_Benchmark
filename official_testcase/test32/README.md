# test32 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test32.v` (15672 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test32.
2. Please load the design from the file test32.v located in the directory testcase/test32/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Determine whether gate g0 lies on any maximum-depth path of the design. Report yes or no.
5. Determine the number of primary inputs and outputs.
6. List all register-to-register paths in this design through combinational logic.
7. Try to replace all 2-input NAND gates that have one input tied to constant 1 with inverters. Ensure the design functionality does not change.
8. How many NOT gates are currently in the design?
9. Does every path from input n2 to output n12 pass through gate g0? Report yes or no.
10. Rename wire n1214 to renamed_wire. Ensure functional equivalence is preserved.
11. Verify functional equivalence between the current design and the original loaded netlist.
12. What is the transitive fanout of primary input n0? List all gates reachable from n0.
13. How many gates are in the logic cone of output n12?
14. Check if there are any dangling gates in this design that do not contribute to any primary output. Remove them if found. Ensure the design functionality does not change.
15. How many dangling gates were removed?
16. Report any NAND gates with constant inputs (0 or 1) in this design.
17. Simplify the reported NAND gates by propagating their constant inputs. Ensure the design functionality does not change.
18. How many NAND gates were eliminated by constant propagation?
19. Find all combinational paths from primary input n2 to primary output n12 and list each path showing the gates traversed.
20. Please write the current design to the output file test32_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
