from __future__ import annotations

import os
import sys

os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib_cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    roc_auc_score,
)

from byte2beat.paths import FIGURES_DIR, TABLES_DIR, ensure_output_dirs
from byte2beat.plotting import save_current_figure, set_plot_style


SEED = 42
N_BOOTSTRAPS = 2000
DATASET = "cardio_clean"
MODEL = "hist_gradient_boosting"
PREDICTIONS_PATH = TABLES_DIR / "cardio_clean_test_predictions.csv"
BOOTSTRAP_CI_PATH = TABLES_DIR / "selected_model_bootstrap_ci.csv"
BOOTSTRAP_DISTRIBUTION_PATH = TABLES_DIR / "selected_model_bootstrap_distribution.csv"
THRESHOLD_TABLE_PATH = TABLES_DIR / "selected_model_threshold_analysis.csv"
THRESHOLD_SUMMARY_PATH = TABLES_DIR / "selected_model_threshold_summary.csv"


def load_selected_predictions() -> tuple[np.ndarray, np.ndarray]:
    predictions = pd.read_csv(PREDICTIONS_PATH)
    y_true = predictions["cardio"].to_numpy(dtype=int)
    y_score = predictions[MODEL].to_numpy(dtype=float)
    return y_true, y_score


def threshold_metrics(y_true: np.ndarray, y_score: np.ndarray, threshold: float) -> dict[str, float | int]:
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    predicted_positive = tp + fp
    predicted_negative = tn + fn
    actual_positive = tp + fn
    actual_negative = tn + fp

    return {
        "threshold": float(threshold),
        "rows": int(len(y_true)),
        "predicted_positive_rate": float(y_pred.mean()),
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "sensitivity": float(tp / actual_positive) if actual_positive else np.nan,
        "specificity": float(tn / actual_negative) if actual_negative else np.nan,
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "tp": int(tp),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "predicted_positive": int(predicted_positive),
        "predicted_negative": int(predicted_negative),
    }


def bootstrap_metrics(y_true: np.ndarray, y_score: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    rows = []
    n = len(y_true)

    for iteration in range(N_BOOTSTRAPS):
        sample_idx = rng.integers(0, n, size=n)
        y_sample = y_true[sample_idx]
        score_sample = y_score[sample_idx]
        if len(np.unique(y_sample)) < 2:
            continue

        y_pred = (score_sample >= 0.5).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_sample, y_pred, labels=[0, 1]).ravel()
        rows.extend(
            [
                {
                    "bootstrap_iteration": iteration,
                    "metric": "auroc",
                    "value": roc_auc_score(y_sample, score_sample),
                },
                {
                    "bootstrap_iteration": iteration,
                    "metric": "auprc",
                    "value": average_precision_score(y_sample, score_sample),
                },
                {
                    "bootstrap_iteration": iteration,
                    "metric": "accuracy",
                    "value": accuracy_score(y_sample, y_pred),
                },
                {
                    "bootstrap_iteration": iteration,
                    "metric": "brier",
                    "value": brier_score_loss(y_sample, score_sample),
                },
                {
                    "bootstrap_iteration": iteration,
                    "metric": "sensitivity",
                    "value": tp / (tp + fn) if tp + fn else np.nan,
                },
                {
                    "bootstrap_iteration": iteration,
                    "metric": "specificity",
                    "value": tn / (tn + fp) if tn + fp else np.nan,
                },
            ]
        )

    distribution = pd.DataFrame(rows)

    point_metrics = {
        "auroc": roc_auc_score(y_true, y_score),
        "auprc": average_precision_score(y_true, y_score),
        "accuracy": threshold_metrics(y_true, y_score, 0.5)["accuracy"],
        "brier": brier_score_loss(y_true, y_score),
        "sensitivity": threshold_metrics(y_true, y_score, 0.5)["sensitivity"],
        "specificity": threshold_metrics(y_true, y_score, 0.5)["specificity"],
    }

    ci_rows = []
    for metric, group in distribution.groupby("metric", observed=False):
        values = group["value"].dropna().to_numpy()
        ci_rows.append(
            {
                "dataset": DATASET,
                "model": MODEL,
                "split": "heldout_test",
                "metric": metric,
                "point_estimate": point_metrics[metric],
                "bootstrap_mean": float(np.mean(values)),
                "bootstrap_std": float(np.std(values, ddof=1)),
                "ci_lower_95": float(np.percentile(values, 2.5)),
                "ci_upper_95": float(np.percentile(values, 97.5)),
                "bootstrap_iterations": int(len(values)),
            }
        )

    ci = pd.DataFrame(ci_rows).sort_values("metric")
    return distribution, ci


