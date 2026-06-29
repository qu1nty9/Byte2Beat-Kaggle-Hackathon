# Result Cards

Use these as evidence cards while writing the Kaggle submission.

## Data Audit Card

- Primary cardiac dataset: 70,000 rows.
- Target balance: 35,021 negative, 34,979 positive.
- Current plausibility filter removes 1,395 rows, or 1.99%.
- Heart dataset: 918 rows; `Cholesterol == 0` in 172 rows.
- ECG dataset: 528 rows, 123,995 columns, 36,441 duplicate non-empty header names.

## EDA Card

Cardio-positive rate by systolic BP band after current cleaning:

| Systolic BP band | Observed cardio-positive rate |
|---|---:|
| `<120` | 0.2305 |
| `120-129` | 0.3560 |
| `130-139` | 0.5985 |
| `>=140` | 0.8370 |

## Main Model Card

Selected cardiac model: `hist_gradient_boosting`.

| Metric | Value |
|---|---:|
| Test AUROC | 0.8037 |
| Test AUPRC | 0.7892 |
| Test accuracy | 0.7355 |
| Test Brier score | 0.1795 |
| 5-fold CV AUROC | 0.8013 +/- 0.0025 |

Bootstrap 95% intervals:

| Metric | 95% interval |
|---|---:|
| AUROC | 0.7970-0.8103 |
| AUPRC | 0.7796-0.7990 |
| Accuracy | 0.7290-0.7425 |
| Brier score | 0.1765-0.1825 |

## Model Comparison Card

Held-out test AUROC on current cleaned cardiac data:

| Model | AUROC |
|---|---:|
| Dummy prior | 0.5000 |
| Logistic regression | 0.7931 |
| Decision tree depth 4 | 0.7876 |
| Random forest | 0.8024 |
| Histogram gradient boosting | 0.8037 |

## Cleaning Sensitivity Card

Held-out AUROC:

| Cleaning profile | Logistic regression | HistGradientBoosting |
|---|---:|---:|
| Raw | 0.7776 | 0.8004 |
| Lenient | 0.7917 | 0.8025 |
| Current | 0.7931 | 0.8037 |
| Strict | 0.7891 | 0.7991 |

## Error Analysis Card

Confusion counts:

| Type | Rows |
|---|---:|
| TN | 6,782 |
| FP | 1,885 |
| FN | 2,651 |
| TP | 5,834 |

Failure modes:

- `<120` systolic BP band: false-negative rate among positives is 0.8596.
- `>=140` systolic BP band: false-positive rate among negatives is 1.0000.
- Cholesterol category `3`: false-positive rate among negatives is 0.8508.

## Threshold Card

Selected operating points:

| Operating point | Threshold | Sensitivity | Specificity | FP | FN |
|---|---:|---:|---:|---:|---:|
| Default | 0.50 | 0.6876 | 0.7825 | 1,885 | 2,651 |
| Max F1 / sensitivity >= 0.80 | 0.35 | 0.8329 | 0.5820 | 3,623 | 1,418 |
| Specificity >= 0.80 | 0.55 | 0.6451 | 0.8215 | 1,547 | 3,011 |
