# Member 2 – Extract and Validate (Step 5)

## Your tasks
1. Understand and test `extract.py`:
   - `extract()` reads the CSV, prints the **number of records** and **number of columns**, saves a copy in `raw_data/` and returns the data.
   - `validate_data()` prints missing values, duplicate rows and negative rainfall counts.
2. Run it: `pip install pandas` then `python extract.py`
3. Take screenshots of the terminal output (records/columns, validation) and save them in a `screenshots/` folder here. Send them to Member 5.
4. Improve if you want (for example, also print column names and data types) – tell the team before changing anything other people depend on.

## Files in this folder
| File | Purpose |
|---|---|
| `extract.py` | Your code: `extract()` and `validate_data()` |
| `raw_data/rainfall_1.csv` | The raw data (source file) |

## Expected output
```
Number of records : 53162
Number of columns : 20
Raw copy saved to : raw_data/rainfall_raw_copy.csv
```

## Hand over to
Member 3 (they read the same raw file). Member 5 will paste your `extract()` into the final `pipeline.py`.

## Be ready to explain in viva
- How the data is read and why a raw copy is saved
- What the validation shows (8 columns with missing values, no duplicates, no negative rainfall)
