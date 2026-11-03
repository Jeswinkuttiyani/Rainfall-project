# Member 2 – Extract and Validate

**Project:** Kerala Rainfall ETL Mini Project  
**Module:** Step 5 – Extraction and Validation

## 1. Overview

This module extracts the raw Kerala rainfall dataset and performs basic data validation using Python and Pandas.

## 2. Objectives

- Read the rainfall CSV dataset.
- Display the number of records and columns.
- Save a copy of the raw dataset.
- Identify missing values.
- Check duplicate records.
- Identify negative rainfall values.

## 3. Project Structure

```text
Member_2_Extract_and_Validate/
│
├── raw_data/
│   ├── rainfall_1.csv
│   └── rainfall_raw_copy.csv
│
├── screenshots/
│   ├── extract.png
│   └── validate.png
│
├── extract.py
└── README.md
```

## 4. Technologies Used

- Python
- Pandas
- Pathlib

## 5. Functions

**extract()**
- Reads the CSV dataset.
- Displays the number of records and columns.
- Saves a copy in the `raw_data/` folder.
- Returns the extracted DataFrame.

**validate_data()**
- Identifies missing values.
- Counts duplicate records.
- Counts negative rainfall values.

## 6. Installation and Execution

Install Pandas:

```bash
pip install pandas
```

Run the program:

```bash
python extract.py
```

## 7. Expected Results

| Description | Expected Result |
|---|---:|
| Total records | 53,162 |
| Total columns | 20 |
| Columns with missing values | 8 |
| Duplicate records | 0 |
| Negative rainfall values | 0 |

*Results should be verified by executing the program.*

## 8. Screenshots

The `screenshots/` folder contains terminal outputs showing successful extraction and validation.

## 9. Handover

The extracted raw dataset is provided to Member 3 for the next stage of the ETL process. The `extract()` function is also shared with Member 5 for integration into the final pipeline.

## 10. Learning Outcomes

- Reading CSV files using Pandas.
- Working with DataFrames.
- Creating Python functions.
- Identifying missing values and duplicates.
- Performing basic data validation.

**Module:** Member 2 – Extraction and Validation
