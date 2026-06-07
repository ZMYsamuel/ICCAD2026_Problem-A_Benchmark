# test_propconst - Constant Propagation

## Design

`test_propconst.v` (module `top`): a 21-gate combinational netlist deliberately constructed so that every supported `propagate_constants` simplification action fires at least once. Inputs `a, b, c, d`; outputs `o1..o18`.

Each gate is annotated with the expected propagation result:

| Category | Count | Gates | Expected outcome |
|---|---|---|---|
| const-output (gate eliminated, output wire becomes const) | 4 | g1, g3, g6, g8 | `o1=0, o3=1, o6=1, o8=0` |
| bypass (gate eliminated, consumers rewired to surviving input) | 4 | g2, g4, g9, g11 | `o2=b, o4=d, o9=a, o11=c` |
| convert-to-NOT (2-input gate degenerates to NOT) | 4 | g5, g7, g10, g12 | `o5=~a, o7=~c, o10=~b, o12=~d` |
| unary on a constant | 2 | g13 (BUF 1), g14 (NOT 0) | `o13=1, o14=1` |
| both inputs constant (full evaluation) | 1 | g15 | `o15=0` |
| cascade (g16a -> g16) | 2 | g16a, g16 | `o16=b` |
| multi-step chain (g17a -> g17b -> g17) | 3 | g17a, g17b, g17 | `o17=c` |
| untouched (no constant input) | 1 | g18 | `o18=a^b` |

## Expected outcome after `propagate_constants`

- 16 gates eliminated (const-output 9 + bypass 7 once the cascade/chain unfolds).
- 4 gates converted to NOT.
- Final netlist: 4 NOT + 1 XOR = 5 gates, with all 18 outputs equivalent to the original.

## Questions (9 total)

1. Init.
2. Load `test_propconst.v`.
3. Pre-pass gate-count by type.
4. Enumerate gates whose input pins include a constant.
5. Apply constant propagation (preserve functional equivalence).
6. Report gates eliminated by constant propagation.
7. Equivalence check vs. originally-loaded netlist.
8. Post-pass gate-count by type.
9. Write the simplified netlist to `test_propconst_out.v`.

## Notes for reviewers

- Equivalence must hold across the entire truth table over `(a, b, c, d)` for every `o1..o18`.
- The cascade (g16) and the 3-stage chain (g17) require the pass to fixed-point - a single sweep is insufficient.
- g18 (`xor a, b`) has no constant input and must survive unchanged. It is the only gate that should remain other than the 4 converted NOTs.