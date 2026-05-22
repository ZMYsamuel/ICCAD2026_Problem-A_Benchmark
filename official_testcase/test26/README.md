# test26 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test26.v` (2051 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test26.
2. Please load the design from the file test26.v located in the directory testcase/test26/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Perform fanout optimization across the netlist with maximum fanout 4. Ensure functional equivalence is preserved.
5. Reduce critical path depth through logic restructuring. Ensure functional equivalence is preserved.
6. Remove all dangling gates and nets not connected to any primary output. Make sure nothing changes functionally.
7. Convert the logic cone of n10 to use only NOR and NOT gates while preserving functional equivalence.
8. Try to restructure n10 with a target depth of 4, preserving functionality. Report original if already optimal.
9. Find all back-to-back inverter pairs and collapse them into a wire. Ensure functional equivalence is preserved.
10. Please write the current design to the output file test26_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
