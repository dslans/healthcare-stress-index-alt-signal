from typing import List

import numpy as np
import pandas as pd
from scipy.stats import zscore

from .config import START_DATE
from .data_loading import (
    load_health_utilization,
    load_insurer_mlr,
    load_health_employment,
)


def build_feature_panel() -> pd.DataFrame:
    """
    Build a monthly feature panel of health utilization, insurer margin,
    and employment series.
    """
    util = load_health_utilization()
    mlr = load_insurer_mlr()
    emp = load_health_employment()

    util = util.add_prefix("util_")
    mlr = mlr.add_prefix("mlr_")
    emp = emp.add_prefix("emp_")

    panel = util.join(mlr, how="outer").join(emp, how="outer")
    panel = panel.sort_index()
    panel = panel.loc[START_DATE:]

    panel = panel.interpolate().ffill().bfill()
    return panel


def build_hsi(panel: pd.DataFrame) -> pd.DataFrame:
    """
    Build a composite Healthcare Stress Index (HSI) from the feature panel.
    Returns df with column 'HSI'.
    """
    df = panel.copy()

    # Features where higher value = more "stress"
    stress_up_features: List[str] = [
        "util_ip_admissions_per_1000",
        "util_ed_visits_per_1000",
        "mlr_mlr",
    ]

    # Features where higher value = less stress (we invert)
    stress_down_features: List[str] = [
        "emp_healthcare_jobs",
    ]

    for f in stress_up_features + stress_down_features:
        if f not in df.columns:
            raise KeyError(f"Expected feature {f} not found in feature panel.")

    # Z-score
    for col in stress_up_features:
        df[col + "_z"] = zscore(df[col].astype(float), nan_policy="omit")

    for col in stress_down_features:
        df[col + "_z"] = -zscore(df[col].astype(float), nan_policy="omit")

    z_cols = [c for c in df.columns if c.endswith("_z")]
    df["HSI"] = df[z_cols].mean(axis=1)

    return df[["HSI"]]
