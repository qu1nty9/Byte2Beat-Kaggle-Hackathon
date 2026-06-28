from __future__ import annotations

import pandas as pd

from byte2beat.paths import DATA_ROOT


CARDIO_BASE_PATH = DATA_ROOT / "Cardiac Failure" / "cardio_base.csv"
CARDIAC_PROCESSED_PATH = DATA_ROOT / "Cardiac Failure" / "cardiac_failure_processed.csv"
HEART_PROCESSED_PATH = DATA_ROOT / "Heart Attack" / "heart_processed.csv"
ECG_TIMESERIES_PATH = DATA_ROOT / "ECG Timeseries" / "ecg_timeseries.csv"

CARDIO_FEATURES = [
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

HEART_TARGET = "HeartDisease"
CARDIO_TARGET = "cardio"


def load_cardio_base() -> pd.DataFrame:
    df = pd.read_csv(CARDIO_BASE_PATH, sep=";")
    return add_cardio_features(df)


def add_cardio_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["age_years"] = df["age"] / 365.25
    df["bmi"] = df["weight"] / (df["height"] / 100) ** 2
    return df


def cardio_plausibility_mask(df: pd.DataFrame) -> pd.Series:
    return (
        df["height"].between(120, 220)
        & df["weight"].between(30, 250)
        & df["bmi"].between(10, 80)
        & df["ap_hi"].between(80, 250)
        & df["ap_lo"].between(40, 150)
        & (df["ap_lo"] <= df["ap_hi"])
    )


def load_cardio_clean() -> pd.DataFrame:
    df = load_cardio_base()
    return df.loc[cardio_plausibility_mask(df)].copy()


def load_heart_processed(add_missing_indicators: bool = True) -> pd.DataFrame:
    df = pd.read_csv(HEART_PROCESSED_PATH)
    if add_missing_indicators:
        df = df.copy()
        df["Cholesterol_zero"] = df["Cholesterol"].eq(0).astype(int)
    return df


def heart_features(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col != HEART_TARGET]


def cardio_bp_band(series: pd.Series) -> pd.Categorical:
    return pd.cut(
        series,
        bins=[0, 119, 129, 139, 250],
        labels=["<120", "120-129", "130-139", ">=140"],
        include_lowest=True,
    )


def cardio_age_band(series: pd.Series) -> pd.Categorical:
    return pd.cut(
        series,
        bins=[0, 39, 49, 59, 120],
        labels=["<40", "40-49", "50-59", ">=60"],
        include_lowest=True,
    )

