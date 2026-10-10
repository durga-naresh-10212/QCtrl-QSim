
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "results" / "resolution_sweep.csv"
OUTPUT = ROOT / "results" / "resolution_summary.csv"


def mean(values):
    return sum(values) / len(values)


def main():
    with INPUT.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        raise ValueError(f"No sweep data found in {INPUT}")

    periods = sorted({
        float(row["clock_period_ns"])
        for row in rows
    })

    summary = []

    print("Clock-Resolution Evaluation")
    print("-" * 65)

    for period in periods:
        subset = [
            row for row in rows
            if float(row["clock_period_ns"]) == period
        ]

        timing_errors = [
            abs(float(row["duration_error_ns"]))
            for row in subset
        ]

        probability_errors = [
            float(row["absolute_probability_error"])
            for row in subset
        ]

        result = {
            "clock_period_ns": period,
            "configurations": len(subset),
            "mean_absolute_timing_error_ns": mean(timing_errors),
            "max_absolute_timing_error_ns": max(timing_errors),
            "mean_absolute_probability_error": mean(probability_errors),
            "max_absolute_probability_error": max(probability_errors),
        }

        summary.append(result)

        print(
            f"Clock={period:5.1f} ns | "
            f"Mean timing error={result['mean_absolute_timing_error_ns']:.2f} ns | "
            f"Max timing error={result['max_absolute_timing_error_ns']:.2f} ns | "
            f"Mean probability error={result['mean_absolute_probability_error']:.5f} | "
            f"Max probability error={result['max_absolute_probability_error']:.5f}"
        )

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary[0].keys(),
        )
        writer.writeheader()
        writer.writerows(summary)

    print(f"\nConfigurations analyzed: {len(rows)}")
    print(f"Clock periods evaluated: {len(periods)}")
    print(f"Summary saved to: {OUTPUT}")


if __name__ == "__main__":
    main()

