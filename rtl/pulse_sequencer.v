module pulse_sequencer #(
    parameter WIDTH = 16
)(
    input wire clk,
    input wire rst,
    input wire start,
    input wire [WIDTH-1:0] delay_cycles,
    input wire [WIDTH-1:0] pulse_cycles,

    output reg pulse_out,
    output reg busy,
    output reg done
);

    localparam IDLE  = 2'b00;
    localparam DELAY = 2'b01;
    localparam PULSE = 2'b10;
    localparam FINISH = 2'b11;

    reg [1:0] state;
    reg [WIDTH-1:0] counter;
    reg [WIDTH-1:0] delay_reg;
    reg [WIDTH-1:0] pulse_reg;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            state     <= IDLE;
            counter   <= 0;
            delay_reg <= 0;
            pulse_reg <= 0;
            pulse_out <= 0;
            busy      <= 0;
            done      <= 0;
        end else begin
            done <= 0;

            case (state)
                IDLE: begin
                    pulse_out <= 0;
                    busy      <= 0;
                    counter   <= 0;

                    if (start && delay_cycles != 0 &&
                                pulse_cycles != 0) begin
                        delay_reg <= delay_cycles;
                        pulse_reg <= pulse_cycles;
                        counter   <= 0;
                        busy      <= 1;
                        state     <= DELAY;
                    end
                end

                DELAY: begin
                    busy      <= 1;
                    pulse_out <= 0;

                    if (counter == delay_reg - 1'b1) begin
                        counter   <= 0;
                        pulse_out <= 1;
                        state     <= PULSE;
                    end else begin
                        counter <= counter + 1'b1;
                    end
                end

                PULSE: begin
                    busy <= 1;

                    if (counter == pulse_reg - 1'b1) begin
                        counter   <= 0;
                        pulse_out <= 0;
                        state     <= FINISH;
                    end else begin
                        counter   <= counter + 1'b1;
                        pulse_out <= 1;
                    end
                end

                FINISH: begin
                    pulse_out <= 0;
                    busy      <= 0;
                    done      <= 1;
                    state     <= IDLE;
                end

                default: begin
                    state     <= IDLE;
                    counter   <= 0;
                    pulse_out <= 0;
                    busy      <= 0;
                    done      <= 0;
                end
            endcase
        end
    end

endmodule