// demo_gate.v
// ICCAD 2026 Problem A — Demo Circuit
//
// Purpose: showcase NetlistGraph analysis API with meaningful
//          combinational depth, path queries, and a DFF.
//
// Circuit topology:
//
//   a ──┬──[U1: AND]──n1──┬──[G_mid: OR]──n3──┬──[U4: NAND]──n4──[U5: BUF]──out0
//   b ──┘                 │                    │
//   c ──[U2: NOT]──n2─────┘────────────────────┘
//
//   a ──┬──[U6: XOR]──n5──[U7: AND]──n6──[FF1: DFF]──q1──[U8: BUF]──out1
//   b ──┘                        c ──┘
//
//   n4, q1 ──[U9: NOR]──n7──[U10: NOT]──out2
//
// Key analysis properties (for demo):
//   Q1: Max depth  a  →  out0  = 4  (U1, G_mid, U4, U5)
//   Q2: Every path a  →  out0  passes through G_mid? → TRUE
//   Q3: Max depth  c  →  out0  = 4  (U2, G_mid, U4, U5)
//   Q4: POs with cone > 3 gates → out0 (5 gates), out2 (10 gates)
//
// DFF port order (positional): dff inst (q, d, clk, rst_n)

module demo_circuit (
    input  wire a,
    input  wire b,
    input  wire c,
    input  wire clk,
    input  wire rst_n,
    output wire out0,
    output wire out1,
    output wire out2
);
    wire   n1, n2, n3, n4, n5, n6, n7, q1;

    // ── Combinational cone → out0 (depth 4) ───────────────────────────────────
    and  U1    (n1, a, b);        // n1  = a & b
    not  U2    (n2, c);           // n2  = ~c
    or   G_mid (n3, n1, n2);      // n3  = n1 | n2
    nand U4    (n4, n3, n2);      // n4  = ~(n3 & n2)
    buf  U5    (out0, n4);        // out0 = n4

    // ── Sequential cone → out1 ────────────────────────────────────────────────
    xor  U6  (n5, a, b);          // n5  = a ^ b
    and  U7  (n6, n5, c);         // n6  = n5 & c
    dff  FF1 (q1, n6, clk, rst_n);// q1  = FF output   (d=n6, clk, rst_n)
    buf  U8  (out1, q1);          // out1 = q1

    // ── Mixed cone → out2 (combinational + sequential) ────────────────────────
    nor  U9  (n7, n4, q1);        // n7  = ~(n4 | q1)
    not  U10 (out2, n7);          // out2 =  n4 | q1

endmodule

// ─── DFF primitive (positional: q, d, clk, rst_n) — ABC-compatible ────────────
module dff (
    output reg  q,
    input  wire d,
    input  wire clk,
    input  wire rst_n
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) q <= 1'b0;
        else        q <= d;
    end
endmodule