# Kaggle Writeup Team Template

Use this as a structure and evidence map. Rewrite the final prose in the team's own words before submission.

## Title

Suggested title: From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

## Subtitle

Suggested subtitle: A data-quality-first Byte2Beat workflow where plausibility checks, calibration, and failure-mode analysis matter as much as AUROC.

## 1. Problem Framing

Team-written text should explain:

- Why cardiovascular risk prediction matters.
- Why public biomedical data quality matters.
- Why the project focuses on reliable risk modeling rather than only leaderboard-style model score.

Evidence to cite:

- Competition focus on cardiovascular AI and interpretability.
- Data audit findings in `research/data_audit.md`.

## 2. Data Sources and Ethics

Include:

- `cardio_base.csv` as primary dataset.
- `heart_processed.csv` as comparison dataset.
- `ecg_timeseries.csv` as gated extension, not headline model.
- Statement that this is educational/research only, not clinical advice.

Evidence:

- `outputs/tables/data_audit.json`
- `outputs/tables/ecg_schema_audit.json`
- `docs/DATA.md`

## 3. Data Audit

Core points:

- Primary cardiac dataset has 70,000 rows and nearly balanced `cardio` target.
- Blood pressure and body-measurement anomalies exist.
- Processed cardiac file still retains blood-pressure anomalies.
- Heart dataset has 172 zero cholesterol values, likely missing-like and target-associated.
- ECG schema is not yet suitable for a supervised headline result.

Figures/tables:

- `outputs/tables/cardio_cleaning_impact.csv`
- `outputs/tables/heart_cleaning_impact.csv`
- `outputs/tables/ecg_schema_audit.json`

## 4. Cleaning and Sensitivity Analysis

Core points:

- Current plausibility filter removes 1,395 rows, or 1.99%.
- Neighboring cleaning profiles retain similar target rates.
- Raw implausible values hurt logistic regression more than boosting.
- Boosting remains stable around AUROC 0.80 across cleaning profiles.

Figures/tables:

- `outputs/figures/cardio_cleaning_flow.png`
- `outputs/figures/cardio_systolic_bp_raw_vs_clean.png`
- `outputs/figures/cleaning_sensitivity_rows.png`
- `outputs/figures/cleaning_sensitivity_auroc.png`
- `outputs/figures/cleaning_sensitivity_brier.png`

## 5. EDA Findings

Core points:

- Cardio-positive rate rises sharply with systolic BP band:
  - `<120`: 23.0%.
  - `120-129`: 35.6%.
  - `130-139`: 59.9%.
  - `>=140`: 83.7%.
- This validates that the target aligns with recognizable cardiovascular risk structure.

Figures/tables:

- `outputs/figures/cardio_target_by_bp_band.png`
- `outputs/figures/cardio_target_by_age_band.png`
- `outputs/figures/cardio_age_distribution_by_target.png`

## 6. Modeling Methods

Models:

- Dummy prior baseline.
- Logistic regression.
- Depth-4 decision tree.
- Random forest.
- Histogram gradient boosting.

Metrics:

- AUROC.
- AUPRC.
- Accuracy.
- F1.
- Brier score.
- Log loss.
- Sensitivity and specificity.
- Calibration bins.
- Subgroup/error analysis.

Figures/tables:

- `outputs/tables/model_comparison.csv`
- `outputs/tables/cross_validation_summary.csv`

## 7. Main Results

Current selected model:

- `hist_gradient_boosting`
- Held-out test AUROC: 0.8037.
- Held-out test AUPRC: 0.7892.
- Held-out test accuracy: 0.7355.
- Held-out test Brier score: 0.1795.
- 5-fold CV AUROC: 0.8013 +/- 0.0025.

Comparison:

- Random forest test AUROC: 0.8024.
- Logistic regression test AUROC: 0.7931.
- Dummy prior AUROC: 0.5000.

Figures:

- `outputs/figures/model_comparison_auroc.png`
- `outputs/figures/roc_curves.png`
- `outputs/figures/pr_curves.png`
- `outputs/figures/calibration_curve.png`

## 8. Interpretability

Core points:

- Logistic baseline is clinically plausible: systolic BP, age, cholesterol, and diastolic BP are major effects.
- Permutation importance from selected model should be interpreted as predictive association, not causality.

Figures/tables:

- `outputs/tables/cardio_logreg_coefficients.csv`
- `outputs/tables/feature_importance.csv`
- `outputs/figures/feature_importance.png`

## 9. Error Analysis

Core points:

- The selected model is asymmetric.
- It misses many actual positives in low systolic BP bands.
- It overcalls the minority of high-BP/high-cholesterol negatives.
- This is clinically intuitive but important as a limitation.

Key numbers:

- TN: 6,782.
- FP: 1,885.
- FN: 2,651.
- TP: 5,834.
- `<120` BP band false-negative rate among positives: 0.8596.
- `>=140` BP band false-positive rate among negatives: 1.0000.

Figures/tables:

- `outputs/figures/error_confusion_matrix.png`
- `outputs/figures/error_prediction_distribution.png`
- `outputs/figures/error_type_by_bp_band.png`
- `outputs/figures/error_type_by_age_band.png`
- `outputs/figures/error_type_by_cholesterol.png`
- `outputs/tables/error_analysis_summary.csv`
- `outputs/tables/error_analysis_by_group.csv`

## 10. What Did Not Work

Include:

- ECG was not used as headline result because schema/labels are unclear.
- Heart dataset gives high AUROC but is small and high-variance.
- More complex models only modestly outperform logistic regression.
- Strict cleaning removes more data without improving performance.

## 11. Limitations

Include:

- Dataset-specific targets.
- Public dataset representativeness limits.
- Predictive association is not causation.
- No deployment or medical decision claims.
- Model is educational/research only.
- Subgroup errors remain meaningful.

## 12. Reproducibility

Commands:

```bash
make setup
make all
make check
```

Notebook:

- Preferred public notebook: `notebooks/02_final_kaggle_notebook.ipynb`.
- Working reproducibility notebook: `notebooks/01_eda_and_baseline.ipynb`.

## 13. AI Usage Disclosure

Use/adapt `research/ai_usage_disclosure.md`.

The team should state actual AI use honestly and ensure final written submission is authored/reviewed by the team.
