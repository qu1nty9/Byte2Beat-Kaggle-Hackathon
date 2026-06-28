from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    log_loss,
    roc_auc_score,
)


def classification_metrics(
    y_true: np.ndarray | pd.Series,
    y_score: np.ndarray | pd.Series,
    dataset: str,
    model: str,
    split: str,
    threshold: float = 0.5,
) -> dict[str, float | int | str]:
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    clipped = np.clip(y_score, 1e-6, 1 - 1e-6)

    has_two_classes = len(np.unique(y_true)) == 2
    return {
        "dataset": dataset,
        "model": model,
        "split": split,
        "rows": int(len(y_true)),
        "positive_rate": float(y_true.mean()),
        "auroc": float(roc_auc_score(y_true, y_score)) if has_two_classes else np.nan,
        "auprc": float(average_precision_score(y_true, y_score)) if has_two_classes else np.nan,
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "brier": float(brier_score_loss(y_true, y_score)),
        "log_loss": float(log_loss(y_true, clipped, labels=[0, 1])),
        "sensitivity": float(tp / (tp + fn)) if tp + fn else np.nan,
        "specificity": float(tn / (tn + fp)) if tn + fp else np.nan,
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
    }


def calibration_table(
    y_true: np.ndarray | pd.Series,
    y_score: np.ndarray | pd.Series,
    dataset: str,
    model: str,
    n_bins: int = 10,
) -> pd.DataFrame:
    frame = pd.DataFrame({"y_true": np.asarray(y_true).astype(int), "y_score": np.asarray(y_score)})
    frame["bin"] = pd.qcut(frame["y_score"], q=n_bins, duplicates="drop")
    out = (
        frame.groupby("bin", observed=False)
        .agg(
            rows=("y_true", "size"),
            mean_predicted_risk=("y_score", "mean"),
            observed_rate=("y_true", "mean"),
            min_predicted_risk=("y_score", "min"),
            max_predicted_risk=("y_score", "max"),
        )
        .reset_index(drop=True)
    )
    out.insert(0, "model", model)
    out.insert(0, "dataset", dataset)
    out["abs_calibration_error"] = (out["observed_rate"] - out["mean_predicted_risk"]).abs()
    return out


def subgroup_metrics(
    df: pd.DataFrame,
    y_col: str,
    score_col: str,
    group_col: str,
    dataset: str,
    model: str,
) -> pd.DataFrame:
    rows = []
    for group_value, group_df in df.groupby(group_col, observed=False, dropna=False):
        if len(group_df) == 0:
            continue
        metric = classification_metrics(
            group_df[y_col].to_numpy(),
            group_df[score_col].to_numpy(),
            dataset=dataset,
            model=model,
            split=f"subgroup:{group_col}",
        )
        metric["group_col"] = group_col
        metric["group_value"] = str(group_value)
        rows.append(metric)
    return pd.DataFrame(rows)

