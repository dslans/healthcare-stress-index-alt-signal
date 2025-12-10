"""
Quick end-to-end run:
- load health data + prices
- build HSI
- backtest simple strategy on IHF
"""

import pandas as pd

from .config import DATA_PROCESSED
from .data_loading import load_or_fetch_sector_prices, compute_monthly_returns
from .features import build_feature_panel, build_hsi
from .backtest import backtest_long_flat, plot_cumulative_returns, performance_summary


def run_example() -> None:
    # Market data
    prices = load_or_fetch_sector_prices()
    sector_rets = compute_monthly_returns(prices)

    # Health features + HSI
    panel = build_feature_panel()
    hsi = build_hsi(panel)

    # Align HSI with returns
    data = hsi.join(sector_rets, how="inner").dropna()

    # Shift returns so HSI_t predicts returns_{t+1}
    shifted = data.copy()
    for col in sector_rets.columns:
        shifted[col] = shifted[col].shift(-1)
    shifted = shifted.dropna()

    # Example: trade IHF; if not available, fall back to XLV
    asset_col = "IHF" if "IHF" in shifted.columns else "XLV"
    bt = backtest_long_flat(signal=shifted["HSI"], returns=shifted[asset_col], quantile=0.7)

    # Plot and print stats
    plot_cumulative_returns(bt, f"HSI strategy vs {asset_col} buy & hold")
    summary = performance_summary(bt)
    print(summary)

    # Save processed panel for reuse
    panel_out = panel.join(hsi, how="left")
    panel_out.to_parquet(DATA_PROCESSED / "hsi_panel.parquet")
    print("Saved processed panel to", DATA_PROCESSED / "hsi_panel.parquet")


if __name__ == "__main__":
    run_example()
