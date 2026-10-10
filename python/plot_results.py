
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT / "results" / "resolution_sweep.csv"
FIGURE_DIR = ROOT / "results" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

with INPUT_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

clock_periods = sorted({
    float(row["clock_period_ns"]) for row in rows
})

# Plot 1: mean probability error versus clock period.
mean_errors = []

for period in clock_periods:
    subset = [
        row for row in rows
        if float(row["clock_period_ns"]) == period
    ]
    mean_errors.append(
        sum(float(row["absolute_probability_error"]) for row in subset)
        / len(subset)
    )

plt.figure()
plt.plot(clock_periods, mean_errors, marker="o")
plt.xlabel("Clock period (ns)")
plt.ylabel("Mean absolute probability error")
plt.title("Timing Resolution vs Quantum Probability Error")
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "resolution_vs_probability_error.png", dpi=300)
plt.close()

# Plot 2: requested versus actual duration for each clock period.
plt.figure()

for period in clock_periods:
    subset = [
        row for row in rows
        if float(row["clock_period_ns"]) == period
    ]
    requested = [
        float(row["requested_duration_ns"]) for row in subset
    ]
    actual = [
        float(row["actual_duration_ns"]) for row in subset
    ]
    plt.plot(requested, actual, marker="o", label=f"{period:g} ns clock")

plt.xlabel("Requested duration (ns)")
plt.ylabel("Quantized duration (ns)")
plt.title("Requested vs Quantized Pulse Duration")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_DIR / "requested_vs_quantized_duration.png", dpi=300)
plt.close()

print("Plots generated successfully:")
print(FIGURE_DIR / "resolution_vs_probability_error.png")
print(FIGURE_DIR / "requested_vs_quantized_duration.png")
