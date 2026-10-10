
import csv
import math
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

ROOT = Path(__file__).resolve().parent.parent
RTL_FILE = ROOT / "results" / "rtl_timing_results.csv"
OUTPUT_FILE = ROOT / "results" / "rtl_quantum_results.csv"

CLOCK_PERIOD_NS = 10.0
REFERENCE_CYCLES = 3
TARGET_ANGLE = math.pi / 2
SHOTS = 4000

simulator = AerSimulator()


def simulate(angle):
    circuit = QuantumCircuit(1, 1)
    circuit.ry(angle, 0)
    circuit.measure(0, 0)

    result = simulator.run(circuit, shots=SHOTS).result()
    counts = result.get_counts()

    return counts.get("0", 0) / SHOTS, counts.get("1", 0) / SHOTS


def main():
    results = []

    with RTL_FILE.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            expected = int(row["expected_cycles"])
            measured = int(row["measured_cycles"])
            status = row["status"].strip().upper()

            if status != "PASS" or measured != expected:
                raise ValueError(f"RTL validation failed: {row}")

            duration_ns = measured * CLOCK_PERIOD_NS

            # Simplified constant-drive, linear-duration model.
            angle = TARGET_ANGLE * measured / REFERENCE_CYCLES
            p0, p1 = simulate(angle)

            results.append({
                "expected_cycles": expected,
                "measured_cycles": measured,
                "duration_ns": duration_ns,
                "rotation_angle_rad": angle,
                "measured_p0": p0,
                "measured_p1": p1,
                "theoretical_p1": math.sin(angle / 2) ** 2,
                "shots": SHOTS,
            })

            print(
                f"RTL={measured} cycles | "
                f"Duration={duration_ns:.1f} ns | "
                f"Angle={angle:.4f} rad | "
                f"P(1)={p1:.4f}"
            )

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nSaved integrated results to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
