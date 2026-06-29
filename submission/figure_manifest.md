# Figure Manifest

Use this to decide which figures enter the Kaggle Writeup and public notebook.

| Figure | Use in writeup | Main claim |
|---|---|---|
| `outputs/figures/cardio_cleaning_flow.png` | Data audit / cleaning | Current cleaning removes a small, transparent subset of rows. |
| `outputs/figures/cardio_systolic_bp_raw_vs_clean.png` | Data audit | Raw systolic BP contains implausible values; cleaning produces a credible distribution. |
| `outputs/figures/cardio_target_by_bp_band.png` | EDA | Cardio-positive rate increases sharply with systolic BP band. |
| `outputs/figures/cardio_target_by_age_band.png` | EDA | Age band has visible target-rate structure. |
| `outputs/figures/cleaning_sensitivity_rows.png` | Robustness | Neighboring cleaning profiles retain similar row counts. |
| `outputs/figures/cleaning_sensitivity_auroc.png` | Robustness | Selected model performance is stable across cleaning profiles. |
| `outputs/figures/cleaning_sensitivity_brier.png` | Robustness | Calibration-quality proxy remains similar across profiles. |
| `outputs/figures/model_comparison_auroc.png` | Results | Boosting/random forest modestly outperform logistic regression. |
| `outputs/figures/roc_curves.png` | Results | All non-dummy models rank risk above baseline. |
| `outputs/figures/pr_curves.png` | Results | Precision-recall performance supports the same model ranking. |
| `outputs/figures/selected_model_bootstrap_ci.png` | Uncertainty | Held-out metrics have narrow bootstrap 95% intervals. |
| `outputs/figures/selected_model_threshold_tradeoff.png` | Threshold analysis | Sensitivity, specificity, precision, and F1 shift materially with the decision threshold. |
| `outputs/figures/selected_model_threshold_counts.png` | Threshold analysis | False-positive and false-negative counts trade off across thresholds. |
| `outputs/figures/calibration_curve.png` | Calibration | Selected model is reasonably calibrated in decile bins. |
| `outputs/figures/feature_importance.png` | Interpretability | Predictive signal is dominated by recognizable cardiovascular factors. |
| `outputs/figures/error_confusion_matrix.png` | Error analysis | Aggregate errors are balanced enough to inspect further. |
| `outputs/figures/error_prediction_distribution.png` | Error analysis | Risk predictions separate classes but overlap meaningfully. |
| `outputs/figures/error_type_by_bp_band.png` | Error analysis | BP bands show asymmetric false-negative/false-positive behavior. |
| `outputs/figures/error_type_by_age_band.png` | Error analysis | Error composition changes across age bands. |
| `outputs/figures/error_type_by_cholesterol.png` | Error analysis | High cholesterol categories drive positive predictions and false positives. |

Recommended final writeup set if space is limited:

1. `cardio_systolic_bp_raw_vs_clean.png`
2. `cardio_target_by_bp_band.png`
3. `cleaning_sensitivity_auroc.png`
4. `model_comparison_auroc.png`
5. `selected_model_bootstrap_ci.png`
6. `selected_model_threshold_tradeoff.png`
7. `calibration_curve.png`
8. `feature_importance.png`
9. `error_type_by_bp_band.png`
