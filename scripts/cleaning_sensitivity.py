from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib_cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from byte2beat.data import (
    CARDIO_CLEANING_PROFILES,
    CARDIO_FEATURES,
    CARDIO_TARGET,
    load_cardio_base,
    load_cardio_by_profile,
)
from byte2beat.evaluation import classification_metrics
from byte2beat.paths import FIGURES_DIR, TABLES_DIR, ensure_output_dirs
from byte2beat.plotting import save_current_figure, set_plot_style


SEED = 42


def sensitivity_models(features: list[str]) -> dict[str, Pipeline]:
    scaler = ColumnTransformer(
        [("scale", StandardScaler(), features)],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    passthrough = ColumnTransformer(
        [("features", "passthrough", features)],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    return {
        "logistic_l2": Pipeline(
            [
                ("features", scaler),
                ("model", LogisticRegression(max_iter=2500, solver="lbfgs", random_state=SEED)),
            ]
        ),
        "hist_gradient_boosting": Pipeline(
            [
                ("features", passthrough),
                (
                    "model",
                    HistGradientBoostingClassifier(
                        max_iter=220,
                        learning_rate=0.055,
                        l2_regularization=0.01,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
    }


def summarize_profiles() -> pd.DataFrame:
    raw = load_cardio_base()
    rows = []
    for profile, config in CARDIO_CLEANING_PROFILES.items():
        df = load_cardio_by_profile(profile)
        rows.append(
            {
                "profile": profile,
                "description": config["description"],
                "rows": len(df),
                "rows_removed": len(raw) - len(df),
                "removed_fraction": (len(raw) - len(df)) / len(raw),
                "target_rate": df[CARDIO_TARGET].mean(),
                "age_mean": df["age_years"].mean(),
                "ap_hi_mean": df["ap_hi"].mean(),
                "ap_lo_mean": df["ap_lo"].mean(),
                "bmi_mean": df["bmi"].mean(),
            }
        )
    return pd.DataFrame(rows)


def evaluate_profile(profile: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = load_cardio_by_profile(profile)
    x = df[CARDIO_FEATURES].astype(float)
    y = df[CARDIO_TARGET].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=SEED,
        stratify=y,
    )

    scoring = {
        "auroc": "roc_auc",
        "auprc": "average_precision",
        "accuracy": "accuracy",
        "neg_brier": "neg_brier_score",
        "neg_log_loss": "neg_log_loss",
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    metric_rows = []
    cv_rows = []
    for model_name, model in sensitivity_models(CARDIO_FEATURES).items():
        fitted = model.fit(x_train, y_train)
        y_test_score = fitted.predict_proba(x_test)[:, 1]
        row = classification_metrics(y_test, y_test_score, "cardio", model_name, "test")
        row["cleaning_profile"] = profile
        metric_rows.append(row)

        cv_result = cross_validate(
            model,
            x,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=1,
            error_score="raise",
        )
        cv_rows.append(
            {
                "cleaning_profile": profile,
                "model": model_name,
                "cv_folds": 5,
                "cv_auroc_mean": cv_result["test_auroc"].mean(),
                "cv_auroc_std": cv_result["test_auroc"].std(),
                "cv_auprc_mean": cv_result["test_auprc"].mean(),
                "cv_auprc_std": cv_result["test_auprc"].std(),
                "cv_accuracy_mean": cv_result["test_accuracy"].mean(),
                "cv_accuracy_std": cv_result["test_accuracy"].std(),
                "cv_brier_mean": (-cv_result["test_neg_brier"]).mean(),
                "cv_log_loss_mean": (-cv_result["test_neg_log_loss"]).mean(),
            }
        )
    return pd.DataFrame(metric_rows), pd.DataFrame(cv_rows)


def write_figures(summary: pd.DataFrame, metrics: pd.DataFrame) -> None:
    set_plot_style()
    plt.figure(figsize=(8, 4.8))
    ax = sns.barplot(data=summary, x="profile", y="rows", color="#427AA1")
    ax.set_title("Rows retained by cardiac cleaning profile")
    ax.set_xlabel("Cleaning profile")
    ax.set_ylabel("Rows retained")
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=3)
    save_current_figure(FIGURES_DIR / "cleaning_sensitivity_rows.png")

    set_plot_style()
    plt.figure(figsize=(8, 4.8))
    ax = sns.lineplot(data=metrics, x="cleaning_profile", y="auroc", hue="model", marker="o")
    ax.set_title("Held-out AUROC is stable across cleaning profiles")
    ax.set_xlabel("Cleaning profile")
    ax.set_ylabel("Test AUROC")
    ax.set_ylim(0.75, 0.82)
    save_current_figure(FIGURES_DIR / "cleaning_sensitivity_auroc.png")

    set_plot_style()
    plt.figure(figsize=(8, 4.8))
    ax = sns.lineplot(data=metrics, x="cleaning_profile", y="brier", hue="model", marker="o")
    ax.set_title("Brier score across cleaning profiles")
    ax.set_xlabel("Cleaning profile")
    ax.set_ylabel("Test Brier score")
    save_current_figure(FIGURES_DIR / "cleaning_sensitivity_brier.png")


def main() -> None:
    ensure_output_dirs()
    summary = summarize_profiles()
    metric_tables = []
    cv_tables = []
    for profile in CARDIO_CLEANING_PROFILES:
        metrics, cv = evaluate_profile(profile)
        metric_tables.append(metrics)
        cv_tables.append(cv)

    metrics = pd.concat(metric_tables, ignore_index=True)
    cv = pd.concat(cv_tables, ignore_index=True)
    summary.to_csv(TABLES_DIR / "cleaning_sensitivity_summary.csv", index=False)
    metrics.to_csv(TABLES_DIR / "cleaning_sensitivity_metrics.csv", index=False)
    cv.to_csv(TABLES_DIR / "cleaning_sensitivity_cv.csv", index=False)
    write_figures(summary, metrics)

    print("Wrote cleaning sensitivity tables and figures")
    print(metrics[["cleaning_profile", "model", "rows", "auroc", "auprc", "accuracy", "brier"]].to_string(index=False))


if __name__ == "__main__":
    main()
