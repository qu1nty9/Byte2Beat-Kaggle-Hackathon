from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "docs" / "drive-download-20260627T215828Z-3-001" / "Datasets"
OUT_TABLES = ROOT / "outputs" / "tables"


def summarize_subset(name: str, df: pd.DataFrame, target: str) -> dict[str, float | int | str]:
    return {
        "subset": name,
        "rows": int(len(df)),
        "positive": int(df[target].sum()),
        "negative": int((1 - df[target]).sum()),
        "target_rate": float(df[target].mean()) if len(df) else np.nan,
    }


def cardio_cleaning_impact() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    path = DATA_ROOT / "Cardiac Failure" / "cardio_base.csv"
    df = pd.read_csv(path, sep=";")
    df = df.assign(
        age_years=df["age"] / 365.25,
        bmi=df["weight"] / (df["height"] / 100) ** 2,
    )

    plausible_body = (
        df["height"].between(120, 220)
        & df["weight"].between(30, 250)
        & df["bmi"].between(10, 80)
    )
    plausible_bp = (
        df["ap_hi"].between(80, 250)
        & df["ap_lo"].between(40, 150)
        & (df["ap_lo"] <= df["ap_hi"])
    )
    plausible_all = plausible_body & plausible_bp

    impact = pd.DataFrame(
        [
            summarize_subset("raw", df, "cardio"),
            summarize_subset("plausible_body", df[plausible_body], "cardio"),
            summarize_subset("plausible_bp", df[plausible_bp], "cardio"),
            summarize_subset("plausible_body_and_bp", df[plausible_all], "cardio"),
        ]
    )
    impact["rows_removed_vs_raw"] = int(len(df)) - impact["rows"]
    impact["removed_fraction_vs_raw"] = impact["rows_removed_vs_raw"] / len(df)

    clean = df[plausible_all].copy()
    clean["systolic_band"] = pd.cut(
        clean["ap_hi"],
        bins=[0, 119, 129, 139, 250],
        labels=["<120", "120-129", "130-139", ">=140"],
        include_lowest=True,
    )
    bp_band = (
        clean.groupby("systolic_band", observed=False)
        .agg(rows=("cardio", "size"), target_rate=("cardio", "mean"), mean_age=("age_years", "mean"))
        .reset_index()
    )

    feature_summary = (
        clean.groupby("cardio")
        .agg(
            rows=("cardio", "size"),
            age_years_mean=("age_years", "mean"),
            bmi_mean=("bmi", "mean"),
            ap_hi_mean=("ap_hi", "mean"),
            ap_lo_mean=("ap_lo", "mean"),
            cholesterol_mean=("cholesterol", "mean"),
            gluc_mean=("gluc", "mean"),
            smoke_rate=("smoke", "mean"),
            active_rate=("active", "mean"),
        )
        .reset_index()
    )

    return impact, bp_band, feature_summary


def heart_cleaning_impact() -> tuple[pd.DataFrame, pd.DataFrame]:
    path = DATA_ROOT / "Heart Attack" / "heart_processed.csv"
    df = pd.read_csv(path)

    valid_bp = df["RestingBP"].between(80, 250)
    cholesterol_observed = df["Cholesterol"] > 0
    both = valid_bp & cholesterol_observed

    impact = pd.DataFrame(
        [
            summarize_subset("raw", df, "HeartDisease"),
            summarize_subset("valid_resting_bp", df[valid_bp], "HeartDisease"),
            summarize_subset("cholesterol_observed", df[cholesterol_observed], "HeartDisease"),
            summarize_subset("valid_resting_bp_and_cholesterol_observed", df[both], "HeartDisease"),
        ]
    )
    impact["rows_removed_vs_raw"] = int(len(df)) - impact["rows"]
    impact["removed_fraction_vs_raw"] = impact["rows_removed_vs_raw"] / len(df)

    feature_summary = (
        df.assign(cholesterol_missing_like=df["Cholesterol"].eq(0))
        .groupby("HeartDisease")
        .agg(
            rows=("HeartDisease", "size"),
            age_mean=("Age", "mean"),
            resting_bp_mean=("RestingBP", "mean"),
            cholesterol_mean=("Cholesterol", "mean"),
            cholesterol_zero_rate=("cholesterol_missing_like", "mean"),
            max_hr_mean=("MaxHR", "mean"),
            oldpeak_mean=("Oldpeak", "mean"),
            male_rate=("Sex_M", "mean"),
            exercise_angina_rate=("ExerciseAngina_Y", "mean"),
        )
        .reset_index()
    )

    return impact, feature_summary


def main() -> None:
    OUT_TABLES.mkdir(parents=True, exist_ok=True)

    cardio_impact, cardio_bp_band, cardio_features = cardio_cleaning_impact()
    heart_impact, heart_features = heart_cleaning_impact()

    outputs = {
        "cardio_cleaning_impact.csv": cardio_impact,
        "cardio_target_by_bp_band.csv": cardio_bp_band,
        "cardio_feature_summary_by_target.csv": cardio_features,
        "heart_cleaning_impact.csv": heart_impact,
        "heart_feature_summary_by_target.csv": heart_features,
    }

    for filename, table in outputs.items():
        table.to_csv(OUT_TABLES / filename, index=False)
        print(f"Wrote outputs/tables/{filename} rows={len(table)}")


if __name__ == "__main__":
    main()

