from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Market data settings
SECTOR_TICKERS = ["XLV", "IHF", "IYH"]  # change as needed

START_DATE = "2010-01-01"
END_DATE = None  # use today's date
FREQ = "M"  # monthly frequency
