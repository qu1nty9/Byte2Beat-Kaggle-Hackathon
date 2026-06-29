# Uncertainty and Threshold Analysis

Generated on 2026-06-30 with `scripts/uncertainty_threshold_analysis.py`.

## Research Question

How stable are the selected cardiac model's held-out metrics, and how do false positives and false negatives change when the decision threshold changes?

## Input

Exact input file:

- `outputs/tables/cardio_clean_test_predictions.csv`

Target:

- `cardio`

Score:

- `hist_gradient_boosting`

Unit of analysis:

- One held-out cardiac test row.

## Method

Bootstrap uncertainty:

- 2,000 bootstrap resamples of the held-out prediction table.
- Metrics: AUROC, AUPRC, accuracy, Brier score, sensitivity, specificity.
- Confidence interval: percentile 2.5% and 97.5%.

Threshold analysis:

- Threshold grid from 0.10 to 0.90 in 0.05 increments.
- Metrics: predicted-positive rate, accuracy, precision, sensitivity, specificity, F1, TP, TN, FP, FN.
- Summary operating points: default threshold 0.50, max F1, sensitivity at least 0.80 with lowest false positives, and specificity at least 0.80 with lowest false negatives.

## Main Results

Bootstrap 95% intervals:

| Metric | Point estimate | 95% interval |
|---|---:|---:|
| AUROC | 0.8037 | 0.7970-0.8103 |
| AUPRC | 0.7892 | 0.7796-0.7990 |
| Accuracy | 0.7355 | 0.7290-0.7425 |
| Brier score | 0.1795 | 0.1765-0.1825 |
| Sensitivity | 0.6876 | 0.6778-0.6975 |
| Specificity | 0.7825 | 0.7740-0.7916 |

Selected threshold trade-offs:

| Operating point | Threshold | Sensitivity | Specificity | Precision | F1 | FP | FN |
|---|---:|---:|---:|---:|---:|---:|---:|
| Default | 0.50 | 0.6876 | 0.7825 | 0.7558 | 0.7201 | 1,885 | 2,651 |
| Max F1 / sensitivity >= 0.80 | 0.35 | 0.8329 | 0.5820 | 0.6611 | 0.7371 | 3,623 | 1,418 |
| Specificity >= 0.80 | 0.55 | 0.6451 | 0.8215 | 0.7797 | 0.7060 | 1,547 | 3,011 |

## Interpretation

The selected model's held-out discrimination metrics have narrow bootstrap intervals, supporting the stability of the aggregate test result on this split.

Threshold choice materially changes the model's behavior. Lowering the threshold from 0.50 to 0.35 reduces false negatives by 1,233 but adds 1,738 false positives. Raising the threshold from 0.50 to 0.55 removes 338 false positives but adds 360 false negatives.

This should be described as an operating-point trade-off, not as an optimized clinical recommendation.

## Limitations

- Bootstrap intervals quantify uncertainty on the held-out prediction table, not external clinical generalization.
- Threshold analysis is illustrative because no clinical cost matrix or deployment context is defined.
- The same public-data limitations from `research/data_audit.md` still apply.

## Artifacts

Tables:

- `outputs/tables/selected_model_bootstrap_ci.csv`
- `outputs/tables/selected_model_bootstrap_distribution.csv`
- `outputs/tables/selected_model_threshold_analysis.csv`
- `outputs/tables/selected_model_threshold_summary.csv`

Figures:

- `outputs/figures/selected_model_bootstrap_ci.png`
- `outputs/figures/selected_model_threshold_tradeoff.png`
- `outputs/figures/selected_model_threshold_counts.png`
