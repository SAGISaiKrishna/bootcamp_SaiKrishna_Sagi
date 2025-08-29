# src/outliers.py
import numpy as np
import pandas as pd

def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Detect outliers using the IQR rule.
    Returns a boolean mask where True indicates an outlier.

    Parameters
    ----------
    series : pd.Series
        Numeric series to evaluate.
    k : float, default 1.5
        Multiplier on IQR for the lower and upper fences.

    Returns
    -------
    pd.Series
        Boolean mask aligned to the input index.
    """
    s = pd.to_numeric(series, errors="coerce")
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr
    return (s < lower) | (s > upper)

def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using a simple z score rule.
    Returns a boolean mask where True indicates an outlier.

    Parameters
    ----------
    series : pd.Series
        Numeric series to evaluate.
    threshold : float, default 3.0
        Absolute z score threshold.

    Returns
    -------
    pd.Series
        Boolean mask aligned to the input index.
    """
    s = pd.to_numeric(series, errors="coerce")
    mean = s.mean()
    std = s.std(ddof=0)  # population std for z score
    if std == 0 or np.isnan(std):
        return pd.Series(False, index=s.index)
    z = (s - mean).abs() / std
    return z > threshold

def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """
    Winsorize values by capping at chosen quantiles.
    Preserves row count and reduces leverage of extreme values.

    Parameters
    ----------
    series : pd.Series
        Numeric series to clip.
    lower : float, default 0.05
        Lower quantile.
    upper : float, default 0.95
        Upper quantile.

    Returns
    -------
    pd.Series
        Clipped numeric series aligned to input index.
    """
    s = pd.to_numeric(series, errors="coerce")
    lo = s.quantile(lower)
    hi = s.quantile(upper)
    return s.clip(lower=lo, upper=hi)