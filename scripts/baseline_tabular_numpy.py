from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "docs" / "drive-download-20260627T215828Z-3-001" / "Datasets"
OUT_TABLES = ROOT / "outputs" / "tables"
SEED = 42


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.clip(z, -40, 40)
    return 1.0 / (1.0 + np.exp(-z))


def stratified_split(
    y: np.ndarray,
    train_frac: float = 0.70,
    valid_frac: float = 0.15,
    seed: int = SEED,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train_parts: list[np.ndarray] = []
    valid_parts: list[np.ndarray] = []
    test_parts: list[np.ndarray] = []

    for cls in np.unique(y):
        idx = np.flatnonzero(y == cls)
        rng.shuffle(idx)
        n_train = int(len(idx) * train_frac)
        n_valid = int(len(idx) * valid_frac)
        train_parts.append(idx[:n_train])
        valid_parts.append(idx[n_train : n_train + n_valid])
        test_parts.append(idx[n_train + n_valid :])

    train_idx = np.concatenate(train_parts)
    valid_idx = np.concatenate(valid_parts)
    test_idx = np.concatenate(test_parts)
    rng.shuffle(train_idx)
    rng.shuffle(valid_idx)
    rng.shuffle(test_idx)
    return train_idx, valid_idx, test_idx


def standardize(
    train_x: np.ndarray,
    valid_x: np.ndarray,
    test_x: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    mean = train_x.mean(axis=0)
    std = train_x.std(axis=0)
    std[std == 0] = 1.0
    return (train_x - mean) / std, (valid_x - mean) / std, (test_x - mean) / std, mean, std


def fit_logistic_regression(
    x: np.ndarray,
    y: np.ndarray,
    lr: float = 0.10,
    l2: float = 0.01,
    n_iter: int = 900,
) -> np.ndarray:
    xb = np.column_stack([np.ones(len(x)), x])
    w = np.zeros(xb.shape[1])
    for _ in range(n_iter):
        p = sigmoid(xb @ w)
        grad = xb.T @ (p - y) / len(y)
        grad[1:] += l2 * w[1:]
        w -= lr * grad
    return w


def predict_proba(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    xb = np.column_stack([np.ones(len(x)), x])
    return sigmoid(xb @ w)


def auroc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    y_true = y_true.astype(int)
    n_pos = int(y_true.sum())
    n_neg = int(len(y_true) - n_pos)
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    order = np.argsort(y_score)
    ranks = np.empty(len(y_score), dtype=float)
    ranks[order] = np.arange(1, len(y_score) + 1)
    rank_sum_pos = ranks[y_true == 1].sum()
    return float((rank_sum_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def metrics(dataset: str, split: str, y_true: np.ndarray, y_score: np.ndarray) -> dict[str, float | int | str]:
    y_pred = (y_score >= 0.5).astype(int)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    clipped = np.clip(y_score, 1e-6, 1 - 1e-6)
    return {
        "dataset": dataset,
        "split": split,
        "rows": int(len(y_true)),
        "positive_rate": float(y_true.mean()),
        "auroc": auroc(y_true, y_score),
        "accuracy": float((y_pred == y_true).mean()),
        "brier": float(np.mean((y_score - y_true) ** 2)),
        "log_loss": float(-np.mean(y_true * np.log(clipped) + (1 - y_true) * np.log(1 - clipped))),
        "sensitivity": float(tp / (tp + fn)) if tp + fn else float("nan"),
        "specificity": float(tn / (tn + fp)) if tn + fp else float("nan"),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def run_dataset(
    dataset_name: str,
    df: pd.DataFrame,
    feature_cols: Iterable[str],
    target_col: str,
    n_iter: int,
) -> tuple[list[dict[str, float | int | str]], pd.DataFrame]:
    feature_cols = list(feature_cols)
    x = df[feature_cols].astype(float).to_numpy()
    y = df[target_col].astype(int).to_numpy()

    train_idx, valid_idx, test_idx = stratified_split(y)
    train_x, valid_x, test_x, mean, std = standardize(x[train_idx], x[valid_idx], x[test_idx])
    train_y, valid_y, test_y = y[train_idx], y[valid_idx], y[test_idx]

    w = fit_logistic_regression(train_x, train_y, n_iter=n_iter)

    result_rows = [
        metrics(dataset_name, "train", train_y, predict_proba(train_x, w)),
        metrics(dataset_name, "valid", valid_y, predict_proba(valid_x, w)),
        metrics(dataset_name, "test", test_y, predict_proba(test_x, w)),
    ]

    coef = pd.DataFrame(
        {
            "feature": feature_cols,
            "standardized_coefficient": w[1:],
            "train_mean": mean,
            "train_std": std,
            "abs_standardized_coefficient": np.abs(w[1:]),
        }
    ).sort_values("abs_standardized_coefficient", ascending=False)

    return result_rows, coef


def load_clean_cardio() -> tuple[pd.DataFrame, list[str], str]:
    path = DATA_ROOT / "Cardiac Failure" / "cardio_base.csv"
    df = pd.read_csv(path, sep=";")
    df = df.assign(
        age_years=df["age"] / 365.25,
        bmi=df["weight"] / (df["height"] / 100) ** 2,
    )
    plausible = (
        df["height"].between(120, 220)
        & df["weight"].between(30, 250)
        & df["bmi"].between(10, 80)
        & df["ap_hi"].between(80, 250)
        & df["ap_lo"].between(40, 150)
        & (df["ap_lo"] <= df["ap_hi"])
    )
    df = df.loc[plausible].copy()
    features = [
        "age_years",
        "gender",
        "height",
        "weight",
        "bmi",
        "ap_hi",
        "ap_lo",
        "cholesterol",
        "gluc",
        "smoke",
        "alco",
        "active",
    ]
    return df, features, "cardio"


def load_heart() -> tuple[pd.DataFrame, list[str], str]:
    path = DATA_ROOT / "Heart Attack" / "heart_processed.csv"
    df = pd.read_csv(path)
    df = df.assign(Cholesterol_zero=df["Cholesterol"].eq(0).astype(int))
    features = [col for col in df.columns if col != "HeartDisease"]
    return df, features, "HeartDisease"


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, float | int | str]] = []

    cardio_df, cardio_features, cardio_target = load_clean_cardio()
    cardio_rows, cardio_coef = run_dataset(
        "cardio_base_clean_logreg_numpy",
        cardio_df,
        cardio_features,
        cardio_target,
        n_iter=900,
    )
    rows.extend(cardio_rows)

    heart_df, heart_features, heart_target = load_heart()
    heart_rows, heart_coef = run_dataset(
        "heart_processed_logreg_numpy",
        heart_df,
        heart_features,
        heart_target,
        n_iter=1500,
    )
    rows.extend(heart_rows)

    metrics_df = pd.DataFrame(rows)
    metrics_df.to_csv(OUT_TABLES / "baseline_metrics.csv", index=False)
    cardio_coef.to_csv(OUT_TABLES / "cardio_logreg_coefficients.csv", index=False)
    heart_coef.to_csv(OUT_TABLES / "heart_logreg_coefficients.csv", index=False)

    print("Wrote outputs/tables/baseline_metrics.csv")
    print(metrics_df[["dataset", "split", "rows", "auroc", "accuracy", "brier"]].to_string(index=False))


if __name__ == "__main__":
    main()

