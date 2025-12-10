from typing import Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def backtest_long_flat(
    signal: pd.Series,
    returns: pd.Series,
    quantile: float = 0.7,
) -> pd.DataFrame:
    """
    If signal is above given quantile, go long (1); else flat (0).
    Assumes signal_t predicts returns_{t+1}, i.e., returns should
    already be shifted if needed.
    """
    aligned = pd.concat([signal, returns], axis=1, join="inner").dropna()
    sig = aligned.iloc[:, 0]
    rets = aligned.iloc[:, 1]

    thresh = sig.quantile(quantile)
    position = (sig > thresh).astype(int)
    strat_rets = position * rets

    out = pd.DataFrame(
        {
            "signal": sig,
            "position": position,
            "asset_ret": rets,
            "strat_ret": strat_rets,
        }
    )
    return out


def plot_cumulative_returns(bt_df: pd.DataFrame, title: str) -> None:
    cum_strat = (1 + bt_df["strat_ret"]).cumprod()
    cum_asset = (1 + bt_df["asset_ret"]).cumprod()

    plt.figure(figsize=(10, 5))
    plt.plot(cum_strat.index, cum_strat, label="Strategy")
    plt.plot(cum_asset.index, cum_asset, label="Buy & Hold")
    plt.title(title)
    plt.ylabel("Cumulative Growth of $1")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def performance_summary(
    bt_df: pd.DataFrame, freq_per_year: int = 12
) -> pd.Series:
    """
    Simple annualized return/vol/sharpe summary for strategy vs asset.
    """
    strat = bt_df["strat_ret"]
    asset = bt_df["asset_ret"]

    def annualized(ret: pd.Series) -> float:
        mean = ret.mean()
        return (1 + mean) ** freq_per_year - 1

    def vol(ret: pd.Series) -> float:
        return ret.std() * np.sqrt(freq_per_year)

    ann_strat = annualized(strat)
    ann_asset = annualized(asset)
    vol_strat = vol(strat)
    vol_asset = vol(asset)

    sharpe_strat = ann_strat / vol_strat if vol_strat != 0 else np.nan
    sharpe_asset = ann_asset / vol_asset if vol_asset != 0 else np.nan

    return pd.Series(
        {
            "ann_return_strat": ann_strat,
            "ann_return_asset": ann_asset,
            "ann_vol_strat": vol_strat,
            "ann_vol_asset": vol_asset,
            "sharpe_strat": sharpe_strat,
            "sharpe_asset": sharpe_asset,
            "n_periods": len(bt_df),
        }
    )
