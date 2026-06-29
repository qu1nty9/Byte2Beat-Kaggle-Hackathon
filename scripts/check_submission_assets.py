from __future__ import annotations

import json
import re
from pathlib import Path

import nbformat
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ASSETS = [
    "README.md",
    "requirements.txt",
    "Makefile",
    "notebooks/01_eda_and_baseline.ipynb",
    "notebooks/02_final_kaggle_notebook.ipynb",
    "research/kaggle_writeup_draft.md",
    "research/ai_usage_disclosure.md",
    "paper/manuscript_outline.md",
    "submission/kaggle_writeup_team_template.md",
    "submission/result_cards.md",
    "submission/figure_manifest.md",
    "submission/final_submission_checklist.md",
    "outputs/tables/model_comparison.csv",
    "outputs/tables/cross_validation_summary.csv",
    "outputs/tables/cleaning_sensitivity_metrics.csv",
    "outputs/tables/error_analysis_summary.csv",
    "outputs/tables/error_analysis_by_group.csv",
    "outputs/figures/cardio_systolic_bp_raw_vs_clean.png",
    "outputs/figures/cardio_target_by_bp_band.png",
    "outputs/figures/cleaning_sensitivity_auroc.png",
    "outputs/figures/model_comparison_auroc.png",
    "outputs/figures/calibration_curve.png",
    "outputs/figures/feature_importance.png",
    "outputs/figures/error_type_by_bp_band.png",
]

TABLE_REQUIREMENTS = {
    "outputs/tables/model_comparison.csv": {
        "dataset",
        "model",
        "split",
        "rows",
        "auroc",
        "auprc",
        "accuracy",
        "brier",
    },
    "outputs/tables/cross_validation_summary.csv": {
        "dataset",
        "model",
        "cv_folds",
        "cv_auroc_mean",
        "cv_auroc_std",
        "cv_auprc_mean",
    },
    "outputs/tables/cleaning_sensitivity_metrics.csv": {
        "cleaning_profile",
        "dataset",
        "model",
        "split",
        "rows",
        "auroc",
        "brier",
    },
    "outputs/tables/error_analysis_summary.csv": {
        "error_type",
        "rows",
        "share",
        "mean_predicted_risk",
    },
    "outputs/tables/error_analysis_by_group.csv": {
        "group_col",
        "group_value",
        "rows",
        "fp_rate_among_negatives",
        "fn_rate_among_positives",
    },
    "outputs/tables/cardio_cleaning_impact.csv": {
        "subset",
        "rows",
        "target_rate",
        "rows_removed_vs_raw",
        "removed_fraction_vs_raw",
    },
    "outputs/tables/feature_importance.csv": {
        "dataset",
        "model",
        "feature",
        "importance_mean",
        "importance_std",
    },
}

FIGURE_REQUIREMENTS = [
    "outputs/figures/cardio_systolic_bp_raw_vs_clean.png",
    "outputs/figures/cardio_target_by_bp_band.png",
    "outputs/figures/cardio_cleaning_flow.png",
    "outputs/figures/cleaning_sensitivity_auroc.png",
    "outputs/figures/cleaning_sensitivity_brier.png",
    "outputs/figures/model_comparison_auroc.png",
    "outputs/figures/roc_curves.png",
    "outputs/figures/pr_curves.png",
    "outputs/figures/calibration_curve.png",
    "outputs/figures/feature_importance.png",
    "outputs/figures/error_confusion_matrix.png",
    "outputs/figures/error_prediction_distribution.png",
    "outputs/figures/error_type_by_bp_band.png",
]

NOTEBOOK_REQUIREMENTS = {
    "notebooks/01_eda_and_baseline.ipynb": {"must_be_executed": False},
    "notebooks/02_final_kaggle_notebook.ipynb": {"must_be_executed": True},
}

PRIVATE_PATH_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"/private/(var|tmp)"),
    re.compile(r"Documents/Kaggle"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\"),
]


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_required_assets() -> list[str]:
    missing = [asset for asset in REQUIRED_ASSETS if not (ROOT / asset).exists()]
    return [f"Missing required asset: {asset}" for asset in missing]


def check_tables() -> list[str]:
    failures: list[str] = []
    for relative_path, required_columns in TABLE_REQUIREMENTS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"Missing required table: {relative_path}")
            continue

        try:
            frame = pd.read_csv(path)
        except Exception as exc:  # pragma: no cover - defensive CLI validation
            failures.append(f"Could not read {relative_path}: {exc}")
            continue

        if frame.empty:
            failures.append(f"Required table is empty: {relative_path}")

        missing_columns = sorted(required_columns.difference(frame.columns))
        if missing_columns:
            failures.append(
                f"{relative_path} is missing columns: {', '.join(missing_columns)}"
            )
    return failures


