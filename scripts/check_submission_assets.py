from __future__ import annotations

import json
import os
import re
from pathlib import Path

import nbformat
import pandas as pd
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ASSETS = [
    "README.md",
    "RELEASE_NOTES.md",
    "requirements.txt",
    "Makefile",
    "notebooks/01_eda_and_baseline.ipynb",
    "notebooks/02_final_kaggle_notebook.ipynb",
    "research/kaggle_writeup_draft.md",
    "research/ai_usage_disclosure.md",
    "paper/manuscript_outline.md",
    "paper/publication_readiness.md",
    "submission/claims_ledger.md",
    "submission/data_card.md",
    "submission/final_kaggle_writeup.md",
    "submission/kaggle_writeup_team_template.md",
    "submission/kaggle_writeup_review_draft.md",
    "submission/model_card.md",
    "submission/release_manifest.md",
    "submission/result_cards.md",
    "submission/figure_manifest.md",
    "submission/final_submission_checklist.md",
    "outputs/tables/model_comparison.csv",
    "outputs/tables/cross_validation_summary.csv",
    "outputs/tables/cleaning_sensitivity_metrics.csv",
    "outputs/tables/error_analysis_summary.csv",
    "outputs/tables/error_analysis_by_group.csv",
    "outputs/tables/selected_model_bootstrap_ci.csv",
    "outputs/tables/selected_model_bootstrap_distribution.csv",
    "outputs/tables/selected_model_threshold_analysis.csv",
    "outputs/tables/selected_model_threshold_summary.csv",
    "outputs/figures/cardio_systolic_bp_raw_vs_clean.png",
    "outputs/figures/cardio_target_by_bp_band.png",
    "outputs/figures/cleaning_sensitivity_auroc.png",
    "outputs/figures/model_comparison_auroc.png",
    "outputs/figures/calibration_curve.png",
    "outputs/figures/feature_importance.png",
    "outputs/figures/error_type_by_bp_band.png",
    "outputs/figures/selected_model_bootstrap_ci.png",
    "outputs/figures/selected_model_threshold_tradeoff.png",
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
    "outputs/tables/selected_model_bootstrap_ci.csv": {
        "dataset",
        "model",
        "split",
        "metric",
        "point_estimate",
        "ci_lower_95",
        "ci_upper_95",
        "bootstrap_iterations",
    },
    "outputs/tables/selected_model_bootstrap_distribution.csv": {
        "bootstrap_iteration",
        "metric",
        "value",
    },
    "outputs/tables/selected_model_threshold_analysis.csv": {
        "dataset",
        "model",
        "threshold",
        "precision",
        "sensitivity",
        "specificity",
        "f1",
        "tp",
        "tn",
        "fp",
        "fn",
    },
    "outputs/tables/selected_model_threshold_summary.csv": {
        "dataset",
        "model",
        "operating_point",
        "threshold",
        "precision",
        "sensitivity",
        "specificity",
        "f1",
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
    "outputs/figures/selected_model_bootstrap_ci.png",
    "outputs/figures/selected_model_threshold_tradeoff.png",
    "outputs/figures/selected_model_threshold_counts.png",
]

NOTEBOOK_REQUIREMENTS = {
    "notebooks/01_eda_and_baseline.ipynb": {"must_be_executed": False},
    "notebooks/02_final_kaggle_notebook.ipynb": {"must_be_executed": True},
}
ALLOW_UNEXECUTED_FINAL_NOTEBOOK = os.environ.get("BYTE2BEAT_ALLOW_UNEXECUTED_FINAL_NOTEBOOK") == "1"

PRIVATE_PATH_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"/private/(var|tmp)"),
    re.compile(r"Documents/Kaggle"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\"),
]

CLAIMS_LEDGER_PATH = ROOT / "submission/claims_ledger.md"
FINAL_WRITEUP_PATH = ROOT / "submission/final_kaggle_writeup.md"
WRITEUP_DRAFT_PATH = ROOT / "submission/kaggle_writeup_review_draft.md"
DATA_CARD_PATH = ROOT / "submission/data_card.md"
MODEL_CARD_PATH = ROOT / "submission/model_card.md"
CLAIM_ARTIFACT_PATTERN = re.compile(
    r"`((?:outputs|research|submission|paper|notebooks|scripts)/[^`]+)`"
)


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


