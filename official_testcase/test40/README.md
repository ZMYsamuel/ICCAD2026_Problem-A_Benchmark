# test40 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test40.v` (29065 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test40.
2. Please load the design from the file test40.v located in the directory testcase/test40/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Insert buffers wherever needed so that no gate in the design drives more than 4 loads. Ensure functional equivalence is preserved.
5. Verify functional equivalence between the current design and the original loaded netlist.
6. Remap the entire design to use only NAND and NOT gates. Make sure nothing changes functionally.
7. Try to optimize the logic cone of output n14 targeting depth 4 or less. Ensure the design functionality does not change. Report original if already optimal.
8. What is the depth of the cone of n14 now?
9. Try to replace all 2-input NAND gates that have one input tied to constant 1 with inverters. Ensure the design functionality does not change.
10. How many NOT gates are currently in the design?
11. Find all pairs of back-to-back inverters (NOT followed by NOT) in this design and collapse them into direct wire connections. Ensure the design functionality does not change.
12. What is the maximum combinational logic depth in the design now?
13. List all primary outputs of this design with their bit widths.
14. List all XOR gates in this design.
15. What is the maximum combinational depth on any register-to-register path in this design?
16. Report the D input logic of the flip-flops to report any existing enable or hold structures implemented through multiplexers or AND gates.
17. How many flip-flops were found to have enable or hold structures in their D input logic?
18. What type of gate is g0? Report its gate type and pin connections.
19. Which output has the largest fanin cone?
20. Please write the current design to the output file test40_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