def check_json_artifacts() -> list[str]:
    failures: list[str] = []

    data_audit_path = ROOT / "outputs/tables/data_audit.json"
    try:
        with data_audit_path.open(encoding="utf-8") as handle:
            data_audit = json.load(handle)
    except Exception as exc:  # pragma: no cover - defensive CLI validation
        failures.append(f"Could not read {_relative(data_audit_path)}: {exc}")
        data_audit = {}

    for key in ["cardio_base", "heart_processed", "ecg_timeseries_light"]:
        if key not in data_audit:
            failures.append(f"data_audit.json is missing dataset key: {key}")

    ecg_audit_path = ROOT / "outputs/tables/ecg_schema_audit.json"
    try:
        with ecg_audit_path.open(encoding="utf-8") as handle:
            ecg_audit = json.load(handle)
    except Exception as exc:  # pragma: no cover - defensive CLI validation
        failures.append(f"Could not read {_relative(ecg_audit_path)}: {exc}")
        ecg_audit = {}

    if "duplicate_nonempty_header_count" not in ecg_audit:
        failures.append("ecg_schema_audit.json lacks duplicate-header evidence")

    return failures


def check_figures() -> list[str]:
    failures: list[str] = []
    for relative_path in FIGURE_REQUIREMENTS:
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"Missing required figure: {relative_path}")
            continue
        if path.stat().st_size < 1_000:
            failures.append(f"Figure appears too small or empty: {relative_path}")
            continue
        try:
            with Image.open(path) as image:
                width, height = image.size
                image.verify()
            if width < 300 or height < 200:
                failures.append(
                    f"Figure dimensions are unexpectedly small: {relative_path}"
                )
        except Exception as exc:  # pragma: no cover - defensive CLI validation
            failures.append(f"Could not verify figure {relative_path}: {exc}")
    return failures


def check_notebooks() -> list[str]:
    failures: list[str] = []

    for relative_path, requirements in NOTEBOOK_REQUIREMENTS.items():
        path = ROOT / relative_path
        if not path.exists():
            failures.append(f"Missing required notebook: {relative_path}")
            continue

        try:
            notebook = nbformat.read(path, as_version=4)
        except Exception as exc:  # pragma: no cover - defensive CLI validation
            failures.append(f"Could not read notebook {relative_path}: {exc}")
            continue

        notebook_text = path.read_text(encoding="utf-8")
        for pattern in PRIVATE_PATH_PATTERNS:
            if pattern.search(notebook_text):
                failures.append(
                    f"Notebook contains a private/local path pattern: {relative_path}"
                )
                break

        error_cells = []
        for index, cell in enumerate(notebook.cells, start=1):
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    error_cells.append(str(index))

        if error_cells:
            failures.append(
                f"Notebook has error outputs in cells: {relative_path} "
                f"({', '.join(error_cells)})"
            )

        if requirements["must_be_executed"]:
            unexecuted = [
                str(index)
                for index, cell in enumerate(notebook.cells, start=1)
                if cell.cell_type == "code" and cell.get("execution_count") is None
            ]
            if unexecuted:
                failures.append(
                    f"Notebook has unexecuted code cells: {relative_path} "
                    f"({', '.join(unexecuted)})"
                )

    return failures


def main() -> None:
    checks = [
        ("required assets", check_required_assets),
        ("tables", check_tables),
        ("json artifacts", check_json_artifacts),
        ("figures", check_figures),
        ("notebooks", check_notebooks),
    ]

    failures: list[str] = []
    for label, check in checks:
        check_failures = check()
        if check_failures:
            failures.extend(check_failures)
            print(f"[FAIL] {label}: {len(check_failures)} issue(s)")
        else:
            print(f"[OK] {label}")

    if failures:
        print("\nSubmission package issues:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print(
        "\nSubmission package quality gate passed: "
        f"{len(REQUIRED_ASSETS)} assets, "
        f"{len(TABLE_REQUIREMENTS)} tables, "
        f"{len(FIGURE_REQUIREMENTS)} figures, "
        f"{len(NOTEBOOK_REQUIREMENTS)} notebooks."
    )


if __name__ == "__main__":
    main()