def check_claims_ledger() -> list[str]:
    failures: list[str] = []
    if not CLAIMS_LEDGER_PATH.exists():
        return ["Missing claims ledger: submission/claims_ledger.md"]

    text = CLAIMS_LEDGER_PATH.read_text(encoding="utf-8")
    required_sections = [
        "## Supported Core Claims",
        "## Claims Requiring Extra Work",
        "## Required Final Review Questions",
    ]
    for section in required_sections:
        if section not in text:
            failures.append(f"claims_ledger.md is missing section: {section}")

    referenced_artifacts = sorted(set(CLAIM_ARTIFACT_PATTERN.findall(text)))
    for artifact in referenced_artifacts:
        if not (ROOT / artifact).exists():
            failures.append(f"claims_ledger.md references missing artifact: {artifact}")

    return failures


def check_writeup_draft() -> list[str]:
    failures: list[str] = []
    if not WRITEUP_DRAFT_PATH.exists():
        return ["Missing writeup draft: submission/kaggle_writeup_review_draft.md"]

    text = WRITEUP_DRAFT_PATH.read_text(encoding="utf-8")
    required_sections = [
        "## Executive Summary",
        "## Data Sources",
        "## Main Results",
        "## Uncertainty and Threshold Analysis",
        "## Cleaning Sensitivity",
        "## Error Analysis",
        "## Limitations",
        "## Reproducibility",
        "## Claim-to-Evidence Map",
        "## AI Usage Disclosure",
        "## Final Team Review Tasks",
    ]
    for section in required_sections:
        if section not in text:
            failures.append(
                f"kaggle_writeup_review_draft.md is missing section: {section}"
            )

    referenced_artifacts = sorted(set(CLAIM_ARTIFACT_PATTERN.findall(text)))
    for artifact in referenced_artifacts:
        if not (ROOT / artifact).exists():
            failures.append(
                "kaggle_writeup_review_draft.md references missing artifact: "
                f"{artifact}"
            )

    return failures


def check_final_writeup() -> list[str]:
    failures: list[str] = []
    if not FINAL_WRITEUP_PATH.exists():
        return ["Missing final writeup: submission/final_kaggle_writeup.md"]

    text = FINAL_WRITEUP_PATH.read_text(encoding="utf-8")
    required_sections = [
        "# From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It",
        "## A data-quality-first Byte2Beat workflow",
        "Author: Yaroslav Kholmirzayev",
        "Contact: yaric.kholm@gmail.com",
        "## Executive Summary",
        "## Data Sources",
        "## Main Results",
        "## Uncertainty and Threshold Analysis",
        "## Cleaning Sensitivity",
        "## Error Analysis",
        "## Limitations",
        "## Reproducibility",
        "## AI Usage Disclosure",
    ]
    for section in required_sections:
        if section not in text:
            failures.append(f"final_kaggle_writeup.md is missing: {section}")

    banned_fragments = ["[TEAM REVIEW]", "Status: review-ready scaffold"]
    for fragment in banned_fragments:
        if fragment in text:
            failures.append(f"final_kaggle_writeup.md contains placeholder: {fragment}")

    referenced_artifacts = sorted(set(CLAIM_ARTIFACT_PATTERN.findall(text)))
    for artifact in referenced_artifacts:
        if not (ROOT / artifact).exists():
            failures.append(
                f"final_kaggle_writeup.md references missing artifact: {artifact}"
            )

    return failures


def check_cards() -> list[str]:
    failures: list[str] = []
    card_requirements = {
        DATA_CARD_PATH: [
            "# Data Card",
            "## Data Sources",
            "## Unit of Analysis",
            "## Target",
            "## Known Data Quality Issues",
            "## Intended Use",
            "## Ethical and Publication Notes",
        ],
        MODEL_CARD_PATH: [
            "# Model Card",
            "## Model Type",
            "## Intended Use",
            "## Training and Evaluation Data",
            "## Performance",
            "## Robustness",
            "## Threshold Analysis",
            "## Failure Modes",
            "## Limitations",
        ],
    }
    for path, sections in card_requirements.items():
        if not path.exists():
            failures.append(f"Missing card: {_relative(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        for section in sections:
            if section not in text:
                failures.append(f"{_relative(path)} is missing section: {section}")
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

        if requirements["must_be_executed"] and not ALLOW_UNEXECUTED_FINAL_NOTEBOOK:
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
        ("claims ledger", check_claims_ledger),
        ("writeup draft", check_writeup_draft),
        ("final writeup", check_final_writeup),
        ("cards", check_cards),
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
