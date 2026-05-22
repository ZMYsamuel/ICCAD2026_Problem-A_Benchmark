# test35 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test35.v` (38686 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test35.
2. Please load the design from the file test35.v located in the directory testcase/test35/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Try to replace all XNOR gates in this design with equivalent NOR-only implementations. Ensure the design functionality does not change.
5. How many NOR gates were added by replacing the XNOR gates?
6. Does a combinational path exist from primary input n2 to primary output n25? Report yes or no.
7. Report every gate connected to the output of g0.
8. Which output bit has the deepest fanin logic cone?
9. List all NAND gates in this design with their input and output signals.
10. Update the name of signal n7431 to renamed_wire throughout the netlist. Ensure the design functionality does not change.
11. Prove that the transformed design is equivalent to the pre-transformation netlist.
12. Check whether internal signals n29498 and n29471 are functionally equivalent for all input combinations. Report yes or no.
13. Does there exist any pair of internal signals (a, b) already in the netlist such that NAND(a, b) is equivalent to n25?
14. Find all pairs of back-to-back inverters (NOT followed by NOT) in this design and collapse them into direct wire connections. Ensure the design functionality does not change.
15. What is the maximum combinational logic depth in the design now?
16. What Boolean function does output n25 compute? Express it in terms of the primary inputs.
17. List all flip-flops driven by clock n0.
18. Try to replace all XOR gates in this design with equivalent NAND-only implementations. Each 2-input XOR can be realized with 4 NAND gates. Ensure the design functionality does not change.
19. How many NAND gates were added by replacing the XOR gates?
20. Please write the current design to the output file test35_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
