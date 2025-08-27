# Stage 05 – Data Storage

## Folder Structure
- `data/raw/` — stores immutable CSV snapshots.
- `data/processed/` — stores analysis-ready Parquet files.

## Why CSV and Parquet?
CSV is universal and human-readable, good for portability.  
Parquet is compressed, efficient, and preserves data types for fast analysis.  
Keeping both shows the tradeoff between universality and efficiency.

## Environment-Driven Paths
All save/load locations are configured in `.env`:

The notebook uses `python-dotenv` to load these values so no paths are hardcoded.

## Utilities
- `write_df(df, path)` saves to CSV or Parquet depending on extension.
- `read_df(path, parse_dates=[...])` reloads them correctly.  
Both ensure folders exist and handle missing parquet engines gracefully.

## Reload & Validation
After saving, both CSV and Parquet are reloaded.  
Validation checks confirm shapes match and columns keep expected dtypes (e.g., Date stays datetime, numeric fields stay numeric).  
Notebook prints: `Validation passed ✅`.

> Requires: **pandas**, **python-dotenv**, and **pyarrow** (for Parquet).