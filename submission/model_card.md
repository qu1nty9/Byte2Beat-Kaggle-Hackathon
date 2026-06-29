# Model Card

## Model Name

Histogram Gradient Boosting cardiovascular risk model

## Project

From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

## Author

Yaroslav Kholmirzayev

yaric.kholm@gmail.com

## Model Type

Selected model:

- `hist_gradient_boosting`

Reference models:

- Dummy prior baseline.
- Logistic regression.
- Depth-4 decision tree.
- Random forest.

## Intended Use

Appropriate:

- Educational risk-modeling analysis.
- Kaggle/Hack4Health reproducible notebook.
- Demonstrating why biomedical ML should include data audit, calibration, and error analysis.

Not appropriate:

- Diagnosis.
- Treatment decisions.
- Clinical triage.
- Real-world patient deployment.
- Causal interpretation of feature effects.

## Training and Evaluation Data

Primary dataset:

- Plausibility-cleaned `cardio_base.csv`.

Rows after current cleaning:

- 68,605.

Target:

- Binary `cardio` label.

Evaluation:

- Fixed stratified held-out test split.
- 5-fold stratified cross-validation.
- Cleaning sensitivity across raw, lenient, current, and strict profiles.

## Features

Feature set:

- Age in years.
- Gender coding as provided.
- Height.
- Weight.
- BMI.
- Systolic BP.
- Diastolic BP.
- Cholesterol category.
- Glucose category.
- Smoking indicator.
- Alcohol indicator.
- Activity indicator.

## Performance

Held-out test metrics for selected model:

| Metric | Value |
|---|---:|
| AUROC | 0.8037 |
| AUPRC | 0.7892 |
| Accuracy | 0.7355 |
| Brier score | 0.1795 |
| Sensitivity | 0.6876 |
| Specificity | 0.7825 |

Cross-validation:

- 5-fold CV AUROC: 0.8013 +/- 0.0025.

Model comparison:

- Random forest AUROC: 0.8024.
- Logistic regression AUROC: 0.7931.
- Dummy prior AUROC: 0.5000.

## Robustness

Held-out AUROC across cleaning profiles:

| Cleaning profile | HistGradientBoosting AUROC |
|---|---:|
| Raw | 0.8004 |
| Lenient | 0.8025 |
| Current | 0.8037 |
| Strict | 0.7991 |

Interpretation:

- The selected model remains near AUROC 0.80 across neighboring cleaning choices.
- Logistic regression is more sensitive to raw implausible values.
- Strict cleaning removes more data without improving performance.

## Interpretability

Main predictive factors:

- Systolic BP.
- Age.
- Cholesterol.
- BMI and related body measurements.

Interpretation caveat:

- Feature importance and coefficients are predictive associations, not causal effects.

## Failure Modes

Held-out confusion counts:

| Error type | Rows |
|---|---:|
| TN | 6,782 |
| FP | 1,885 |
| FN | 2,651 |
| TP | 5,834 |

Known asymmetric errors:

- In the `<120` systolic BP band, false-negative rate among positives is 0.8596.
- In the `>=140` systolic BP band, false-positive rate among negatives is 1.0000.
- Cholesterol category `3` has false-positive rate 0.8508 among negatives.

Practical implication:

- The model can miss lower-BP positives and overcall high-risk-looking negatives.

## Limitations

- No external clinical validation.
- Public dataset representativeness is unknown.
- Target definition is dataset-specific.
- Calibration is internal only.
- Subgroup analysis is limited by available variables.
- Model is not suitable for clinical deployment.

## Reproducibility

Core commands:

```bash
make setup
make all
make check
make submission-check
```

Primary code and evidence:

- `scripts/model_comparison.py`
- `scripts/cleaning_sensitivity.py`
- `scripts/error_analysis.py`
- `notebooks/02_final_kaggle_notebook.ipynb`
- `outputs/tables/model_comparison.csv`
- `outputs/tables/cross_validation_summary.csv`
- `outputs/tables/cleaning_sensitivity_metrics.csv`
- `outputs/tables/error_analysis_by_group.csv`
