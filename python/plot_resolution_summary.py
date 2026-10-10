
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "results" / "resolution_summary.csv"
OUTPUT = ROOT / "results" / "figures" / "resolution_summary.png"


def main():
    with INPUT.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"No data found in {INPUT}")

    clocks = [float(row["clock_period_ns"]) for row in rows]
    mean_timing = [
        float(row["mean_absolute_timing_error_ns"]) for row in rows
    ]
    mean_probability = [
        float(row["mean_absolute_probability_error"]) for row in rows
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.plot(clocks, mean_timing, marker="o")
    ax1.set_xlabel("Clock period (ns)")
    ax1.set_ylabel("Mean absolute timing error (ns)")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(clocks, mean_probability, marker="s")
    ax2.set_ylabel("Mean absolute probability error")

    plt.title("Clock Resolution vs. Timing and Probability Error")
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=300)
    plt.close(fig)

    print(f"Saved resolution summary plot to: {OUTPUT}")


if __name__ == "__main__":
    main()
