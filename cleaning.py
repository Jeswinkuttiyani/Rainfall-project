"""
Step 6 (part 1) - Cleaning Transformations T1-T8b
Owner: Member 3
Kerala Rainfall ETL Mini Project
"""

import pandas as pd
import numpy as np

# --------------------------------------------------------------------------
# Paths and constants (pure string paths)
# --------------------------------------------------------------------------
SOURCE_FILE = "raw_data/rainfall_1.csv"
OUTPUT_CLEANED = "output/cleaned_stage1.csv"
OUTPUT_LOG = "output/cleaning_log.csv"

# Standardized column name mapping
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

# Kerala geographical bounds
KERALA_LAT = (8.0, 13.0)
KERALA_LON = (74.5, 77.5)


def _log(log, step, reason, before, after):
    """Record what each transformation did and why it was necessary."""
    log.append({"step": step, "reason": reason, "rows_before": before, "rows_after": after})
    print(f"  [{step}] rows: {before} -> {after}")


# --------------------------------------------------------------------------
# TRANSFORM - Cleaning (Step 6, Part 1)
# --------------------------------------------------------------------------
def t1_rename_columns(df, log):
    """Convert column headers to snake_case for easy coding."""
    before = len(df)
    df = df.rename(columns=COLUMN_MAP)
    _log(log, "T1 Rename columns", "Convert to short snake_case names so they are easy to use in code", before, len(df))
    return df


def t2_remove_duplicates(df, log):
    """Remove exact duplicate rows to avoid double-counting rainfall."""
    before = len(df)
    subset_cols = [c for c in df.columns if c != "sl_no"]
    df = df.drop_duplicates(subset=subset_cols)
    _log(log, "T2 Remove duplicate rows", "Exact duplicates would double-count rainfall", before, len(df))
    return df


def t3_drop_unwanted_columns(df, log, threshold=0.9):
    """Drop arbitrary row index (sl_no) and columns with >90% missing values."""
    before = len(df)
    sparse_cols = [c for c in df.columns if df[c].isna().mean() > threshold]
    df = df.drop(columns=["sl_no"] + sparse_cols)
    _log(log, "T3 Remove unwanted columns",
         f"Dropped row-id and columns >{int(threshold * 100)}% empty: {', '.join(sparse_cols)}", before, len(df))
    return df


def t4_standardize_text(df, log):
    """Strip whitespace and convert to Title Case for uniform grouping."""
    before = len(df)
    text_cols = ["station", "district", "tehsil", "river", "basin", "tributary", "local_river"]
    for col in text_cols:
        if col in df.columns:
            df[col] = (df[col].astype("string").str.strip()
                       .str.replace(r"\s+", " ", regex=True).str.title())
    _log(log, "T4 Standardize text", "Trim spaces and Title Case so the same name is never counted as two values", before, len(df))
    return df


def t5_handle_missing_values(df, log):
    """Fill missing river and basin details with 'Unknown'."""
    before = len(df)
    for col in ["river", "basin", "tributary", "local_river"]:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
    _log(log, "T5 Handle missing values", "Fill missing river/basin details with 'Unknown' so no rows are lost", before, len(df))
    return df


def t6_convert_dates(df, log):
    """Parse text timestamps 'DDMMYYYY  hh:mm:ss AM' to datetime."""
    before = len(df)
    cleaned = df["acquisition_time"].astype(str).str.split().str.join(" ")
    df["date_time"] = pd.to_datetime(cleaned, format="%d%m%Y %I:%M:%S %p", errors="coerce")
    df["date"] = df["date_time"].dt.normalize()
    df = df.drop(columns=["acquisition_time"])
    _log(log, "T6 Convert date format", "Text timestamps cannot be sorted or grouped by month; parsed to datetime", before, len(df))
    return df


def t7_change_data_types(df, log):
    """Cast numeric codes to integer and coordinates/rainfall to float."""
    before = len(df)
    df["state_lgd_code"] = df["state_lgd_code"].astype("int32")
    df["district_lgd_code"] = df["district_lgd_code"].astype("int32")
    df["latitude"] = df["latitude"].astype("float64")
    df["longitude"] = df["longitude"].astype("float64")
    df["rainfall_mm"] = pd.to_numeric(df["rainfall_mm"], errors="coerce")
    _log(log, "T7 Change data types", "Codes as integers, coordinates and rainfall as floats", before, len(df))
    return df


def t8_remove_invalid_values(df, log):
    """Filter records within Kerala coordinates and non-negative rainfall."""
    before = len(df)
    valid = (
        df["date"].notna()
        & df["rainfall_mm"].notna()
        & (df["rainfall_mm"] >= 0)
        & (df["latitude"] >= KERALA_LAT[0]) & (df["latitude"] <= KERALA_LAT[1])
        & (df["longitude"] >= KERALA_LON[0]) & (df["longitude"] <= KERALA_LON[1])
    )
    df = df[valid]
    _log(log, "T8 Remove invalid values",
         "Dropped rows with unparseable dates, missing/negative rainfall or coordinates outside Kerala", before, len(df))
    return df


def t8b_remove_duplicate_readings(df, log):
    """Enforce one reading per station per date."""
    before = len(df)
    df = df.drop_duplicates(subset=["station", "date"], keep="first")
    _log(log, "T8b Remove duplicate station-days", "One reading per station per day; keeps the first", before, len(df))
    return df


def run_cleaning():
    """Execute all cleaning steps and save output for Member 4."""
    try:
        df = pd.read_csv(SOURCE_FILE)
    except FileNotFoundError:
        df = pd.read_csv("rainfall_1.csv")

    log = []
    print("\n--- Cleaning Transformations (Member 3) ---")
    steps = (
        t1_rename_columns,
        t2_remove_duplicates,
        t3_drop_unwanted_columns,
        t4_standardize_text,
        t5_handle_missing_values,
        t6_convert_dates,
        t7_change_data_types,
        t8_remove_invalid_values,
        t8b_remove_duplicate_readings,
    )
    for step in steps:
        df = step(df, log)

    df.to_csv(OUTPUT_CLEANED, index=False)
    pd.DataFrame(log).to_csv(OUTPUT_LOG, index=False)
    print(f"\n[OK] Saved: {OUTPUT_CLEANED} (Hand this file to Member 4)")
    print(f"[OK] Saved: {OUTPUT_LOG}")
    return df


if __name__ == "__main__":
    run_cleaning()
