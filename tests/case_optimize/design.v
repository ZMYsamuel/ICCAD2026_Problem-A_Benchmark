// case_optimize — redundant gates that ABC's resyn2 should collapse.
//
// y = ((a & b) & a) & b
//   = a & b   (idempotent: a&a = a, b&b = b)
//
// 4-gate implementation that reduces to a 1-gate y = a&b after optimization.
//
// dff is included so the file passes ABC's read_verilog without complaint
// even though the design itself is purely combinational.

module redundant_and (
    input  wire a,
    input  wire b,
    output wire y
);
    wire t1, t2, t3;

    and U1 (t1, a, b);    // t1 = a & b
    and U2 (t2, t1, a);   // t2 = (a&b) & a = a&b  (redundant)
    and U3 (t3, t2, b);   // t3 = (a&b) & b = a&b  (redundant)
    buf U4 (y,  t3);      // y  = t3 = a&b         (redundant)
endmodule

// ABC-compatible DFF primitive (unused here but kept for parser compatibility).
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
