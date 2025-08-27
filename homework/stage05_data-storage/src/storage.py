from pathlib import Path
import pandas as pd

def write_df(df: pd.DataFrame, path: Path) -> Path:
    """
    Save a DataFrame based on file extension (.csv or .parquet).
    Creates parent folders if missing. Raises a clear error if parquet engine is absent.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ext = path.suffix.lower()
    if ext == ".csv":
        df.to_csv(path, index=False)
    elif ext == ".parquet":
        try:
            df.to_parquet(path)  # requires pyarrow or fastparquet
        except Exception as e:
            raise RuntimeError("Parquet write requires a parquet engine (e.g., pip install pyarrow).") from e
    else:
        raise ValueError(f"Unsupported extension: {ext}")
    return path

def read_df(path: Path, parse_dates: list[str] | None = None) -> pd.DataFrame:
    """
    Load a DataFrame based on file extension (.csv or .parquet).
    For CSV, optional parse_dates ensures datetime columns round-trip correctly.
    """
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".csv":
        return pd.read_csv(path, parse_dates=parse_dates or [])
    elif ext == ".parquet":
        return pd.read_parquet(path)
    else:
        raise ValueError(f"Unsupported extension: {ext}")
