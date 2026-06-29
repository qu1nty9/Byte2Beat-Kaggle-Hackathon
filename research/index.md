# Research Index

## Core Pages

- [Project Plan](project_plan.md): canonical operating plan for the ideal Kaggle project, repository, writeup, and publication path.
- [Source Inventory](source_inventory.md): competition documents, provided datasets, and provenance notes.
- [Data Audit](data_audit.md): initial dataset profile and data-quality risks.
- [Baseline Results](baseline_results.md): first self-contained tabular logistic-regression baseline.
- [Error Analysis](error_analysis.md): false positive/false negative analysis for the selected cardiac model.
- [Kaggle Writeup Draft](kaggle_writeup_draft.md): working draft for the final public Kaggle submission narrative.
- [AI Usage Disclosure](ai_usage_disclosure.md): draft disclosure aligned with competition policy.
- [Log](log.md): chronological record of work.

## Generated Artifacts

- `outputs/tables/data_audit.json`: machine-readable output from `scripts/profile_data.py`.
- `outputs/tables/cardio_cleaning_impact.csv`: impact of initial plausibility filters.
- `outputs/tables/heart_cleaning_impact.csv`: impact of initial missing-like value filters.
- `outputs/tables/baseline_metrics.csv`: first logistic-regression baseline metrics.
- `outputs/tables/cardio_logreg_coefficients.csv`: standardized coefficients for the cardiac failure baseline.
- `outputs/tables/heart_logreg_coefficients.csv`: standardized coefficients for the heart attack baseline.
- `outputs/tables/model_comparison.csv`: sklearn model comparison across cardiac and heart datasets.
- `outputs/tables/cross_validation_summary.csv`: 5-fold CV summary.
- `outputs/tables/cleaning_sensitivity_metrics.csv`: raw/lenient/current/strict cleaning sensitivity metrics.
- `outputs/tables/cleaning_sensitivity_cv.csv`: cross-validation summary for cleaning sensitivity profiles.
- `outputs/tables/subgroup_metrics.csv`: subgroup metrics for selected cardiac model.
- `outputs/tables/error_analysis_summary.csv`: confusion-type summary for the selected cardiac model.
- `outputs/tables/error_analysis_by_group.csv`: false-positive/false-negative rates by clinical groups.
- `outputs/tables/ecg_schema_audit.json`: lightweight schema audit for the large ECG CSV.
- `outputs/figures/`: writeup-ready EDA, ROC/PR, calibration, and feature-importance figures.

## Current Decision Snapshot

- Lead direction: start with an interpretable cardiovascular risk modeling project on the tabular datasets, with ECG feature extraction as a novelty extension if labels and structure can be validated.
- Primary deliverable: public Kaggle Writeup plus public reproducible notebook.
- Secondary deliverable: article/preprint-style manuscript draft if results are strong enough and organizers are notified before public release.
