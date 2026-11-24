// Bounded Verilog reference with synchronous reset.
module counter(input wire clk, input wire rst, input wire en, output reg [7:0] q);
  always @(posedge clk)
    if (rst) q <= 8'b0;
    else if (en) q <= q + 8'd1;
endmodule
