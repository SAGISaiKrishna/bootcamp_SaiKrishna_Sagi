# Stage 08 – Exploratory Data Analysis

## What this stage does
Generate a small synthetic dataset and run EDA so you can practice the flow. Replace the synthetic generator with your real dataset when ready.

## Files
- `notebooks/stage08_exploratory-data-analysis_homework.ipynb`
- `src/eda.py` helpers
- `figures/` auto-saved plots
- `reports/` saved CSV summaries

## Checklist covered
- First look: info, missing counts
- Numeric profile: describe, skew, kurtosis
- Distributions: at least 3 plots
- Relationships: at least 2 plots
- Correlation matrix
- Findings, so what, now what

## How to swap in your data
- Replace the synthetic generator cell with `pd.read_csv("path/to/your.csv")`
- Update which columns go into numeric profile and plots