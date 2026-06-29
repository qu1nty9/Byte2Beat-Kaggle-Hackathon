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
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from byte2beat.data import CARDIO_FEATURES, CARDIO_TARGET, cardio_age_band, cardio_bp_band, load_cardio_by_profile
from byte2beat.paths import FIGURES_DIR, TABLES_DIR, ensure_output_dirs
from byte2beat.plotting import save_current_figure, set_plot_style


SEED = 42
MODEL_NAME = "hist_gradient_boosting"
ERROR_ORDER = ["TN", "FP", "FN", "TP"]


def selected_model(features: list[str]) -> Pipeline:
    passthrough = ColumnTransformer(
        [("features", "passthrough", features)],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    return Pipeline(
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
    )


def assign_error_type(y_true: pd.Series, y_pred: pd.Series) -> pd.Series:
    return pd.Series(
        [
            "TP" if truth == 1 and pred == 1 else
            "TN" if truth == 0 and pred == 0 else
            "FP" if truth == 0 and pred == 1 else
            "FN"
            for truth, pred in zip(y_true, y_pred)
        ],
        index=y_true.index,
    )


def build_predictions() -> pd.DataFrame:
    df = load_cardio_by_profile("current")
    x = df[CARDIO_FEATURES].astype(float)
    y = df[CARDIO_TARGET].astype(int)
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.25,
        random_state=SEED,
        stratify=y,
    )

    model = selected_model(CARDIO_FEATURES).fit(x_train, y_train)
    score = model.predict_proba(x_test)[:, 1]
    pred = (score >= 0.5).astype(int)

    out = df.loc[x_test.index].copy()
    out["y_true"] = y_test
    out["predicted_risk"] = score
    out["y_pred"] = pred
    out["error_type"] = assign_error_type(out["y_true"], out["y_pred"])
    out["bp_band"] = cardio_bp_band(out["ap_hi"])
    out["age_band"] = cardio_age_band(out["age_years"])
    out["absolute_error"] = (out["predicted_risk"] - out["y_true"]).abs()
    return out


def write_summary_tables(predictions: pd.DataFrame) -> None:
    summary = (
        predictions.groupby("error_type", observed=False)
        .agg(
            rows=("y_true", "size"),
            share=("y_true", lambda s: len(s) / len(predictions)),
            mean_predicted_risk=("predicted_risk", "mean"),
            mean_age=("age_years", "mean"),
            mean_systolic_bp=("ap_hi", "mean"),
            mean_diastolic_bp=("ap_lo", "mean"),
            mean_bmi=("bmi", "mean"),
            mean_cholesterol=("cholesterol", "mean"),
            active_rate=("active", "mean"),
            smoke_rate=("smoke", "mean"),
        )
        .reindex(ERROR_ORDER)
        .reset_index()
    )
    summary.to_csv(TABLES_DIR / "error_analysis_summary.csv", index=False)

    group_tables = []
    error_type_tables = []
    for group_col in ["bp_band", "age_band", "gender", "cholesterol"]:
        grouped_rows = []
        for group_value, group_df in predictions.groupby(group_col, observed=False, dropna=False):
            if len(group_df) == 0:
                continue
            tn, fp, fn, tp = confusion_matrix(group_df["y_true"], group_df["y_pred"], labels=[0, 1]).ravel()
            actual_pos = tp + fn
            actual_neg = tn + fp
            grouped_rows.append(
                {
                    "group_col": group_col,
                    "group_value": str(group_value),
                    "rows": len(group_df),
                    "positive_rate": group_df["y_true"].mean(),
                    "predicted_positive_rate": group_df["y_pred"].mean(),
                    "mean_predicted_risk": group_df["predicted_risk"].mean(),
                    "accuracy": (group_df["y_true"] == group_df["y_pred"]).mean(),
                    "fp_rate_among_negatives": fp / actual_neg if actual_neg else float("nan"),
                    "fn_rate_among_positives": fn / actual_pos if actual_pos else float("nan"),
                    "tp": tp,
                    "tn": tn,
                    "fp": fp,
                    "fn": fn,
                }
            )
        group_tables.append(pd.DataFrame(grouped_rows))

        counts = (
            predictions.groupby([group_col, "error_type"], observed=False)
            .size()
            .rename("rows")
            .reset_index()
        )
        totals = counts.groupby(group_col, observed=False)["rows"].transform("sum")
        counts["share_within_group"] = counts["rows"] / totals
        counts.insert(0, "group_col", group_col)
        counts = counts.rename(columns={group_col: "group_value"})
        counts["group_value"] = counts["group_value"].astype(str)
        error_type_tables.append(counts)

    pd.concat(group_tables, ignore_index=True).to_csv(TABLES_DIR / "error_analysis_by_group.csv", index=False)
    pd.concat(error_type_tables, ignore_index=True).to_csv(TABLES_DIR / "error_type_by_group.csv", index=False)

    high_confidence_fp = (
        predictions[predictions["error_type"].eq("FP")]
        .sort_values("predicted_risk", ascending=False)
        .head(25)
    )
    high_confidence_fn = (
        predictions[predictions["error_type"].eq("FN")]
        .sort_values("predicted_risk", ascending=True)
        .head(25)
    )
    high_confidence = pd.concat([high_confidence_fp, high_confidence_fn], ignore_index=False)
    cols = [
        "id",
        "y_true",
        "y_pred",
        "predicted_risk",
        "error_type",
        "age_years",
        "gender",
        "ap_hi",
        "ap_lo",
        "cholesterol",
        "gluc",
        "bmi",
        "active",
        "smoke",
    ]
    high_confidence[cols].to_csv(TABLES_DIR / "error_high_confidence_examples.csv", index=True)


