# Publication Readiness

This file tracks what must be true before turning the Kaggle project into a blog post, arXiv-style preprint, workshop submission, or journal article.

## Current Status

Status: not publication-ready yet.

The project is close to a strong Kaggle submission because it has a reproducible pipeline, a public notebook, generated figures, sensitivity analysis, calibration reporting, and error analysis. A publication requires a higher evidence standard: verified dataset provenance, related work, stronger external-validity discussion, and explicit publication coordination with Hack4Health organizers.

## Candidate Contribution

Working contribution:

> A reproducible, data-quality-aware workflow for public cardiovascular risk modeling that combines plausibility checks, cleaning sensitivity, calibration, interpretability, and subgroup error analysis.

This contribution is methodological and educational. It should not be framed as a new clinical risk score or a deployable medical device.

## Publication Options

| Option | Readiness | Best use | Extra work |
|---|---|---|---|
| Kaggle Writeup | High | Competition submission and project explanation. | Team-authored final prose and final checklist review. |
| GitHub release | Medium-high | Reproducible project archive. | Confirm repository visibility, data access notes, and release tag. |
| Blog/article | Medium | Accessible explanation of data-quality lessons. | Add clearer narrative, limitations, and selected visuals. |
| arXiv-style preprint | Medium-low | Formal methods/results writeup. | Add related work, citations, license verification, stronger robustness checks. |
| Journal/conference article | Low | Possible later extension. | Add external validation or stronger novelty beyond a hackathon workflow. |

## Must-Complete Before Public Publication Beyond Kaggle

- Notify Hack4Health organizers before public publication if required by the competition rules.
- Verify dataset licenses, citation requirements, and allowed redistribution boundaries.
- Confirm that no raw restricted datasets are committed or exposed.
- Add a related-work section based on verified primary sources.
- Add a data availability statement explaining how readers can access raw inputs.
- Add a code availability statement pointing to the public repository and commit/release.
- Add an ethics and limitations section that states the model is not clinical advice.
- Ensure final text is team-authored and AI assistance is disclosed accurately.

## Evidence Already Available

| Evidence type | Artifact |
|---|---|
| Data audit | `research/data_audit.md`, `outputs/tables/data_audit.json` |
| Cleaning sensitivity | `outputs/tables/cleaning_sensitivity_metrics.csv`, `outputs/figures/cleaning_sensitivity_auroc.png` |
| Model comparison | `outputs/tables/model_comparison.csv`, `outputs/tables/cross_validation_summary.csv` |
| Calibration | `outputs/tables/cardio_clean_calibration_bins.csv`, `outputs/figures/calibration_curve.png` |
| Interpretability | `outputs/tables/feature_importance.csv`, `outputs/tables/cardio_logreg_coefficients.csv`, `outputs/figures/feature_importance.png` |
| Error analysis | `research/error_analysis.md`, `outputs/tables/error_analysis_by_group.csv`, `outputs/figures/error_type_by_bp_band.png` |
| Reproducibility | `Makefile`, `scripts/`, `notebooks/02_final_kaggle_notebook.ipynb` |
| AI disclosure | `research/ai_usage_disclosure.md` |

## Related Work Needed

Add and verify citations for:

- Public cardiovascular risk prediction datasets and their known limitations.
- Data quality and plausibility checking in biomedical machine learning.
- Calibration and Brier score in clinical prediction modeling.
- Interpretability caveats for feature importance and predictive association.
- Transparent reporting standards for prediction models.

Do not add unverified citations. Use primary sources or official reporting guidelines where possible.

## Robustness Work Needed

- Add repeated cross-validation or bootstrap confidence intervals for the small `heart_processed.csv` comparison.
- Decide whether the heart dataset remains an appendix or a secondary result.
- Add a stricter written rationale for plausibility thresholds.
- Consider a compact threshold analysis for clinical operating points, clearly marked as illustrative.
- If ECG is included, validate row semantics, labels, and linkage before any supervised claim.

## Manuscript Guardrails

Allowed:

- "Predictive association."
- "Educational/research workflow."
- "Public dataset limitations."
- "Data-quality-aware modeling."
- "Held-out and cross-validation performance on this dataset."

Avoid:

- "Diagnosis."
- "Clinical decision support."
- "Patient-level deployment."
- "Causal effect."
- "Clinically validated."
- "Generalizes to real-world care."

## Preprint Abstract Checklist

- One sentence on why public cardiovascular ML needs data-quality checks.
- One sentence describing datasets and plausibility filtering.
- One sentence describing models and metrics.
- One sentence with the selected model's AUROC/AUPRC/Brier/CV result.
- One sentence on cleaning sensitivity.
- One sentence on asymmetric errors and limitations.
- One sentence stating educational/research status.

## Release Checklist

- `make all` passes from a clean working tree with raw data available locally.
- `make check` passes.
- `notebooks/02_final_kaggle_notebook.ipynb` is executed top-to-bottom.
- `submission/claims_ledger.md` matches the final writeup.
- Repository README explains data access and reproducibility.
- A release tag or final commit hash is recorded in the writeup.
- Publication/visibility permission has been checked with organizers.
