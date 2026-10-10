
import csv
import math
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = PROJECT_ROOT / "results" / "timing_results.csv"
OUTPUT_CSV = PROJECT_ROOT / "results" / "statistical_evaluation.csv"

SHOT_COUNTS = [500, 1000, 2000, 4000, 8000]
SEEDS = [42, 123, 2026]
SIMULATOR = AerSimulator()


def simulate_probability(angle_rad, shots, seed):
    circuit = QuantumCircuit(1, 1)
    circuit.ry(angle_rad, 0)
    circuit.measure(0, 0)

    result = SIMULATOR.run(
        circuit,
        shots=shots,
        seed_simulator=seed,
    ).result()

    counts = result.get_counts()
    return counts.get("1", 0) / shots


def main():
    records = []

    with INPUT_CSV.open(newline="", encoding="utf-8") as file:
        timing_data = list(csv.DictReader(file))

    if not timing_data:
        raise ValueError(f"No timing data found in {INPUT_CSV}")

    for item in timing_data:
        cycles = int(item["pulse_cycles"])
        duration = float(item["duration_ns"])
        angle = float(item["rotation_angle_rad"])
        theoretical_p1 = math.sin(angle / 2) ** 2

        for shots in SHOT_COUNTS:
            probabilities = []

            for seed in SEEDS:
                measured_p1 = simulate_probability(angle, shots, seed)
                absolute_error = abs(measured_p1 - theoretical_p1)
                probabilities.append(measured_p1)

                records.append({
                    "pulse_cycles": cycles,
                    "duration_ns": duration,
                    "shots": shots,
                    "seed": seed,
                    "measured_p1": measured_p1,
                    "theoretical_p1": theoretical_p1,
                    "absolute_error": absolute_error,
                })

            mean_p1 = sum(probabilities) / len(probabilities)
            mean_abs_error = sum(
                abs(p - theoretical_p1) for p in probabilities
            ) / len(probabilities)

            print(
                f"{cycles} cycles | shots={shots:5d} | "
                f"mean P(1)={mean_p1:.4f} | "
                f"mean absolute error={mean_abs_error:.5f}"
            )

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "pulse_cycles",
                "duration_ns",
                "shots",
                "seed",
                "measured_p1",
                "theoretical_p1",
                "absolute_error",
            ],
        )
        writer.writeheader()
        writer.writerows(records)

    print(f"\nTotal simulation configurations: {len(records)}")
    print(f"Saved results to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
