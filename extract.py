"""
Step 5 - extract() and validate_data()
Owner: Member 2
Standalone part of the Kerala Rainfall ETL mini project.
"""

from pathlib import Path
import shutil

import pandas as pd

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw_data"
REPORTS_DIR = BASE_DIR / "reports"
OUTPUT_DIR = BASE_DIR / "output"

SOURCE_FILE = RAW_DIR / "rainfall_1.csv"
RAW_COPY = RAW_DIR / "rainfall_raw_copy.csv"

COLUMN_MAP = {
    "SlNo": "sl_no",
    "Station": "station",
    "Agency": "agency",
    "State LGD Code": "state_lgd_code",
    "State": "state",
    "District LGD Code": "district_lgd_code",
    "District": "district",
    "Tehsil": "tehsil",
    "Block": "block",
    "Village": "village",
    "River": "river",
    "Basin": "basin",
    "Tributary": "tributary",
    "Subtributary": "subtributary",
    "SubSubtributary": "sub_subtributary",
    "Local River": "local_river",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "Data Acquisition Time": "acquisition_time",
    "Manual Daily Rainfall (mm)": "rainfall_mm",
}

# Rough bounding box of Kerala, used to catch wrong coordinates
KERALA_LAT = (8.0, 13.0)
KERALA_LON = (74.5, 77.5)

# IMD (India Meteorological Department) daily rainfall classes, in mm
RAIN_BINS = [0, 2.5, 15.6, 64.5, 115.6, 204.5, float("inf")]
RAIN_LABELS = ["Very Light", "Light", "Moderate", "Heavy", "Very Heavy", "Extremely Heavy"]

SEASONS = {
    1: "Winter", 2: "Winter",
    3: "Pre-Monsoon", 4: "Pre-Monsoon", 5: "Pre-Monsoon",
    6: "Southwest Monsoon", 7: "Southwest Monsoon",
    8: "Southwest Monsoon", 9: "Southwest Monsoon",
    10: "Post-Monsoon", 11: "Post-Monsoon", 12: "Post-Monsoon",
}


def _log(log, step, reason, before, after):
    """Record what a transformation did, and why it was needed."""
    log.append({"step": step, "reason": reason, "rows_before": before, "rows_after": after})
    print(f"  [{step}] rows: {before} -> {after}")


# --------------------------------------------------------------------------
# EXTRACT  (Member 2)
# --------------------------------------------------------------------------
def extract(source_file=SOURCE_FILE):
    """Read the raw CSV, show its size and save a copy in raw_data/."""
    print("\n=== EXTRACT ===")
    source_file = Path(source_file)
    if not source_file.exists():
        raise FileNotFoundError(f"Source file not found: {source_file}")

    df = pd.read_csv(source_file)
    print(f"Source            : {source_file.name}")
    print(f"Number of records : {len(df)}")
    print(f"Number of columns : {df.shape[1]}")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(RAW_COPY, index=False)
    print(f"Raw copy saved to : {RAW_COPY.relative_to(BASE_DIR)}")
    return df


def validate_data(df):
    """Quick quality check on the raw data (prints a short profile)."""
    print("\n--- Raw data validation ---")
    missing = df.isna().sum()
    print("Columns with missing values:")
    print(missing[missing > 0].to_string())
    print(f"Fully duplicated rows: {df.duplicated().sum()}")
    print(f"Negative rainfall values: {(df['Manual Daily Rainfall (mm)'] < 0).sum()}")



if __name__ == "__main__":
    data = extract()
    validate_data(data)
