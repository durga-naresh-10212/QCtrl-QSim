
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "results" / "quantization_study.csv"

CLOCK_NS = 10.0
IDEAL_DURATION_NS = 30.0
TARGET_ANGLE = math.pi / 2

# Requested pulse durations, including values not representable
# exactly by a controller with a 10 ns clock period.
requested_durations = [15, 20, 25, 27, 29, 30, 31, 33, 35, 40, 45]

rows = []

for requested_ns in requested_durations:
    # Round to the nearest positive whole clock cycle.
    cycles = max(1, math.floor(requested_ns / CLOCK_NS + 0.5))
    actual_ns = cycles * CLOCK_NS

    requested_angle = TARGET_ANGLE * requested_ns / IDEAL_DURATION_NS
    actual_angle = TARGET_ANGLE * actual_ns / IDEAL_DURATION_NS

    requested_p1 = math.sin(requested_angle / 2) ** 2
    actual_p1 = math.sin(actual_angle / 2) ** 2

    rows.append({
        "requested_duration_ns": requested_ns,
        "clock_period_ns": CLOCK_NS,
        "selected_cycles": cycles,
        "actual_duration_ns": actual_ns,
        "duration_error_ns": actual_ns - requested_ns,
        "requested_angle_rad": requested_angle,
        "actual_angle_rad": actual_angle,
        "ideal_model_p1": requested_p1,
        "quantized_model_p1": actual_p1,
        "absolute_probability_difference": abs(actual_p1 - requested_p1),
    })

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Digital Timing Quantization Study")
print("-" * 76)

for row in rows:
    print(
        f"Requested={row['requested_duration_ns']:5.1f} ns | "
        f"Actual={row['actual_duration_ns']:5.1f} ns | "
        f"Timing error={row['duration_error_ns']:+5.1f} ns | "
        f"P(1) difference="
        f"{row['absolute_probability_difference']:.4f}"
    )

print(f"\nSaved results to: {OUTPUT}")
