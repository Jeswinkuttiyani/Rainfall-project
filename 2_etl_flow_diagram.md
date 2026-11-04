# ETL Flow Diagram (redraw this as an image)

```
Data Source  (rainfall_1.csv)
      │
      ▼
Extract            read CSV, show records and columns, save raw copy
      │
      ▼
Validate Data      missing values, duplicates, negative rainfall
      │
      ▼
Clean Data         rename, remove duplicates, drop columns, standardize text,
      │            fill missing, convert dates, change types, remove invalid rows
      ▼
Transform Data     date parts, season, rainfall category, station total + rank, sort
      │
      ▼
Generate Reports   summary, district, monthly, seasonal, top/bottom 10 ...
      │
      ▼
Load               save to reports/ and output/
```
