
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "results" / "resolution_sweep.csv"

TARGET_DURATION_NS = 30.0
TARGET_ANGLE = math.pi / 2

# Explore several hypothetical controller clock periods.
CLOCK_PERIODS_NS = [2.0, 5.0, 10.0, 15.0, 20.0]

# Include requests near and between representable durations.
REQUESTED_DURATIONS_NS = [
    21.0, 24.0, 26.0, 27.0, 29.0,
    30.0, 31.0, 33.0, 34.0, 39.0
]


def probability_one(angle):
    return math.sin(angle / 2) ** 2


def main():
    rows = []

    for clock_ns in CLOCK_PERIODS_NS:
        for requested_ns in REQUESTED_DURATIONS_NS:
            cycles = max(
                1,
                math.floor(requested_ns / clock_ns + 0.5)
            )
            actual_ns = cycles * clock_ns

            requested_angle = (
                TARGET_ANGLE * requested_ns / TARGET_DURATION_NS
            )
            actual_angle = (
                TARGET_ANGLE * actual_ns / TARGET_DURATION_NS
            )

            rows.append({
                "clock_period_ns": clock_ns,
                "requested_duration_ns": requested_ns,
                "selected_cycles": cycles,
                "actual_duration_ns": actual_ns,
                "duration_error_ns": actual_ns - requested_ns,
                "angle_error_rad": actual_angle - requested_angle,
                "ideal_probability": probability_one(requested_angle),
                "modeled_probability": probability_one(actual_angle),
                "absolute_probability_error": abs(
                    probability_one(actual_angle)
                    - probability_one(requested_angle)
                ),
            })

    with OUTPUT.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("Timing Resolution Sweep")
    print("-" * 40)

    for clock_ns in CLOCK_PERIODS_NS:
        subset = [r for r in rows if r["clock_period_ns"] == clock_ns]
        mean_error = sum(
            r["absolute_probability_error"] for r in subset
        ) / len(subset)

        max_timing_error = max(
            abs(r["duration_error_ns"]) for r in subset
        )

        print(
            f"Clock={clock_ns:5.1f} ns | "
            f"Max timing error={max_timing_error:5.1f} ns | "
            f"Mean probability error={mean_error:.5f}"
        )

    print(f"\nSaved: {OUTPUT}")


if __name__ == "__main__":
    main()
