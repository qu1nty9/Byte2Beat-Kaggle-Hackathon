from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ASSETS = [
    "README.md",
    "requirements.txt",
    "Makefile",
    "notebooks/01_eda_and_baseline.ipynb",
    "notebooks/02_final_kaggle_notebook.ipynb",
    "research/kaggle_writeup_draft.md",
    "research/ai_usage_disclosure.md",
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


def main() -> None:
    missing = [asset for asset in REQUIRED_ASSETS if not (ROOT / asset).exists()]
    if missing:
        print("Missing submission assets:")
        for asset in missing:
            print(f"- {asset}")
        raise SystemExit(1)
    print(f"All {len(REQUIRED_ASSETS)} submission assets are present.")


if __name__ == "__main__":
    main()
