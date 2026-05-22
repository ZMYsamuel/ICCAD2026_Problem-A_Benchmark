# test25 — official 0510 release

**Source**: Cadence Design Systems, official release 2026-05-10.
**Netlist**: `test25.v` (848 lines)

## Prompts

1. This is the beginning of a new testcase. The case name is test25.
2. Please load the design from the file test25.v located in the directory testcase/test25/.
3. Please count all the gates in this design and report the total count broken down by gate type (AND, OR, NOT, NAND, NOR, XOR, XNOR, BUF, DFF).
4. Perform depth optimization on the combinational logic. Ensure functional equivalence is preserved.
5. Eliminate unused logic gates from the netlist. Ensure functional equivalence is preserved.
6. Change the identifier of gate g0 to renamed_gate and update all references. Ensure the design functionality does not change.
7. Change the identifier of wire n74 to renamed_wire and update all references. Ensure the design functionality does not change.
8. Replace all 2-input OR gates in the cone of n11[0] with equivalent logic built only from NAND and NOT gates. Ensure the design functionality does not change.
9. Please write the current design to the output file test25_out.v.

## Notes

Golden answers are placeholders until human-reviewed. See `meta.yaml` for per-prompt task_type / expected.kind heuristic classifications.
