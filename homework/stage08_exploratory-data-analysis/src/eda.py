# src/eda.py
from __future__ import annotations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Sequence

def structure_and_missing(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": df.isna().sum(),
        "missing_pct": (df.isna().mean() * 100).round(2)
    })

def numeric_profile(df: pd.DataFrame, cols: Optional[Sequence[str]] = None) -> pd.DataFrame:
    num = df if cols is None else df[cols]
    num = num.select_dtypes(include=[np.number])
    desc = num.describe().T
    desc["skew"] = num.skew(numeric_only=True)
    desc["kurtosis"] = num.kurtosis(numeric_only=True)
    return desc

def save_fig(fig, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)