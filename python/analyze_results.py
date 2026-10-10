
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "results" / "quantum_results.csv"
OUTPUT_FILE = ROOT / "results" / "error_analysis.csv"

rows = []

with INPUT_FILE.open(newline="", encoding="utf-8") as file:
    for item in csv.DictReader(file):
        angle = float(item["rotation_angle_rad"])
        measured_p1 = float(item["p_one"])
        theoretical_p1 = math.sin(angle / 2) ** 2

        rows.append({
            "pulse_cycles": int(item["pulse_cycles"]),
            "duration_ns": float(item["duration_ns"]),
            "measured_p1": measured_p1,
            "theoretical_p1": theoretical_p1,
            "absolute_error": abs(measured_p1 - theoretical_p1),
        })

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

mae = sum(row["absolute_error"] for row in rows) / len(rows)

print("Quantum Simulation Error Analysis")
print("-" * 42)

for row in rows:
    print(
        f"{row['duration_ns']:5.1f} ns | "
        f"Measured={row['measured_p1']:.4f} | "
        f"Theory={row['theoretical_p1']:.4f} | "
        f"Absolute error={row['absolute_error']:.4f}"
    )

print(f"\nMean absolute probability error: {mae:.5f}")
print(f"Saved: {OUTPUT_FILE}")
