
import csv
from pathlib import Path

# QCtrl-QSim: RTL timing to quantum-control model
# Initial model only; not a physical qubit calibration.

CLOCK_PERIOD_NS = 10.0
IDEAL_PULSE_CYCLES = 3


def calculate_timing(pulse_cycles, clock_period_ns=CLOCK_PERIOD_NS):
    """Calculate digital pulse duration from clock cycles."""
    if pulse_cycles <= 0:
        raise ValueError("pulse_cycles must be greater than zero")

    return pulse_cycles * clock_period_ns


def estimate_rotation_angle(
    actual_duration_ns,
    ideal_duration_ns,
    target_angle_rad
):
    """
    Simplified linear model:
    rotation angle is proportional to pulse duration,
    assuming constant drive amplitude.
    """
    if ideal_duration_ns <= 0:
        raise ValueError("ideal_duration_ns must be positive")

    return target_angle_rad * actual_duration_ns / ideal_duration_ns


def main():
    ideal_duration_ns = calculate_timing(IDEAL_PULSE_CYCLES)
    target_angle_rad = 1.5707963267948966  # pi/2 radians

    results = []

    print("QCtrl-QSim Timing Bridge")
    print("-" * 35)
    print(f"Clock period: {CLOCK_PERIOD_NS:.1f} ns")
    print(f"Ideal pulse cycles: {IDEAL_PULSE_CYCLES}")
    print(f"Ideal pulse duration: {ideal_duration_ns:.1f} ns")
    print()

    for cycles in range(1, 6):
        duration_ns = calculate_timing(cycles)
        angle_rad = estimate_rotation_angle(
            duration_ns,
            ideal_duration_ns,
            target_angle_rad
        )

        row = {
            "pulse_cycles": cycles,
            "duration_ns": duration_ns,
            "rotation_angle_rad": angle_rad,
            "angle_error_rad": angle_rad - target_angle_rad,
        }
        results.append(row)

        print(
            f"Cycles={cycles} | Duration={duration_ns:.1f} ns | "
            f"Angle={angle_rad:.4f} rad | "
            f"Error={row['angle_error_rad']:.4f} rad"
        )

    output_file = Path(__file__).resolve().parent.parent / "results" / "timing_results.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
