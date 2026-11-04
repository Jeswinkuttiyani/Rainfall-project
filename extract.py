"""
Step 5 - extract() and validate_data()
Owner: Member 2
Kerala Rainfall ETL Mini Project
"""

import pandas as pd
import numpy as np

# --------------------------------------------------------------------------
# Paths and constants (pure string paths)
# --------------------------------------------------------------------------
SOURCE_FILE = "raw_data/rainfall_1.csv"
RAW_COPY = "raw_data/rainfall_raw_copy.csv"


# --------------------------------------------------------------------------
# EXTRACT (Step 5)
# --------------------------------------------------------------------------
def extract(source_file=SOURCE_FILE):
    """Read the raw CSV, display record & column counts, save a copy in raw_data/."""
    print("\n=== EXTRACT (Member 2) ===")
    try:
        df = pd.read_csv(source_file)
    except FileNotFoundError:
        df = pd.read_csv("rainfall_1.csv")

    print(f"Source file       : {source_file}")
    print(f"Number of records : {len(df)}")
    print(f"Number of columns : {df.shape[1]}")

    df.to_csv(RAW_COPY, index=False)
    print(f"Raw copy saved to : {RAW_COPY}")
    return df


def validate_data(df):
    """Quality check on the raw data (missing values, duplicates, negative values)."""
    print("\n--- Raw Data Validation ---")
    missing = df.isna().sum()
    print("Columns with missing values:")
    print(missing[missing > 0].to_string())
    print(f"Fully duplicated rows: {int(df.duplicated().sum())}")
    
    # Check negative rainfall using pandas/numpy
    rainfall_numeric = pd.to_numeric(df["Manual Daily Rainfall (mm)"], errors="coerce")
    neg_count = int(np.sum(rainfall_numeric < 0))
    print(f"Negative rainfall values: {neg_count}")


if __name__ == "__main__":
    raw_df = extract()
    validate_data(raw_df)
