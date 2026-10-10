
import csv
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
INPUT = ROOT / "results" / "rtl_timing_sweep.csv"
OUTPUT = ROOT / "results" / "rtl_sweep_analysis.csv"

CLOCK_PERIOD_NS = 10.0

with INPUT.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

if not rows:
    raise ValueError("No RTL sweep rows found.")

results = []
for row in rows:
    delay = int(row["delay_cycles"])
    expected = int(row["expected_cycles"])
    measured = int(row["measured_cycles"])
    rtl_status = row["status"].strip().upper()

    passed = measured == expected and rtl_status == "PASS"

    results.append({
        "delay_cycles": delay,
        "expected_cycles": expected,
        "measured_cycles": measured,
        "expected_duration_ns": expected * CLOCK_PERIOD_NS,
        "measured_duration_ns": measured * CLOCK_PERIOD_NS,
        "timing_error_ns": (measured - expected) * CLOCK_PERIOD_NS,
        "rtl_status": rtl_status,
        "analysis_status": "PASS" if passed else "FAIL",
    })

with OUTPUT.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

passed = sum(r["analysis_status"] == "PASS" for r in results)
failed = len(results) - passed

print("QCtrl-QSim RTL Sweep Analysis")
print("-" * 36)
print(f"Total test cases: {len(results)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

print("\nResults by delay:")
for delay, count in sorted(Counter(
    r["delay_cycles"] for r in results
).items()):
    subset = [r for r in results if r["delay_cycles"] == delay]
    delay_passes = sum(
        r["analysis_status"] == "PASS" for r in subset
    )
    print(f"  Delay {delay}: {delay_passes}/{count} passed")

print(f"\nReport saved to: {OUTPUT}")

if failed or len(results) != 12:
    raise SystemExit("Validation failed: expected 12 passing tests.")

print("SUCCESS: all 12 RTL sweep results validated.")