def threshold_analysis(y_true: np.ndarray, y_score: np.ndarray) -> tuple[pd.DataFrame, pd.DataFrame]:
    thresholds = np.round(np.arange(0.10, 0.91, 0.05), 2)
    table = pd.DataFrame([threshold_metrics(y_true, y_score, threshold) for threshold in thresholds])
    table.insert(0, "model", MODEL)
    table.insert(0, "dataset", DATASET)

    max_f1_row = table.loc[table["f1"].idxmax()]
    max_accuracy_row = table.loc[table["accuracy"].idxmax()]
    high_sensitivity_candidates = table[table["sensitivity"] >= 0.80]
    high_specificity_candidates = table[table["specificity"] >= 0.80]

    operating_rows = [
        {"operating_point": "default_threshold_0_50", **threshold_metrics(y_true, y_score, 0.50)},
        {"operating_point": "max_f1", **max_f1_row.drop(["dataset", "model"]).to_dict()},
        {"operating_point": "max_accuracy", **max_accuracy_row.drop(["dataset", "model"]).to_dict()},
    ]
    if not high_sensitivity_candidates.empty:
        row = high_sensitivity_candidates.sort_values(["fp", "threshold"]).iloc[0]
        operating_rows.append(
            {
                "operating_point": "sensitivity_at_least_0_80_lowest_fp",
                **row.drop(["dataset", "model"]).to_dict(),
            }
        )
    if not high_specificity_candidates.empty:
        row = high_specificity_candidates.sort_values(["fn", "threshold"]).iloc[0]
        operating_rows.append(
            {
                "operating_point": "specificity_at_least_0_80_lowest_fn",
                **row.drop(["dataset", "model"]).to_dict(),
            }
        )

    summary = pd.DataFrame(operating_rows)
    summary.insert(0, "model", MODEL)
    summary.insert(0, "dataset", DATASET)
    return table, summary


def write_bootstrap_figure(ci: pd.DataFrame) -> None:
    plot_data = ci[ci["metric"].isin(["auroc", "auprc", "accuracy", "brier"])].copy()
    metric_labels = {
        "auroc": "AUROC",
        "auprc": "AUPRC",
        "accuracy": "Accuracy",
        "brier": "Brier score",
    }
    plot_data["metric_label"] = plot_data["metric"].map(metric_labels)
    plot_data["error_low"] = plot_data["point_estimate"] - plot_data["ci_lower_95"]
    plot_data["error_high"] = plot_data["ci_upper_95"] - plot_data["point_estimate"]

    set_plot_style()
    plt.figure(figsize=(8.2, 4.8))
    ax = plt.gca()
    ax.errorbar(
        plot_data["point_estimate"],
        plot_data["metric_label"],
        xerr=[plot_data["error_low"], plot_data["error_high"]],
        fmt="o",
        color="#1F4E79",
        ecolor="#7A9EB1",
        capsize=4,
    )
    ax.set_title("Bootstrap 95% intervals for selected model metrics")
    ax.set_xlabel("Metric value")
    ax.set_ylabel("")
    ax.set_xlim(0.15, 0.85)
    save_current_figure(FIGURES_DIR / "selected_model_bootstrap_ci.png")


def write_threshold_figures(table: pd.DataFrame) -> None:
    long = table.melt(
        id_vars=["threshold"],
        value_vars=["precision", "sensitivity", "specificity", "f1", "accuracy"],
        var_name="metric",
        value_name="value",
    )
    metric_order = ["sensitivity", "specificity", "precision", "f1", "accuracy"]
    long["metric"] = pd.Categorical(long["metric"], categories=metric_order, ordered=True)

    set_plot_style()
    plt.figure(figsize=(8.6, 5.2))
    ax = sns.lineplot(data=long, x="threshold", y="value", hue="metric", marker="o")
    ax.set_title("Threshold trade-offs for selected cardiac model")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Metric value")
    ax.set_ylim(0, 1.02)
    save_current_figure(FIGURES_DIR / "selected_model_threshold_tradeoff.png")

    counts = table.melt(
        id_vars=["threshold"],
        value_vars=["tp", "fp", "fn", "tn"],
        var_name="confusion_type",
        value_name="count",
    )
    counts["confusion_type"] = pd.Categorical(
        counts["confusion_type"],
        categories=["tp", "fp", "fn", "tn"],
        ordered=True,
    )

    set_plot_style()
    plt.figure(figsize=(8.6, 5.2))
    ax = sns.lineplot(data=counts, x="threshold", y="count", hue="confusion_type", marker="o")
    ax.set_title("Confusion counts across decision thresholds")
    ax.set_xlabel("Decision threshold")
    ax.set_ylabel("Rows")
    save_current_figure(FIGURES_DIR / "selected_model_threshold_counts.png")


def main() -> None:
    ensure_output_dirs()
    y_true, y_score = load_selected_predictions()

    distribution, ci = bootstrap_metrics(y_true, y_score)
    distribution.to_csv(BOOTSTRAP_DISTRIBUTION_PATH, index=False)
    ci.to_csv(BOOTSTRAP_CI_PATH, index=False)

    threshold_table, threshold_summary = threshold_analysis(y_true, y_score)
    threshold_table.to_csv(THRESHOLD_TABLE_PATH, index=False)
    threshold_summary.to_csv(THRESHOLD_SUMMARY_PATH, index=False)

    write_bootstrap_figure(ci)
    write_threshold_figures(threshold_table)

    print("Wrote selected model uncertainty and threshold analysis")
    print(ci.to_string(index=False))
    print(threshold_summary.to_string(index=False))


if __name__ == "__main__":
    main()
