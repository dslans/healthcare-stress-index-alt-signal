from pathlib import Path
from typing import List, Optional

import pandas as pd
import yfinance as yf

from .config import DATA_RAW, START_DATE, END_DATE, FREQ, SECTOR_TICKERS


def load_or_fetch_sector_prices(
    tickers: Optional[List[str]] = None,
    start: str = START_DATE,
    end: Optional[str] = END_DATE,
    csv_path: Path = DATA_RAW / "prices_sector_etfs.csv",
) -> pd.DataFrame:
    """
    Returns a monthly DataFrame of adjusted close prices for given tickers.
    Index: Date, Columns: tickers.
    """
    if tickers is None:
        tickers = SECTOR_TICKERS

    if csv_path.exists():
        df = pd.read_csv(csv_path, parse_dates=["date"])
        df = df.set_index("date").sort_index()
        missing = set(tickers) - set(df.columns)
        if missing:
            raise ValueError(f"Missing tickers {missing} in {csv_path}")
        return df[tickers]

    data = yf.download(tickers, start=start, end=end, auto_adjust=True)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()

    # business days → monthly last
    data = data.asfreq("B").ffill()
    data = data.resample(FREQ).last()
    data.to_csv(csv_path, index_label="date")
    return data


def load_health_utilization(
    path: Path = DATA_RAW / "health_utilization.csv",
) -> pd.DataFrame:
    """
    Expected columns:
    - date (monthly)
    - ip_admissions_per_1000
    - op_visits_per_1000
    - ed_visits_per_1000
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date").sort_index()
    df = df.asfreq(FREQ).interpolate()
    return df


def load_insurer_mlr(
    path: Path = DATA_RAW / "insurer_mlr.csv",
) -> pd.DataFrame:
    """
    Expected columns:
    - date (monthly or quarterly)
    - mlr (medical loss ratio, 0-1 or 0-100)
    - claims_trend (optional)
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date").sort_index()
    df = df.asfreq(FREQ).interpolate()
    return df


def load_health_employment(
    path: Path = DATA_RAW / "health_employment.csv",
) -> pd.DataFrame:
    """
    Expected columns:
    - date (monthly)
    - healthcare_jobs
    - avg_hourly_earnings
    """
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.set_index("date").sort_index()
    df = df.asfreq(FREQ).interpolate()
    return df


def compute_monthly_returns(price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple percentage returns.
    """
    rets = price_df.pct_change().dropna()
    return rets
