
# QCtrl-QSim
### RTL-Aware Quantum Control Co-Simulation Framework

QCtrl-QSim is an experimental framework that connects Verilog-based
digital pulse sequencing with Python analysis and Qiskit Aer quantum-circuit
simulation.

The project investigates how finite digital timing resolution can affect
a simplified model of quantum rotation control.

## Project Objectives

- Implement a configurable pulse sequencer in Verilog.
- Verify pulse widths using Vivado behavioral simulation.
- Export RTL measurements to CSV.
- Analyze timing results using Python.
- Simulate modeled rotation-angle changes using Qiskit Aer.
- Study timing quantization under different hypothetical clock periods.

## Architecture

1. **RTL layer:** Verilog pulse sequencer with configurable delay and width.
2. **Verification layer:** Vivado testbenches for timing and edge cases.
3. **Data layer:** CSV exports from RTL simulation.
4. **Analysis layer:** Python timing calculations and validation.
5. **Quantum simulation layer:** Qiskit Aer circuits using RY rotations.
6. **Visualization layer:** Python plots and experiment reports.

## Technology Stack

- Verilog HDL
- Xilinx Vivado / XSim
- Python
- Qiskit
- Qiskit Aer
- NumPy
- Pandas
- Matplotlib

## Current Verification Results

| Test suite | Result |
|---|---:|
| RTL pulse-width sweep | 12/12 passed |
| RTL edge-case tests | 5/5 passed |
| Combined regression | Successful |

The timing sweep covers three delay settings and four pulse widths.
Edge-case tests cover reset, idle behavior, zero-length commands,
and reset during an active pulse.

## Project Structure

```text
qctrl-qsim/
├── rtl/
│   └── pulse_sequencer.v
├── testbench/
│   ├── tb_pulse_sequencer.v
│   └── tb_pulse_edge_cases.v
├── python/
│   ├── timing_bridge.py
│   ├── quantum_experiment.py
│   ├── analyze_results.py
│   ├── quantization_study.py
│   ├── plot_results.py
│   ├── rtl_validation.py
│   ├── rtl_quantum_bridge.py
│   ├── resolution_sweep.py
│   ├── analyze_rtl_sweep.py
│   └── regression_summary.py
├── experiments/
├── results/
│   └── figures/
└── docs/
```

## Setup

Install the Python dependencies:

```bash
python -m pip install qiskit qiskit-aer numpy matplotlib pandas
```

Run the Python analyses from the project root:

```bash
python python/timing_bridge.py
python python/quantum_experiment.py
python python/analyze_results.py
python python/quantization_study.py
python python/resolution_sweep.py
python python/plot_results.py
python python/rtl_validation.py
python python/rtl_quantum_bridge.py
python python/analyze_rtl_sweep.py
python python/regression_summary.py
```

RTL simulation requires a compatible Vivado installation. Add the RTL
module and the desired testbench as design and simulation sources, then
run behavioral simulation.

## Modeling Assumptions and Limitations

- The current RTL verification is simulation-based, not physical FPGA testing.
- The Python-to-quantum bridge is file-based.
- The pulse-duration-to-rotation mapping assumes a simplified linear
  relationship under constant drive amplitude.
- Qiskit Aer results are simulated, not measured from a physical qubit.
- The timing-resolution sweep uses hypothetical clock periods; it does not
  establish measured performance on different FPGA configurations.
- Passing testbenches establish only the behaviors covered by those tests.

## Future Work

- Automate RTL-to-Python data transfer.
- Expand regression tests and parameter sweeps.
- Compare quantization policies and timing-error metrics.
- Add controlled noise models and reproducible repeated trials.
- Validate the model assumptions and compare against relevant literature.
- Explore integration with more realistic quantum-control models.

## Research Scope

QCtrl-QSim is an exploratory engineering and simulation project.
Its current results establish a working prototype and preliminary
model-based observations; novelty and research contribution require
further literature review and experimental validation.
