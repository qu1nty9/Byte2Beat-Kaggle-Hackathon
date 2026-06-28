from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[2] / ".matplotlib_cache"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(__file__).resolve().parents[2] / ".cache"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def set_plot_style() -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    plt.rcParams.update(
        {
            "figure.dpi": 140,
            "savefig.dpi": 180,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "axes.titlesize": 12,
            "font.size": 10,
        }
    )


def save_current_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def barplot(
    data: pd.DataFrame,
    x: str,
    y: str,
    path: Path,
    title: str,
    xlabel: str,
    ylabel: str,
    hue: str | None = None,
    rotate_xticks: bool = False,
) -> None:
    set_plot_style()
    plt.figure(figsize=(8, 4.8))
    ax = sns.barplot(data=data, x=x, y=y, hue=hue)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if rotate_xticks:
        ax.tick_params(axis="x", rotation=25)
    save_current_figure(path)
