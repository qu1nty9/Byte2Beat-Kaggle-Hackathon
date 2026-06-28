from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib_cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "1")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

sys.path.insert(0, str(ROOT / "src"))

from byte2beat.data import (
    CARDIO_FEATURES,
    CARDIO_TARGET,
    HEART_TARGET,
    cardio_age_band,
    cardio_bp_band,
    heart_features,
    load_cardio_clean,
    load_heart_processed,
)
from byte2beat.evaluation import calibration_table, classification_metrics, subgroup_metrics
from byte2beat.paths import FIGURES_DIR, MODELS_DIR, TABLES_DIR, ensure_output_dirs
from byte2beat.plotting import save_current_figure, set_plot_style


SEED = 42


def model_zoo(feature_names: list[str]) -> dict[str, Pipeline]:
    scaler = ColumnTransformer(
        [("scale", StandardScaler(), feature_names)],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    passthrough = ColumnTransformer(
        [("features", "passthrough", feature_names)],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    return {
        "dummy_prior": Pipeline(
            [("features", passthrough), ("model", DummyClassifier(strategy="prior", random_state=SEED))]
        ),
        "logistic_l2": Pipeline(
            [
                ("features", scaler),
                (
                    "model",
                    LogisticRegression(
                        max_iter=2500,
                        random_state=SEED,
                        solver="lbfgs",
                    ),
                ),
            ]
        ),
        "decision_tree_depth4": Pipeline(
            [
                ("features", passthrough),
                (
                    "model",
                    DecisionTreeClassifier(
                        max_depth=4,
                        min_samples_leaf=100,
                        random_state=SEED,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            [
                ("features", passthrough),
                (
                    "model",
                    RandomForestClassifier(
                        n_estimators=300,
                        min_samples_leaf=30,
                        random_state=SEED,
                        n_jobs=1,
                    ),
                ),
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


def run_dataset(dataset_name: str, df: pd.DataFrame, features: list[str], target: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    x = df[features].astype(float)
    y = df[target].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=SEED,
        stratify=y,
    )

    models = model_zoo(features)
    metric_rows = []
    cv_rows = []
    fitted_models = {}
    prediction_frame = pd.DataFrame({target: y_test.to_numpy()}, index=x_test.index)

    scoring = {
        "auroc": "roc_auc",
        "auprc": "average_precision",
        "accuracy": "accuracy",
        "neg_brier": "neg_brier_score",
        "neg_log_loss": "neg_log_loss",
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    for model_name, pipeline in models.items():
        fitted = pipeline.fit(x_train, y_train)
        fitted_models[model_name] = fitted
        y_train_score = fitted.predict_proba(x_train)[:, 1]
        y_test_score = fitted.predict_proba(x_test)[:, 1]
        prediction_frame[model_name] = y_test_score

        metric_rows.append(classification_metrics(y_train, y_train_score, dataset_name, model_name, "train"))
        metric_rows.append(classification_metrics(y_test, y_test_score, dataset_name, model_name, "test"))

        cv_result = cross_validate(
            pipeline,
            x,
            y,
            cv=cv,
            scoring=scoring,
            # Keep single-process execution. Some sandboxed systems disallow
            # joblib/loky semaphore checks even when the code itself is safe.
            n_jobs=1,
            error_score="raise",
        )
        cv_rows.append(
            {
                "dataset": dataset_name,
                "model": model_name,
                "cv_folds": 5,
                "cv_auroc_mean": float(cv_result["test_auroc"].mean()),
                "cv_auroc_std": float(cv_result["test_auroc"].std()),
                "cv_auprc_mean": float(cv_result["test_auprc"].mean()),
                "cv_auprc_std": float(cv_result["test_auprc"].std()),
                "cv_accuracy_mean": float(cv_result["test_accuracy"].mean()),
                "cv_accuracy_std": float(cv_result["test_accuracy"].std()),
                "cv_brier_mean": float((-cv_result["test_neg_brier"]).mean()),
                "cv_log_loss_mean": float((-cv_result["test_neg_log_loss"]).mean()),
            }
        )

    metrics_df = pd.DataFrame(metric_rows)
    cv_df = pd.DataFrame(cv_rows)
    prediction_frame.to_csv(TABLES_DIR / f"{dataset_name}_test_predictions.csv", index=True)

    best_row = (
        metrics_df[(metrics_df["split"] == "test") & (metrics_df["model"] != "dummy_prior")]
        .sort_values(["auroc", "brier"], ascending=[False, True])
        .iloc[0]
    )
    best_model_name = str(best_row["model"])
    best_model = fitted_models[best_model_name]

    calibration = calibration_table(y_test, prediction_frame[best_model_name], dataset_name, best_model_name)
    calibration.to_csv(TABLES_DIR / f"{dataset_name}_calibration_bins.csv", index=False)

    if dataset_name == "cardio_clean":
        subgroup_source = df.loc[x_test.index].copy()
        subgroup_source["prediction"] = prediction_frame[best_model_name].to_numpy()
        subgroup_source["bp_band"] = cardio_bp_band(subgroup_source["ap_hi"])
        subgroup_source["age_band"] = cardio_age_band(subgroup_source["age_years"])
        subgroup_tables = [
            subgroup_metrics(subgroup_source, CARDIO_TARGET, "prediction", "bp_band", dataset_name, best_model_name),
            subgroup_metrics(subgroup_source, CARDIO_TARGET, "prediction", "age_band", dataset_name, best_model_name),
            subgroup_metrics(subgroup_source, CARDIO_TARGET, "prediction", "gender", dataset_name, best_model_name),
            subgroup_metrics(subgroup_source, CARDIO_TARGET, "prediction", "cholesterol", dataset_name, best_model_name),
        ]
        pd.concat(subgroup_tables, ignore_index=True).to_csv(TABLES_DIR / "subgroup_metrics.csv", index=False)
        save_feature_importance(best_model, x_test, y_test, features, dataset_name, best_model_name)
        save_model_plots(metrics_df, prediction_frame, y_test, target, dataset_name, best_model_name)

    return metrics_df, cv_df


def save_feature_importance(
    model: Pipeline,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    features: list[str],
    dataset_name: str,
    model_name: str,
) -> None:
    sample_x = x_test
    sample_y = y_test
    if len(x_test) > 6000:
        sample_x = x_test.sample(n=6000, random_state=SEED)
        sample_y = y_test.loc[sample_x.index]

    result = permutation_importance(
        model,
        sample_x,
        sample_y,
        scoring="roc_auc",
        n_repeats=8,
        random_state=SEED,
        n_jobs=1,
    )
    importance = pd.DataFrame(
        {
            "dataset": dataset_name,
            "model": model_name,
            "feature": features,
            "importance_mean": result.importances_mean,
            "importance_std": result.importances_std,
        }
    ).sort_values("importance_mean", ascending=False)
    importance.to_csv(TABLES_DIR / "feature_importance.csv", index=False)

    set_plot_style()
    plt.figure(figsize=(8, 5.2))
    top = importance.head(12).iloc[::-1]
    ax = plt.barh(top["feature"], top["importance_mean"], xerr=top["importance_std"], color="#2A9D8F")
    plt.title(f"Permutation importance: {model_name}")
    plt.xlabel("Mean AUROC decrease")
    plt.ylabel("")
    save_current_figure(FIGURES_DIR / "feature_importance.png")


def save_model_plots(
    metrics_df: pd.DataFrame,
    predictions: pd.DataFrame,
    y_test: pd.Series,
    target: str,
    dataset_name: str,
    best_model_name: str,
) -> None:
    test_metrics = metrics_df[metrics_df["split"] == "test"].copy()
    test_metrics.to_csv(TABLES_DIR / f"{dataset_name}_test_model_metrics.csv", index=False)

    set_plot_style()
    plt.figure(figsize=(8, 4.8))
    ax = sns.barplot(data=test_metrics.sort_values("auroc"), x="auroc", y="model", color="#427AA1")
    ax.set_title("Test AUROC by model")
    ax.set_xlabel("AUROC")
    ax.set_ylabel("")
    ax.set_xlim(0.45, 1.0)
    save_current_figure(FIGURES_DIR / "model_comparison_auroc.png")

    set_plot_style()
    fig, ax = plt.subplots(figsize=(6.6, 5.5))
    for model_name in [c for c in predictions.columns if c != target]:
        RocCurveDisplay.from_predictions(y_test, predictions[model_name], name=model_name, ax=ax)
    ax.set_title("ROC curves on held-out cardiac test set")
    save_current_figure(FIGURES_DIR / "roc_curves.png")

    set_plot_style()
    fig, ax = plt.subplots(figsize=(6.6, 5.5))
    for model_name in [c for c in predictions.columns if c != target]:
        PrecisionRecallDisplay.from_predictions(y_test, predictions[model_name], name=model_name, ax=ax)
    ax.set_title("Precision-recall curves on held-out cardiac test set")
    save_current_figure(FIGURES_DIR / "pr_curves.png")

    calibration = pd.read_csv(TABLES_DIR / f"{dataset_name}_calibration_bins.csv")
    set_plot_style()
    plt.figure(figsize=(6.6, 5.5))
    plt.plot([0, 1], [0, 1], linestyle="--", color="#6C757D", label="Perfect calibration")
    plt.plot(
        calibration["mean_predicted_risk"],
        calibration["observed_rate"],
        marker="o",
        color="#D1495B",
        label=best_model_name,
    )
    plt.title("Calibration curve for selected cardiac model")
    plt.xlabel("Mean predicted risk")
    plt.ylabel("Observed cardio-positive rate")
    plt.legend()
    save_current_figure(FIGURES_DIR / "calibration_curve.png")


def main() -> None:
    ensure_output_dirs()

    cardio = load_cardio_clean()
    cardio_metrics, cardio_cv = run_dataset("cardio_clean", cardio, CARDIO_FEATURES, CARDIO_TARGET)

    heart = load_heart_processed(add_missing_indicators=True)
    heart_metrics, heart_cv = run_dataset("heart_processed", heart, heart_features(heart), HEART_TARGET)

    metrics = pd.concat([cardio_metrics, heart_metrics], ignore_index=True)
    cv = pd.concat([cardio_cv, heart_cv], ignore_index=True)
    metrics.to_csv(TABLES_DIR / "model_comparison.csv", index=False)
    cv.to_csv(TABLES_DIR / "cross_validation_summary.csv", index=False)

    print("Wrote outputs/tables/model_comparison.csv")
    print(
        metrics[metrics["split"] == "test"]
        .sort_values(["dataset", "auroc"], ascending=[True, False])[
            ["dataset", "model", "rows", "auroc", "auprc", "accuracy", "brier"]
        ]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
