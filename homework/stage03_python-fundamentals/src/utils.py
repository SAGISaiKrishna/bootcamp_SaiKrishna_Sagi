import pandas as pd

def get_summary_stats(df: pd.DataFrame, group_col: str = None):
    summary = df.describe(include="all")

    grouped = None
    if group_col and group_col in df.columns:
        # Only aggregate numeric columns to avoid errors
        numeric_cols = df.select_dtypes(include="number").columns
        if len(numeric_cols) > 0:
            grouped = df.groupby(group_col)[numeric_cols].mean()

    return summary, grouped
