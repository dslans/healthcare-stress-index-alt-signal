# Healthcare Stress Index (HSI) Alt-Signal

This project builds a macro-style **Healthcare Stress Index (HSI)** from public health and insurance data and tests whether it predicts excess returns for:

- US health insurers
- US hospital / provider chains
- the broader healthcare sector

## Project Outline

1. Collect public healthcare data (utilization, employment, MLR ratios, etc.)
2. Engineer features and build a composite HSI time series
3. Align HSI with sector ETF returns (e.g., IHF, XLV, IYH)
4. Backtest simple long/short strategies conditioned on HSI

## Layout

- `data/raw/`: CSVs downloaded from public sources
- `data/processed/`: cleaned time-series panel files
- `src/hsi/`: reusable code for loading, transforming, HSI construction, and backtesting
- `notebooks/01_healthcare_stress_index_signal.ipynb`: main research notebook

## Quickstart

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Place raw CSVs in `data/raw/`:

- `health_utilization.csv`
- `insurer_mlr.csv`
- `health_employment.csv`
- optionally `prices_sector_etfs.csv` (or let `yfinance` fetch)

3. Run the example script:

```bash
python -m src.hsi.hsi_signal
```

4. Open the notebook (once created):

```bash
jupyter lab notebooks/01_healthcare_stress_index_signal.ipynb
```
