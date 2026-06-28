# Baseline Results

First baseline generated on 2026-06-28 with `scripts/baseline_tabular_numpy.py`.

## Method

The baseline uses a self-contained logistic regression implementation in numpy so the project has a reproducible reference before adding heavier dependencies.

Shared setup:

- Fixed seed: 42.
- Stratified train/validation/test split: 70% / 15% / 15%.
- Standardization fit on train only.
- Metrics: AUROC, accuracy, Brier score, log loss, sensitivity, specificity.

## Cardiac Failure Baseline

Input: `cardio_base.csv` after the initial plausibility filter described in `research/data_audit.md`.

Features:

- Age in years, gender, height, weight, BMI, systolic BP, diastolic BP, cholesterol, glucose, smoking, alcohol, activity.

Held-out test result:

- Rows: 10,293.
- AUROC: 0.7974.
- Accuracy: 0.7359.
- Brier score: 0.1851.
- Sensitivity: 0.6720.
- Specificity: 0.7985.

Largest standardized coefficients:

- `ap_hi`: +0.8045.
- `age_years`: +0.3346.
- `cholesterol`: +0.3241.
- `ap_lo`: +0.1749.
- `weight`: +0.0850.
- `active`: -0.0799.

Interpretation: the first model is clinically plausible and already writeup-worthy as a transparent baseline. Next steps are calibration curves, cross-validation, and comparison to tree/boosting models.

## Heart Attack Baseline

Input: `heart_processed.csv`, with an added `Cholesterol_zero` indicator.

Held-out test result:

- Rows: 139.
- AUROC: 0.9411.
- Accuracy: 0.8705.
- Brier score: 0.0904.
- Sensitivity: 0.8701.
- Specificity: 0.8710.

Largest standardized coefficients:

- `ST_Slope_Flat`: +0.6369.
- `Sex_M`: +0.6158.
- `ChestPainType_NAP`: -0.5825.
- `ST_Slope_Up`: -0.5574.
- `ChestPainType_ATA`: -0.5536.
- `Cholesterol_zero`: +0.5122.

Interpretation: this result is promising but high-variance because the dataset has only 918 rows. The `Cholesterol_zero` coefficient is a warning that missing-like values carry target information and need careful explanation.

## Immediate Model Improvements

1. Add repeated cross-validation for the heart dataset.
2. Add calibration tables and reliability plots.
3. Add sklearn baselines once dependencies are installed: regularized logistic regression, random forest, gradient boosting.
4. Compare raw vs cleaned cardiac inputs to quantify whether cleaning improves generalization or mainly improves validity.
5. Add subgroup metrics and false-positive/false-negative analysis.

## Sklearn Model Comparison

Generated with `scripts/model_comparison.py`.

Main cardiac input: plausibility-cleaned `cardio_base.csv`.

Held-out cardiac test metrics:

| Model | AUROC | AUPRC | Accuracy | Brier |
|---|---:|---:|---:|---:|
| HistGradientBoosting | 0.8037 | 0.7892 | 0.7355 | 0.1795 |
| Random forest | 0.8024 | 0.7875 | 0.7355 | 0.1801 |
| Logistic regression | 0.7931 | 0.7750 | 0.7267 | 0.1863 |
| Depth-4 decision tree | 0.7876 | 0.7598 | 0.7296 | 0.1844 |
| Dummy prior | 0.5000 | 0.4947 | 0.5053 | 0.2500 |

5-fold cross-validation on cardiac data:

- HistGradientBoosting AUROC: 0.8013 +/- 0.0025.
- Random forest AUROC: 0.8007 +/- 0.0025.
- Logistic regression AUROC: 0.7912 +/- 0.0026.
- Depth-4 decision tree AUROC: 0.7864 +/- 0.0033.

Interpretation: boosting and random forest improve AUROC by about 0.01 over logistic regression, but the improvement is modest. This supports a final story centered on data quality, calibration, and interpretability rather than model complexity alone.

Generated artifacts:

- `outputs/tables/model_comparison.csv`
- `outputs/tables/cross_validation_summary.csv`
- `outputs/tables/cardio_clean_calibration_bins.csv`
- `outputs/tables/subgroup_metrics.csv`
- `outputs/tables/feature_importance.csv`
- `outputs/figures/model_comparison_auroc.png`
- `outputs/figures/roc_curves.png`
- `outputs/figures/pr_curves.png`
- `outputs/figures/calibration_curve.png`
- `outputs/figures/feature_importance.png`

## Cleaning Sensitivity

Generated with `scripts/cleaning_sensitivity.py`.

Profiles:

- `raw`: no plausibility filtering.
- `lenient`: broad plausibility rules.
- `current`: primary cleaning profile.
- `strict`: stricter robustness profile.

Rows retained:

| Profile | Rows | Removed fraction | Target rate |
|---|---:|---:|---:|
| Raw | 70,000 | 0.0000 | 0.4997 |
| Lenient | 68,644 | 0.0194 | 0.4947 |
| Current | 68,605 | 0.0199 | 0.4947 |
| Strict | 68,362 | 0.0234 | 0.4950 |

Held-out AUROC:

| Profile | Logistic regression | HistGradientBoosting |
|---|---:|---:|
| Raw | 0.7776 | 0.8004 |
| Lenient | 0.7917 | 0.8025 |
| Current | 0.7931 | 0.8037 |
| Strict | 0.7891 | 0.7991 |

Interpretation: the raw outliers meaningfully hurt logistic regression, but the boosting model remains stable around AUROC 0.80. The current profile gives the best held-out AUROC and Brier score for the selected model, while strict filtering removes more data without improving performance.

Generated artifacts:

- `outputs/tables/cleaning_sensitivity_summary.csv`
- `outputs/tables/cleaning_sensitivity_metrics.csv`
- `outputs/tables/cleaning_sensitivity_cv.csv`
- `outputs/figures/cleaning_sensitivity_rows.png`
- `outputs/figures/cleaning_sensitivity_auroc.png`
- `outputs/figures/cleaning_sensitivity_brier.png`
