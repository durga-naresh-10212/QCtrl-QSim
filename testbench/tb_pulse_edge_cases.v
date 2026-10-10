
`timescale 1ns / 1ps

module tb_pulse_edge_cases;
    integer fd;
    reg clk = 0;
    reg rst = 1;
    reg start = 0;
    reg [15:0] delay_cycles = 2;
    reg [15:0] pulse_cycles = 3;

    wire pulse_out;
    wire busy;
    wire done;

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

    initial begin
        $display("Starting QCtrl-QSim edge-case tests");
        fd = $fopen("edge_case_results.csv", "w");
        if (fd == 0)
            $fatal(1, "Could not open edge-case CSV");

        $fdisplay(fd, "test_name,status");

        // Test 1: Reset should clear outputs.
        repeat (2) @(negedge clk);
        if (pulse_out !== 0 || busy !== 0 || done !== 0)
            $fatal(1, "FAIL: outputs not cleared during reset");
        $display("PASS: reset clears outputs");

        rst = 0;

        // Test 2: No start command should leave controller idle.
        repeat (3) @(negedge clk);
        if (pulse_out !== 0 || busy !== 0)
            $fatal(1, "FAIL: controller not idle without start");
        $display("PASS: idle without start");

        // Test 3: Zero pulse length should be rejected.
        @(negedge clk);
        pulse_cycles = 0;
        delay_cycles = 2;
        start = 1;

        @(negedge clk);
        start = 0;

        repeat (4) @(negedge clk);
        if (pulse_out !== 0 || busy !== 0 || done !== 0)
            $fatal(1, "FAIL: zero pulse command was not rejected");
        $display("PASS: zero pulse length rejected");

        // Test 4: Zero delay should be rejected.
        @(negedge clk);
        pulse_cycles = 3;
        delay_cycles = 0;
        start = 1;

        @(negedge clk);
        start = 0;

        repeat (4) @(negedge clk);
        if (pulse_out !== 0 || busy !== 0 || done !== 0)
            $fatal(1, "FAIL: zero delay command was not rejected");
        $display("PASS: zero delay rejected");

        // Test 5: Reset during a pulse must clear outputs.
        delay_cycles = 1;
        pulse_cycles = 5;

        @(negedge clk);
        start = 1;

        @(negedge clk);
        start = 0;

        wait(pulse_out === 1'b1);
        @(negedge clk);
        rst = 1;

        @(negedge clk);
        if (pulse_out !== 0 || busy !== 0 || done !== 0)
            $fatal(1, "FAIL: reset during pulse did not clear outputs");
        $display("PASS: reset during pulse clears outputs");

        rst = 0;
        repeat (2) @(negedge clk);

        $display("All 5 edge-case tests passed.");
        $fdisplay(fd, "reset_clears_outputs,PASS");
        $fdisplay(fd, "no_start_command,PASS");
        $fdisplay(fd, "zero_pulse_length,PASS");
        $fdisplay(fd, "zero_delay,PASS");
        $fdisplay(fd, "reset_during_pulse,PASS");
        $fclose(fd);
        $finish;
    end

    initial begin
        #2000;
        $fatal(1, "TIMEOUT: edge-case testbench did not finish");
    end

endmodule
