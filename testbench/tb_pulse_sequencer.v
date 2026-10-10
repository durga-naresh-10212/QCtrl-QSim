
`timescale 1ns / 1ps

module tb_pulse_sequencer;

    reg clk = 0;
    reg rst = 1;
    reg start = 0;

    reg [15:0] delay_cycles = 2;
    reg [15:0] pulse_cycles = 3;

    wire pulse_out;
    wire busy;
    wire done;

    integer fd;
    integer measured_cycles;
    integer expected_cycles;
    integer delay_used;
    integer pass_count;
    integer fail_count;
    integer i;
    integer j;
    reg measuring;

    pulse_sequencer dut (
        .clk(clk),
        .rst(rst),
        .start(start),
        .delay_cycles(delay_cycles),
        .pulse_cycles(pulse_cycles),
        .pulse_out(pulse_out),
        .busy(busy),
        .done(done)
    );

    always #5 clk = ~clk;

    // Count high pulse intervals at falling edges.
    always @(negedge clk) begin
        if (rst) begin
            measured_cycles = 0;
            measuring = 0;
        end else if (pulse_out === 1'b1) begin
            measured_cycles = measured_cycles + 1;
            measuring = 1;
        end else if (measuring) begin
            if (measured_cycles == expected_cycles) begin
                $display(
                    "PASS: delay=%0d pulse=%0d measured=%0d",
                    delay_used, expected_cycles, measured_cycles
                );
                $fdisplay(fd, "%0d,%0d,%0d,PASS",
                          delay_used, expected_cycles,
                          measured_cycles);
                pass_count = pass_count + 1;
            end else begin
                $display(
                    "FAIL: delay=%0d expected=%0d measured=%0d",
                    delay_used, expected_cycles, measured_cycles
                );
                $fdisplay(fd, "%0d,%0d,%0d,FAIL",
                          delay_used, expected_cycles,
                          measured_cycles);
                fail_count = fail_count + 1;
            end

            measured_cycles = 0;
            measuring = 0;
        end
    end

    task run_test;
        input integer delay_value;
        input integer pulse_value;
        begin
            delay_used = delay_value;
            expected_cycles = pulse_value;

            @(negedge clk);
            delay_cycles = delay_value;
            pulse_cycles = pulse_value;
            start = 1;

            @(negedge clk);
            start = 0;

            wait(done == 1);
            repeat (2) @(negedge clk);
        end
    endtask

    initial begin
        measured_cycles = 0;
        expected_cycles = 3;
        delay_used = 2;
        measuring = 0;
        pass_count = 0;
        fail_count = 0;

        fd = $fopen("rtl_timing_sweep.csv", "w");
        if (fd == 0)
            $fatal(1, "Could not open CSV output");

        $fdisplay(fd,
            "delay_cycles,expected_cycles,measured_cycles,status");

        repeat (2) @(negedge clk);
        rst = 0;

        // Three delay settings and four pulse widths.
        for (i = 1; i <= 3; i = i + 1) begin
            for (j = 1; j <= 4; j = j + 1) begin
                case (j)
                    1: run_test(i, 1);
                    2: run_test(i, 2);
                    3: run_test(i, 3);
                    4: run_test(i, 5);
                endcase
            end
        end

        $fclose(fd);

        $display("--------------------------------");
        $display("Passed: %0d", pass_count);
        $display("Failed: %0d", fail_count);

        if (pass_count != 12 || fail_count != 0)
            $fatal(1, "RTL timing sweep failed");

        $display("All 12 RTL timing tests passed.");
        $finish;
    end

endmodule
