// case_spec_gaps/design.v
// Hand-crafted small design to exercise problem-statement §4.3 example
// transformations not covered by the existing community testcases:
//   - Fanout reduction: net `hi` is driven by a single buffer and fans out
//     to 4 consumers, providing a target for max-fanout-2 splitting.
//   - Gate insertion based on naming patterns: two buffer instances are
//     prefixed `BUF_` — the problem-spec example asks for "Insert AND gates
//     before all buffers with certain naming patterns."
//   - Dangling-gate removal: `DANGLE_NOT` and `DANGLE_AND` form a small
//     subcircuit that is never connected to any primary output.

module spec_gaps (a, b, c, d, e, f, out0, out1);
  input a, b, c, d, e, f;
  output out0, out1;

  wire hi;                   // high-fanout net driven by BUF_main
  wire w1;                   // buffered alias of `b` via BUF_aux
  wire w2, w3, w4, w5;
  wire dangle1, dangle2;     // dangling: never reaches out0 or out1

  // Naming-pattern buffers (target for spec §4.3 gate-insertion-by-pattern).
  buf BUF_main (hi, a);
  buf BUF_aux  (w1, b);

  // hi has fanout 4 (target for fanout reduction).
  and AND_a (w2, hi, c);
  and AND_b (w3, hi, d);
  or  OR_a  (w4, hi, w1);
  not NOT_a (w5, hi);

  // Combine into the two POs.
  and FINAL_AND (out0, w2, w4);
  xor FINAL_XOR (out1, w3, w5);

  // Dangling logic: feeds nothing observable.
  not DANGLE_NOT (dangle1, e);
  and DANGLE_AND (dangle2, dangle1, f);

endmodule