def stacked_error_plot(predictions: pd.DataFrame, group_col: str, path: Path, title: str) -> None:
    counts = pd.crosstab(predictions[group_col], predictions["error_type"], normalize="index")
    counts = counts.reindex(columns=ERROR_ORDER, fill_value=0)
    set_plot_style()
    ax = counts.plot(
        kind="bar",
        stacked=True,
        figsize=(8.2, 5.0),
        color=["#4F772D", "#E76F51", "#F4A261", "#427AA1"],
    )
    ax.set_title(title)
    ax.set_xlabel(group_col.replace("_", " ").title())
    ax.set_ylabel("Share within group")
    ax.legend(title="Prediction type", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=20)
    save_current_figure(path)


def write_figures(predictions: pd.DataFrame) -> None:
    cm = confusion_matrix(predictions["y_true"], predictions["y_pred"], labels=[0, 1])
    set_plot_style()
    plt.figure(figsize=(5.8, 4.8))
    ax = sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Predicted 0", "Predicted 1"],
        yticklabels=["Actual 0", "Actual 1"],
    )
    ax.set_title("Confusion matrix for selected cardiac model")
    ax.set_xlabel("")
    ax.set_ylabel("")
    save_current_figure(FIGURES_DIR / "error_confusion_matrix.png")

    set_plot_style()
    plt.figure(figsize=(8.0, 5.0))
    ax = sns.histplot(
        data=predictions,
        x="predicted_risk",
        hue="y_true",
        bins=35,
        stat="density",
        common_norm=False,
        alpha=0.45,
    )
    ax.set_title("Predicted risk distribution by actual class")
    ax.set_xlabel("Predicted cardio-positive risk")
    ax.set_ylabel("Density")
    save_current_figure(FIGURES_DIR / "error_prediction_distribution.png")

    stacked_error_plot(
        predictions,
        "bp_band",
        FIGURES_DIR / "error_type_by_bp_band.png",
        "Prediction types by systolic BP band",
    )
    stacked_error_plot(
        predictions,
        "age_band",
        FIGURES_DIR / "error_type_by_age_band.png",
        "Prediction types by age band",
    )
    stacked_error_plot(
        predictions,
        "cholesterol",
        FIGURES_DIR / "error_type_by_cholesterol.png",
        "Prediction types by cholesterol category",
    )


def main() -> None:
    ensure_output_dirs()
    predictions = build_predictions()
    predictions.to_csv(TABLES_DIR / "error_analysis_predictions.csv", index=True)
    write_summary_tables(predictions)
    write_figures(predictions)
    print("Wrote error analysis tables and figures")
    print(pd.read_csv(TABLES_DIR / "error_analysis_summary.csv").to_string(index=False))


if __name__ == "__main__":
    main()

