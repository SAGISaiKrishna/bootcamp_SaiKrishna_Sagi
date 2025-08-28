# src/cleaning.py
import pandas as pd

def fill_missing_median(df: pd.DataFrame, cols=None) -> pd.DataFrame:
    """
    Why: Replace numeric NAs with column medians, which is robust to outliers.
    If cols is None we target all numeric columns.
    """
    out = df.copy()
    if cols is None:
        cols = out.select_dtypes(include="number").columns
    for c in cols:
        out[c] = out[c].fillna(out[c].median())
    return out

def drop_missing(df: pd.DataFrame, how: str = "any", thresh: int | None = None) -> pd.DataFrame:
    """
    Why: Remove rows with missing data according to a simple rule.
    - how='any' drops a row if any NA is present
    - how='all' drops a row only if all entries are NA
    - thresh keeps rows with at least 'thresh' non-NA values
    """
    if thresh is not None:
        return df.dropna(thresh=thresh)
    return df.dropna(how=how)

def normalize_data(df: pd.DataFrame, cols=None, method: str = "standard") -> pd.DataFrame:
    """
    Why: Put numeric features on comparable scales for downstream modeling.
    - 'standard': (x - mean) / std    (good default)
    - 'minmax'  : (x - min) / (max - min)
    """
    out = df.copy()
    if cols is None:
        cols = out.select_dtypes(include="number").columns
    if method == "standard":
        for c in cols:
            mu = out[c].mean()
            sd = out[c].std(ddof=0)
            out[c] = (out[c] - mu) / sd if sd not in (0, None, 0.0) else 0.0
    elif method == "minmax":
        for c in cols:
            mn, mx = out[c].min(), out[c].max()
            rng = mx - mn
            out[c] = (out[c] - mn) / rng if rng != 0 else 0.0
    else:
        raise ValueError("method must be 'standard' or 'minmax'")
    return out