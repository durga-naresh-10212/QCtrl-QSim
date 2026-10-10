
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INPUT_CSV = ROOT / "results" / "rtl_timing_results.csv"
OUTPUT_CSV = ROOT / "results" / "rtl_validation.csv"

CLOCK_PERIOD_NS = 10.0


def main():
    validated_rows = []

    with INPUT_CSV.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            expected = int(row["expected_cycles"])
            measured = int(row["measured_cycles"])
            status = row["status"].strip().upper()

            width_pass = measured == expected and status == "PASS"

            validated_rows.append({
                "expected_cycles": expected,
                "measured_cycles": measured,
                "expected_duration_ns": expected * CLOCK_PERIOD_NS,
                "measured_duration_ns": measured * CLOCK_PERIOD_NS,
                "timing_error_ns": (measured - expected) * CLOCK_PERIOD_NS,
                "rtl_status": status,
                "validation": "PASS" if width_pass else "FAIL",
            })

    if not validated_rows:
        raise ValueError("The RTL timing CSV contains no test results.")

    fields = list(validated_rows[0].keys())

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(validated_rows)

    print("QCtrl-QSim RTL Validation")
    print("-" * 48)

    for row in validated_rows:
        print(
            f"Expected={row['expected_cycles']} cycles | "
            f"Measured={row['measured_cycles']} cycles | "
            f"Duration={row['measured_duration_ns']:.1f} ns | "
            f"{row['validation']}"
        )

    passed = sum(r["validation"] == "PASS" for r in validated_rows)
    failed = len(validated_rows) - passed

    print(f"\nTests passed: {passed}/{len(validated_rows)}")
    print(f"Tests failed: {failed}")
    print(f"Report saved to: {OUTPUT_CSV}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
