from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = ROOT / "docs"
DATA_ROOT = DOCS_ROOT / "drive-download-20260627T215828Z-3-001" / "Datasets"
OUTPUTS_ROOT = ROOT / "outputs"
TABLES_DIR = OUTPUTS_ROOT / "tables"
FIGURES_DIR = OUTPUTS_ROOT / "figures"
MODELS_DIR = OUTPUTS_ROOT / "models"


def ensure_output_dirs() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

