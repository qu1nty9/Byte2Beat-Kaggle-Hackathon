from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "docs" / "drive-download-20260627T215828Z-3-001" / "Datasets"
OUT_PATH = ROOT / "outputs" / "tables" / "data_audit.json"


def as_builtin(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): as_builtin(v) for k, v in value.items()}
    if isinstance(value, list):
        return [as_builtin(v) for v in value]
    if isinstance(value, tuple):
        return [as_builtin(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


def profile_cardio_base() -> dict[str, Any]:
    path = DATA_ROOT / "Cardiac Failure" / "cardio_base.csv"
    df = pd.read_csv(path, sep=";")
    return {
        "path": str(path.relative_to(ROOT)),
        "shape": df.shape,
        "columns": list(df.columns),
        "target_counts": df["cardio"].value_counts(dropna=False).to_dict(),
        "age_years": {
            "min": df["age"].min() / 365.25,
            "median": df["age"].median() / 365.25,
            "max": df["age"].max() / 365.25,
        },
        "bp_anomalies": {
            "ap_hi_le_0": (df["ap_hi"] <= 0).sum(),
            "ap_lo_le_0": (df["ap_lo"] <= 0).sum(),
            "ap_hi_gt_250": (df["ap_hi"] > 250).sum(),
            "ap_lo_gt_200": (df["ap_lo"] > 200).sum(),
            "ap_lo_gt_ap_hi": (df["ap_lo"] > df["ap_hi"]).sum(),
        },
        "height_range": [df["height"].min(), df["height"].max()],
        "weight_range": [df["weight"].min(), df["weight"].max()],
        "missing_total": df.isna().sum().sum(),
    }


def profile_cardiac_processed() -> dict[str, Any]:
    path = DATA_ROOT / "Cardiac Failure" / "cardiac_failure_processed.csv"
    df = pd.read_csv(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "shape": df.shape,
        "columns": list(df.columns),
        "target_counts": df["cardio"].value_counts(dropna=False).to_dict(),
        "age_scaled": {
            "min": df["age"].min(),
            "median": df["age"].median(),
            "max": df["age"].max(),
        },
        "bp_anomalies": {
            "ap_hi_le_0": (df["ap_hi"] <= 0).sum(),
            "ap_lo_le_0": (df["ap_lo"] <= 0).sum(),
            "ap_hi_gt_250": (df["ap_hi"] > 250).sum(),
            "ap_lo_gt_200": (df["ap_lo"] > 200).sum(),
            "ap_lo_gt_ap_hi": (df["ap_lo"] > df["ap_hi"]).sum(),
        },
    }


def profile_heart() -> dict[str, Any]:
    path = DATA_ROOT / "Heart Attack" / "heart_processed.csv"
    df = pd.read_csv(path)
    return {
        "path": str(path.relative_to(ROOT)),
        "shape": df.shape,
        "columns": list(df.columns),
        "target_counts": df["HeartDisease"].value_counts(dropna=False).to_dict(),
        "zero_resting_bp": (df["RestingBP"] == 0).sum(),
        "zero_cholesterol": (df["Cholesterol"] == 0).sum(),
        "sex_m_counts": df["Sex_M"].value_counts(dropna=False).to_dict(),
        "missing_total": df.isna().sum().sum(),
    }


def profile_ecg_light() -> dict[str, Any]:
    path = DATA_ROOT / "ECG Timeseries" / "ecg_timeseries.csv"
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        first_rows = [next(reader) for _ in range(3)]

    sample_cols = {0, len(header) - 1}
    sample_cols.update(range(1, len(header), 1000))

    values: list[float] = []
    row_count = 0
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            row_count += 1
            for idx in sample_cols:
                if idx == 0 or idx >= len(row):
                    continue
                try:
                    values.append(float(row[idx]))
                except ValueError:
                    pass

    first_row_samples = []
    for row in first_rows:
        row_values = [float(x) for x in row[1:101] if x]
        first_row_samples.append(
            {
                "index_value": row[0],
                "first5": row[1:6],
                "sample100_min": min(row_values),
                "sample100_mean": sum(row_values) / len(row_values),
                "sample100_max": max(row_values),
            }
        )

    return {
        "path": str(path.relative_to(ROOT)),
        "file_size_mb": path.stat().st_size / (1024 * 1024),
        "header_len": len(header),
        "first_header": header[:8],
        "last_header": header[-8:],
        "row_count": row_count,
        "first_row_samples": first_row_samples,
        "sampled_numeric_values": len(values),
        "sampled_global_min": min(values),
        "sampled_global_mean": sum(values) / len(values),
        "sampled_global_max": max(values),
    }


def main() -> None:
    audit = {
        "cardio_base": profile_cardio_base(),
        "cardiac_failure_processed": profile_cardiac_processed(),
        "heart_processed": profile_heart(),
        "ecg_timeseries_light": profile_ecg_light(),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(as_builtin(audit), indent=2), encoding="utf-8")

    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")
    for name, payload in audit.items():
        print(f"{name}: shape={payload.get('shape', 'n/a')}")


if __name__ == "__main__":
    main()

