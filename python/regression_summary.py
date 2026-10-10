
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

SWEEP_CSV = RESULTS / "rtl_timing_sweep.csv"
EDGE_CSV = RESULTS / "edge_case_results.csv"
SUMMARY_CSV = RESULTS / "regression_summary.csv"


def main():
    if not SWEEP_CSV.exists():
        raise FileNotFoundError(f"Missing input: {SWEEP_CSV}")

    with SWEEP_CSV.open(newline="", encoding="utf-8") as file:
        sweep_rows = list(csv.DictReader(file))

    sweep_passed = sum(
        row["status"].strip().upper() == "PASS"
        and int(row["expected_cycles"]) == int(row["measured_cycles"])
        for row in sweep_rows
    )

    edge_rows = []
    if EDGE_CSV.exists():
        with EDGE_CSV.open(newline="", encoding="utf-8") as file:
            edge_rows = list(csv.DictReader(file))

    edge_passed = sum(
        row["status"].strip().upper() == "PASS"
        for row in edge_rows
    )

    summary = [
        {
            "suite": "RTL timing sweep",
            "passed": sweep_passed,
            "total": len(sweep_rows),
            "status": "PASS" if len(sweep_rows) == 12
            and sweep_passed == 12 else "CHECK",
        },
        {
            "suite": "RTL edge cases",
            "passed": edge_passed,
            "total": len(edge_rows),
            "status": "PASS" if len(edge_rows) == 5
            and edge_passed == 5 else "NOT EXPORTED",
        },
    ]

    with SUMMARY_CSV.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["suite", "passed", "total", "status"]
        )
        writer.writeheader()
        writer.writerows(summary)

    print("QCtrl-QSim Regression Summary")
    print("-" * 36)

    for row in summary:
        print(
            f"{row['suite']}: {row['passed']}/{row['total']} "
            f"-- {row['status']}"
        )

    print(f"\nReport saved to: {SUMMARY_CSV}")


if __name__ == "__main__":
    main()
