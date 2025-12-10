"""
Placeholder script to show where you'd transform raw public data into the
expected CSV schemas used by src/hsi/data_loading.py.

For now, this just documents the expected schemas.
"""

EXPECTED_FILES = {
    "health_utilization.csv": [
        "date",
        "ip_admissions_per_1000",
        "op_visits_per_1000",
        "ed_visits_per_1000",
    ],
    "insurer_mlr.csv": [
        "date",
        "mlr",
        "claims_trend",
    ],
    "health_employment.csv": [
        "date",
        "healthcare_jobs",
        "avg_hourly_earnings",
    ],
}


def main() -> None:
    print("This is a stub. Expected files and columns:")
    for fname, cols in EXPECTED_FILES.items():
        print(f"- {fname}: {', '.join(cols)}")


if __name__ == "__main__":
    main()
