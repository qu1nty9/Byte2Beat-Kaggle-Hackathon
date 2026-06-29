# Claims Ledger

Use this file as the final review map before writing or publishing. It separates claims that are supported by current evidence from claims that would overstate the project.

The final Kaggle Writeup should be reviewed and approved by the author. This ledger is an evidence and guardrail artifact, not final prose to copy verbatim.

## Supported Core Claims

| Claim | Evidence | Confidence | Safe wording | Avoid saying |
|---|---|---|---|---|
| The primary cardiac dataset is large and nearly balanced. | `outputs/tables/data_audit.json`, `submission/result_cards.md` | High | The primary tabular cardiac dataset has 70,000 rows and an approximately balanced target. | The dataset represents a clinical population. |
| Transparent plausibility checks remove a small fraction of rows. | `outputs/tables/cardio_cleaning_impact.csv`, `outputs/figures/cardio_cleaning_flow.png` | High | The current plausibility filter removes 1,395 rows, or about 1.99% of the primary dataset. | Cleaning proves the remaining rows are clinically valid. |
| Raw blood-pressure values contain implausible artifacts. | `outputs/figures/cardio_systolic_bp_raw_vs_clean.png`, `research/data_audit.md` | High | The raw data contain implausible blood-pressure values, so the project uses explicit plausibility checks. | The raw dataset is unusable. |
| Cardio-positive rate rises sharply with systolic BP band. | `outputs/tables/cardio_target_by_bp_band.csv`, `outputs/figures/cardio_target_by_bp_band.png` | High | Observed target prevalence increases from about 23% in the `<120` systolic BP band to about 84% in the `>=140` band. | The plot proves a causal blood-pressure effect. |
| The selected model is stable around AUROC 0.80 across plausible cleaning profiles. | `outputs/tables/cleaning_sensitivity_metrics.csv`, `outputs/figures/cleaning_sensitivity_auroc.png` | High | Histogram gradient boosting remains near AUROC 0.80 across raw, lenient, current, and strict cleaning profiles. | Cleaning choices do not matter at all. |
| Implausible raw values affect logistic regression more than boosting. | `outputs/tables/cleaning_sensitivity_metrics.csv`, `research/baseline_results.md` | Medium | Logistic regression improves more after plausibility filtering than the selected boosting model. | Boosting is immune to data quality problems. |
| The selected model modestly outperforms logistic regression. | `outputs/tables/model_comparison.csv`, `outputs/figures/model_comparison_auroc.png` | High | Histogram gradient boosting and random forest are slightly ahead of logistic regression, but the gain is modest. | Complex models are necessary for this problem. |
| The selected model's headline held-out AUROC is 0.8037. | `outputs/tables/cardio_clean_test_model_metrics.csv`, `outputs/tables/model_comparison.csv` | High | On the held-out split, the selected model reaches AUROC 0.8037 and AUPRC 0.7892. | The model is clinically accurate enough for use. |
| Cross-validation supports the held-out result. | `outputs/tables/cross_validation_summary.csv` | High | Five-fold CV gives AUROC 0.8013 +/- 0.0025 for the selected model. | The model will generalize to all clinical settings. |
| Bootstrap intervals quantify held-out metric uncertainty. | `outputs/tables/selected_model_bootstrap_ci.csv`, `outputs/figures/selected_model_bootstrap_ci.png` | High | Bootstrap resampling gives a 95% AUROC interval of 0.7970-0.8103 and AUPRC interval of 0.7796-0.7990 on the held-out predictions. | The true clinical AUROC is guaranteed to lie in this range. |
| Threshold choice materially changes false-positive and false-negative trade-offs. | `outputs/tables/selected_model_threshold_summary.csv`, `outputs/figures/selected_model_threshold_tradeoff.png` | High | Lowering the threshold to 0.35 raises sensitivity to 0.8329 but increases false positives to 3,623; raising it to 0.55 increases specificity to 0.8215 but raises false negatives to 3,011. | We have identified the clinically optimal threshold. |
| Calibration and Brier score are part of the evaluation, not afterthoughts. | `outputs/tables/cardio_clean_calibration_bins.csv`, `outputs/figures/calibration_curve.png`, `outputs/tables/model_comparison.csv` | High | The evaluation includes discrimination, calibration bins, Brier score, and log loss. | The model is perfectly calibrated. |
| The model relies on recognizable cardiovascular risk factors. | `outputs/tables/feature_importance.csv`, `outputs/tables/cardio_logreg_coefficients.csv`, `outputs/figures/feature_importance.png` | Medium | Feature importance and logistic coefficients point to systolic BP, age, cholesterol, and related risk factors. | Feature importance proves clinical causality. |
| Error analysis reveals asymmetric failure modes. | `outputs/tables/error_analysis_summary.csv`, `outputs/tables/error_analysis_by_group.csv`, `outputs/figures/error_type_by_bp_band.png` | High | The model misses many lower-BP positives and overcalls some high-risk-looking negatives. | The model is fair or reliable across all subgroups. |
| ECG is intentionally gated out of the headline result. | `outputs/tables/ecg_schema_audit.json`, `research/data_audit.md` | High | ECG is treated as an extension because row semantics, labels, and schema need validation before supervised claims. | The ECG data were modeled successfully. |
| The project is reproducible from scripts and notebooks. | `Makefile`, `notebooks/02_final_kaggle_notebook.ipynb`, `scripts/check_submission_assets.py` | High | The repository includes scripts, generated tables/figures, a public notebook, and a submission quality gate. | Reproducibility is guaranteed on every external machine without checking data paths. |

## Claims Requiring Extra Work

| Claim | Missing evidence | Required next step |
|---|---|---|
| The workflow is robust across multiple public cardiovascular datasets. | Stronger repeated CV and deeper discussion for the small heart dataset. | Add repeated CV/bootstrap intervals and a conservative comparison section. |
| The project is publication-ready as a preprint. | Related work, dataset license confirmation, organizer notification, and stronger external validity discussion. | Complete `paper/publication_readiness.md` and verify publication requirements. |
| The model is suitable for a deployed educational demo. | Demo UX, disclaimers, and model-card style caveats. | Build a demo only after final Kaggle materials are stable. |
| The ECG file can improve prediction. | Valid labels, row semantics, lead/timepoint mapping, and linkage. | Resolve ECG provenance and create a gated ECG appendix. |

## Required Final Review Questions

- Does every numeric claim map to a generated table or figure?
- Are all medical claims phrased as predictive associations, not causal or diagnostic statements?
- Does the writeup state that the model is educational/research only?
- Does the AI usage disclosure match the author's actual workflow?
- Does `make submission-check` pass after the final notebook and writeup are updated?
- Has the team checked Hack4Health publication/visibility requirements before any non-Kaggle publication?
