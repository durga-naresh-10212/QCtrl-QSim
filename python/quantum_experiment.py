import csv
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = PROJECT_ROOT / "results" / "timing_results.csv"
OUTPUT_CSV = PROJECT_ROOT / "results" / "quantum_results.csv"
SHOTS = 4000
RANDOM_SEED = 42
SIMULATOR = AerSimulator()
def run_experiment(angle_rad):
    circuit = QuantumCircuit(1, 1)
    circuit.ry(angle_rad, 0)
    circuit.measure(0, 0)
    result = SIMULATOR.run(
        circuit,
        shots=SHOTS,
        seed_simulator=RANDOM_SEED,
    ).result()
    counts = result.get_counts()
    p_one = counts.get("1", 0) / SHOTS
    p_zero = counts.get("0", 0) / SHOTS
    return p_zero, p_one
def main():
    rows = []
    with INPUT_CSV.open(newline="", encoding="utf-8") as file:
        timing_data = csv.DictReader(file)
        for item in timing_data:
            cycles = int(item["pulse_cycles"])
            duration = float(item["duration_ns"])
            angle = float(item["rotation_angle_rad"])

            p_zero, p_one = run_experiment(angle)

            rows.append({
                "pulse_cycles": cycles,
                "duration_ns": duration,
                "rotation_angle_rad": angle,
                "p_zero": p_zero,
                "p_one": p_one,
                "shots": SHOTS,
            })

            print(
                f"{cycles} cycles | {duration:.1f} ns | "
                f"angle={angle:.4f} rad | "
                f"P(0)={p_zero:.4f} | P(1)={p_one:.4f}"
            )
    if not rows:
        raise ValueError(f"No timing data found in {INPUT_CSV}")
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nRandom seed: {RANDOM_SEED}")
    print(f"Shots per experiment: {SHOTS}")
    print(f"Saved quantum results to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
