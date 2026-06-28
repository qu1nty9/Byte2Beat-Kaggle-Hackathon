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

CARDIO_CLEANING_PROFILES = {
    "raw": {
        "height": (0, 1000),
        "weight": (0, 1000),
        "bmi": (0, 1000),
        "ap_hi": (-10000, 20000),
        "ap_lo": (-10000, 20000),
        "require_ap_lo_le_ap_hi": False,
        "description": "No plausibility filtering; included as a stress-test baseline.",
    },
    "lenient": {
        "height": (100, 230),
        "weight": (25, 250),
        "bmi": (8, 90),
        "ap_hi": (60, 300),
        "ap_lo": (30, 200),
        "require_ap_lo_le_ap_hi": True,
        "description": "Broad plausibility rules that remove extreme artifacts while keeping borderline measurements.",
    },
    "current": {
        "height": (120, 220),
        "weight": (30, 250),
        "bmi": (10, 80),
        "ap_hi": (80, 250),
        "ap_lo": (40, 150),
        "require_ap_lo_le_ap_hi": True,
        "description": "Primary rules used in the current project baseline.",
    },
    "strict": {
        "height": (140, 210),
        "weight": (35, 200),
        "bmi": (15, 60),
        "ap_hi": (90, 220),
        "ap_lo": (50, 130),
        "require_ap_lo_le_ap_hi": True,
        "description": "Stricter sensitivity rules for robustness checking.",
    },
}


def load_cardio_base() -> pd.DataFrame:
    df = pd.read_csv(CARDIO_BASE_PATH, sep=";")
    return add_cardio_features(df)


def add_cardio_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["age_years"] = df["age"] / 365.25
    df["bmi"] = df["weight"] / (df["height"] / 100) ** 2
    return df


def cardio_plausibility_mask(df: pd.DataFrame) -> pd.Series:
    return cardio_cleaning_mask(df, "current")


def cardio_cleaning_mask(df: pd.DataFrame, profile: str = "current") -> pd.Series:
    if profile not in CARDIO_CLEANING_PROFILES:
        valid = ", ".join(CARDIO_CLEANING_PROFILES)
        raise ValueError(f"Unknown cleaning profile {profile!r}. Valid profiles: {valid}")

    rules = CARDIO_CLEANING_PROFILES[profile]
    mask = (
        df["height"].between(*rules["height"])
        & df["weight"].between(*rules["weight"])
        & df["bmi"].between(*rules["bmi"])
        & df["ap_hi"].between(*rules["ap_hi"])
        & df["ap_lo"].between(*rules["ap_lo"])
    )
    if rules["require_ap_lo_le_ap_hi"]:
        mask = mask & (df["ap_lo"] <= df["ap_hi"])
    return mask


def load_cardio_by_profile(profile: str = "current") -> pd.DataFrame:
    df = load_cardio_base()
    return df.loc[cardio_cleaning_mask(df, profile)].copy()


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
