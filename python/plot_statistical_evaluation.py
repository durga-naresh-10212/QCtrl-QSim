
import csv
from pathlib import Path

import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = PROJECT_ROOT / "results" / "statistical_evaluation.csv"
OUTPUT_PNG = (
    PROJECT_ROOT
    / "results"
    / "figures"
    / "statistical_error_vs_shots.png"
)

def main():
    grouped = {}

    with INPUT_CSV.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            shots = int(row["shots"])
            error = float(row["absolute_error"])
            grouped.setdefault(shots, []).append(error)

    if not grouped:
        raise ValueError(f"No data found in {INPUT_CSV}")

    shot_counts = sorted(grouped)
    mean_errors = [
        sum(grouped[shots]) / len(grouped[shots])
        for shots in shot_counts
    ]

    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(shot_counts, mean_errors, marker="o")
    plt.xlabel("Shots per simulation")
    plt.ylabel("Mean absolute probability error")
    plt.title("Shot Count vs. Mean Absolute Probability Error")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=300)
    plt.close()

    print("Statistical Evaluation Plot")
    print("--------------------------")

    for shots, error in zip(shot_counts, mean_errors):
        print(f"{shots:5d} shots | Mean absolute error = {error:.6f}")

    print(f"\nPlot saved to: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
