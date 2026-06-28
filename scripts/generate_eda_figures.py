from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib_cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".cache"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sys.path.insert(0, str(ROOT / "src"))

from byte2beat.data import CARDIO_TARGET, cardio_age_band, cardio_bp_band, cardio_plausibility_mask, load_cardio_base
from byte2beat.paths import FIGURES_DIR, TABLES_DIR, ensure_output_dirs
from byte2beat.plotting import save_current_figure, set_plot_style


def cleaning_flow_figure(df: pd.DataFrame) -> None:
    body_mask = df["height"].between(120, 220) & df["weight"].between(30, 250) & df["bmi"].between(10, 80)
    bp_mask = df["ap_hi"].between(80, 250) & df["ap_lo"].between(40, 150) & (df["ap_lo"] <= df["ap_hi"])
    rows = pd.DataFrame(
        {
            "step": ["Raw", "Body plausibility", "BP plausibility", "Body + BP"],
            "rows": [len(df), int(body_mask.sum()), int(bp_mask.sum()), int((body_mask & bp_mask).sum())],
        }
    )
    rows["removed"] = len(df) - rows["rows"]
    rows.to_csv(TABLES_DIR / "cardio_cleaning_flow.csv", index=False)

    set_plot_style()
    plt.figure(figsize=(7.5, 4.5))
    ax = sns.barplot(data=rows, x="step", y="rows", color="#427AA1")
    ax.set_title("Rows retained after plausibility checks")
    ax.set_xlabel("")
    ax.set_ylabel("Rows")
    ax.bar_label(ax.containers[0], fmt="%.0f", padding=3)
    ax.tick_params(axis="x", rotation=15)
    save_current_figure(FIGURES_DIR / "cardio_cleaning_flow.png")


def target_rate_figures(df: pd.DataFrame) -> None:
    clean = df.loc[cardio_plausibility_mask(df)].copy()
    clean["systolic_band"] = cardio_bp_band(clean["ap_hi"])
    clean["age_band"] = cardio_age_band(clean["age_years"])

    bp_summary = (
        clean.groupby("systolic_band", observed=False)
        .agg(rows=(CARDIO_TARGET, "size"), target_rate=(CARDIO_TARGET, "mean"))
        .reset_index()
    )
    age_summary = (
        clean.groupby("age_band", observed=False)
        .agg(rows=(CARDIO_TARGET, "size"), target_rate=(CARDIO_TARGET, "mean"))
        .reset_index()
    )
    bp_summary.to_csv(TABLES_DIR / "cardio_target_rate_by_systolic_band.csv", index=False)
    age_summary.to_csv(TABLES_DIR / "cardio_target_rate_by_age_band.csv", index=False)

    set_plot_style()
    plt.figure(figsize=(7.2, 4.5))
    ax = sns.barplot(data=bp_summary, x="systolic_band", y="target_rate", color="#D1495B")
    ax.set_title("Cardio-positive rate rises sharply with systolic BP")
    ax.set_xlabel("Systolic BP band")
    ax.set_ylabel("Observed cardio-positive rate")
    ax.set_ylim(0, 1)
    ax.bar_label(ax.containers[0], labels=[f"{v:.1%}" for v in bp_summary["target_rate"]], padding=3)
    save_current_figure(FIGURES_DIR / "cardio_target_by_bp_band.png")

    set_plot_style()
    plt.figure(figsize=(7.2, 4.5))
    ax = sns.barplot(data=age_summary, x="age_band", y="target_rate", color="#4F772D")
    ax.set_title("Cardio-positive rate by age band")
    ax.set_xlabel("Age band")
    ax.set_ylabel("Observed cardio-positive rate")
    ax.set_ylim(0, 1)
    ax.bar_label(ax.containers[0], labels=[f"{v:.1%}" for v in age_summary["target_rate"]], padding=3)
    save_current_figure(FIGURES_DIR / "cardio_target_by_age_band.png")


def distribution_figures(df: pd.DataFrame) -> None:
    clean = df.loc[cardio_plausibility_mask(df)].copy()

    set_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    sns.histplot(df["ap_hi"], bins=80, ax=axes[0], color="#8D99AE")
    axes[0].set_xlim(-20, 350)
    axes[0].set_title("Raw systolic BP has implausible values")
    axes[0].set_xlabel("Systolic BP")
    sns.histplot(clean["ap_hi"], bins=50, ax=axes[1], color="#2A9D8F")
    axes[1].set_title("Cleaned systolic BP distribution")
    axes[1].set_xlabel("Systolic BP")
    save_current_figure(FIGURES_DIR / "cardio_systolic_bp_raw_vs_clean.png")

    set_plot_style()
    plt.figure(figsize=(7.5, 4.8))
    ax = sns.kdeplot(data=clean, x="age_years", hue=CARDIO_TARGET, common_norm=False, fill=True, alpha=0.35)
    ax.set_title("Age distribution by cardio target")
    ax.set_xlabel("Age, years")
    ax.set_ylabel("Density")
    save_current_figure(FIGURES_DIR / "cardio_age_distribution_by_target.png")


def main() -> None:
    ensure_output_dirs()
    df = load_cardio_base()
    cleaning_flow_figure(df)
    target_rate_figures(df)
    distribution_figures(df)
    print("Wrote EDA figures to outputs/figures")


if __name__ == "__main__":
    main()
