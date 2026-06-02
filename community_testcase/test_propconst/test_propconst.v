// Test netlist for propagate constants(official test32/36/38/39).
// Each gate exercises a specific simplification action.

module top(a, b, c, d,
           o1, o2, o3, o4, o5, o6, o7, o8, o9, o10,
           o11, o12, o13, o14, o15, o16, o17, o18);
  input a, b, c, d;
  output o1, o2, o3, o4, o5, o6, o7, o8, o9, o10;
  output o11, o12, o13, o14, o15, o16, o17, o18;
  wire w_and0, w_chain1, w_chain2;

  // ---- const-output cases (gate is eliminated, output wire becomes const) ----
  and  g1 (o1, 1'b0, a);    // AND(0, a)  = 0
  or   g3 (o3, 1'b1, c);    // OR (1, c)  = 1
  nand g6 (o6, 1'b0, b);    // NAND(0, b) = 1
  nor  g8 (o8, 1'b1, d);    // NOR(1, d)  = 0

  // ---- bypass cases (gate is eliminated, consumers wired to surviving input) ----
  and  g2  (o2,  1'b1, b);  // AND(1, b)  = b
  or   g4  (o4,  1'b0, d);  // OR (0, d)  = d
  xor  g9  (o9,  1'b0, a);  // XOR(0, a)  = a
  xnor g11 (o11, 1'b1, c);  // XNOR(1, c) = c

  // ---- convert-to-NOT cases (2-input gate degenerates to NOT) ----
  nand g5  (o5,  1'b1, a);  // NAND(1, a) = ~a
  nor  g7  (o7,  1'b0, c);  // NOR(0, c)  = ~c
  xor  g10 (o10, 1'b1, b);  // XOR(1, b)  = ~b
  xnor g12 (o12, 1'b0, d);  // XNOR(0, d) = ~d

  // ---- unary on a constant ----
  buf  g13 (o13, 1'b1);     // BUF(1) = 1
  not  g14 (o14, 1'b0);     // NOT(0) = 1

  // ---- both inputs constant (full evaluation) ----
  and  g15 (o15, 1'b1, 1'b0); // AND(1, 0) = 0

  // ---- cascade: g16a becomes const 0, then g16 bypasses to b ----
  and  g16a (w_and0, 1'b0, a);
  or   g16  (o16, w_and0, b);

  // ---- multi-step chain: g17a -> g17b -> g17 ----
  not  g17a (w_chain1, 1'b0);          // -> 1
  and  g17b (w_chain2, w_chain1, c);   // AND(1, c) = c
  or   g17  (o17, w_chain2, 1'b0);     // OR (c, 0) = c

  // ---- untouched (no constant input) - sanity check that the tool leaves it alone ----
  xor  g18 (o18, a, b);
endmodule