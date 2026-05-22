# test38 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test38.v` (4707 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test38.
2. Please load the design from the file test38.v located in the directory testcase/test38/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Try to insert buffers on the reset signal n1 to reduce its fanout to at most 4 loads per driver. Ensure the design functionality does not change.
5. What is the maximum fanout of n1 now?
6. Which primary input has the highest fanout in this design?
7. Find all pairs of back-to-back inverters (NOT followed by NOT) in this design and collapse them into direct wire connections. Ensure the design functionality does not change.
8. What is the maximum combinational logic depth in the design now?
9. Are there any redundant gates in this design that can be removed without changing functionality? Remove them if found. Ensure the design functionality does not change.
10. How many redundant gates were removed?
11. Find all paths of length 0 (direct wire connections from PI to PO).
12. Find all articulation points in the combinational graph between n2 and n14.
13. Update the name of signal n440 to renamed_wire throughout the netlist. Ensure the design functionality does not change.
14. Confirm that the design is still functionally equivalent to the original.
15. Report any NAND gates with constant inputs (0 or 1) in this design.
16. Simplify the reported NAND gates by propagating their constant inputs. Ensure the design functionality does not change.
17. How many NAND gates were eliminated by constant propagation?
18. Report the number of each gate type in the cone of n14.
19. Compute the fanin logic cone of output n14 and list all gates that contribute to this output.
20. Please write the current design to the output file test38_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
