# src/ingest.py
import os
import requests
import pandas as pd
import yfinance as yf
import time
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

def load_api_data(ticker: str = "AAPL") -> pd.DataFrame:
    df = yf.download(
        ticker, period="5d", interval="1d",
        group_by="column", auto_adjust=False,
        progress=False, threads=False
    ).reset_index()

    if df.empty:  # tiny backoff + one retry
        time.sleep(1)
        df = yf.download(
            ticker, period="5d", interval="1d",
            group_by="column", auto_adjust=False,
            progress=False, threads=False
        ).reset_index()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.columns.name = None

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    for c in ("Adj Close", "Close", "Open", "High", "Low", "Volume"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df

def scrape_table(url: str, css: str = "table") -> pd.DataFrame:
    """
    Parse with BeautifulSoup, then build DataFrame from the first table matching css.
    """
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    node = soup.select_one(css)
    if node is None:
        raise ValueError(f"No table found for selector: {css}")
    df = pd.read_html(str(node))[0]
    return df

def validate_data(
    df: pd.DataFrame,
    required_cols: list[str] | None = None,
    need_numeric: bool = False,
    need_text: bool = False,
) -> bool:
    """
    Minimal validation:
      1) not empty
      2) required columns present
      3) optional checks for at least one numeric and one text column
    """
    if df is None or df.shape[0] == 0:
        raise ValueError("Empty dataframe")
    if required_cols:
        missing = [c for c in required_cols if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
    if need_numeric and df.select_dtypes(include="number").shape[1] == 0:
        raise ValueError("No numeric columns found")
    if need_text and df.select_dtypes(exclude="number").shape[1] == 0:
        raise ValueError("No text columns found")

    print("Shape:", df.shape)
    print("NA counts:\n", df.isna().sum())
    return True

def save_csv(df: pd.DataFrame, prefix: str, out_dir: str = "data/raw") -> str:
    """
    Save to data/raw with timestamped filename.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    path = out / f"{prefix}_{ts}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {path}")
    return str(path)