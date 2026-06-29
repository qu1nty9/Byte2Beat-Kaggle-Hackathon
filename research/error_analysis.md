# Error Analysis

Generated on 2026-06-29 with `scripts/error_analysis.py`.

## Setup

Dataset:

- Current plausibility-cleaned `cardio_base.csv`.

Model:

- `hist_gradient_boosting`, matching the current selected cardiac model from `scripts/model_comparison.py`.

Split:

- Stratified 75/25 train/test split with seed 42.

## Confusion Summary

Held-out test rows: 17,152.

| Prediction type | Rows | Share | Mean predicted risk | Mean age | Mean systolic BP | Mean cholesterol |
|---|---:|---:|---:|---:|---:|---:|
| TN | 6,782 | 0.3954 | 0.2687 | 50.44 | 115.78 | 1.11 |
| FP | 1,885 | 0.1099 | 0.6872 | 56.68 | 133.42 | 1.59 |
| FN | 2,651 | 0.1546 | 0.3336 | 52.93 | 118.13 | 1.17 |
| TP | 5,834 | 0.3401 | 0.7685 | 55.83 | 141.22 | 1.67 |

## Main Failure Modes

### Low-BP false negatives

In the `<120` systolic BP band:

- Rows: 3,050.
- Positive rate: 0.2266.
- False-negative rate among positives: 0.8596.
- False-positive rate among negatives: 0.0246.

Interpretation: the model often treats low systolic BP as a strong negative signal, so actual positives with low BP are easily missed.

### High-BP false positives

In the `>=140` systolic BP band:

- Rows: 4,578.
- Positive rate: 0.8432.
- Predicted positive rate: 1.0000.
- False-positive rate among negatives: 1.0000.
- False-negative rate among positives: 0.0000.

Interpretation: high systolic BP dominates the model's risk estimate. This produces excellent sensitivity in this band but no specificity among the minority of high-BP negatives.

### Cholesterol category effects

For cholesterol category `3`:

- Rows: 1,914.
- Positive rate: 0.7654.
- Predicted positive rate: 0.9373.
- False-positive rate among negatives: 0.8508.
- False-negative rate among positives: 0.0362.

Interpretation: high cholesterol pushes the model strongly toward positive predictions, similar to high systolic BP.

## Writeup Implication

The model is useful as a risk stratification demonstration, but it is not clinically neutral across subgroups. It leans heavily on classic risk signals such as systolic BP and cholesterol. This makes the model intuitive, but creates asymmetric errors:

- Lower-risk-looking positives are missed.
- High-risk-looking negatives are overcalled.

This is a good limitation to discuss in the Kaggle Writeup because it shows model behavior rather than only reporting aggregate AUROC.

## Generated Artifacts

- `outputs/tables/error_analysis_predictions.csv`
- `outputs/tables/error_analysis_summary.csv`
- `outputs/tables/error_analysis_by_group.csv`
- `outputs/tables/error_type_by_group.csv`
- `outputs/tables/error_high_confidence_examples.csv`
- `outputs/figures/error_confusion_matrix.png`
- `outputs/figures/error_prediction_distribution.png`
- `outputs/figures/error_type_by_bp_band.png`
- `outputs/figures/error_type_by_age_band.png`
- `outputs/figures/error_type_by_cholesterol.png`

