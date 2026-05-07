// case_basic_io — minimal valid design for testcase init / load / write smoke test.
// Single 2-input AND gate. No DFF. No analysis or transform.

module simple_and (
    input  wire a,
    input  wire b,
    output wire y
);
    and U1 (y, a, b);
endmodule
