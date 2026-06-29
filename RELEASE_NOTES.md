# Release Notes

## v1.0.0-kaggle-submission

Release date: 2026-06-30

Release purpose: stable Kaggle submission snapshot for the Byte2Beat / Hack4Health cardiovascular AI project.

Final project title:

> From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

Subtitle:

> A data-quality-first Byte2Beat workflow where plausibility checks, calibration, and failure-mode analysis matter as much as AUROC.

Author:

- Yaroslav Kholmirzayev
- yaric.kholm@gmail.com

## Included Submission Assets

- Final Kaggle writeup: `submission/final_kaggle_writeup.md`
- Public notebook: `notebooks/02_final_kaggle_notebook.ipynb`
- Data card: `submission/data_card.md`
- Model card: `submission/model_card.md`
- Claims ledger: `submission/claims_ledger.md`
- Figure manifest: `submission/figure_manifest.md`
- Final checklist: `submission/final_submission_checklist.md`
- Publication readiness plan: `paper/publication_readiness.md`

## Main Results

Selected model: `hist_gradient_boosting` on the plausibility-cleaned cardiac dataset.

Held-out test metrics:

| Metric | Value |
|---|---:|
| AUROC | 0.8037 |
| AUPRC | 0.7892 |
| Accuracy | 0.7355 |
| Brier score | 0.1795 |
| 5-fold CV AUROC | 0.8013 +/- 0.0025 |

Bootstrap 95% intervals:

| Metric | 95% interval |
|---|---:|
| AUROC | 0.7970-0.8103 |
| AUPRC | 0.7796-0.7990 |
| Accuracy | 0.7290-0.7425 |
| Brier score | 0.1765-0.1825 |

Threshold analysis:

| Operating point | Threshold | Sensitivity | Specificity | FP | FN |
|---|---:|---:|---:|---:|---:|
| Default | 0.50 | 0.6876 | 0.7825 | 1,885 | 2,651 |
| Max F1 / sensitivity >= 0.80 | 0.35 | 0.8329 | 0.5820 | 3,623 | 1,418 |
| Specificity >= 0.80 | 0.55 | 0.6451 | 0.8215 | 1,547 | 3,011 |

## Reproducibility

Recommended validation commands:

```bash
make all
make check
make submission-check
```

Current quality gate validates:

- Required submission files.
- Core result table schemas.
- JSON audit artifacts.
- Claims-ledger and writeup evidence links.
- Final writeup structure.
- Data card and model card structure.
- Required figure readability.
- Public notebook execution status and error outputs.
- Notebook path hygiene.

## Known Boundaries

- Raw competition datasets are not committed to the repository.
- The model is educational/research-only and is not a clinical tool.
- ECG data remain a gated extension because schema and label semantics are not validated.
- Publication beyond Kaggle may require organizer notification and dataset license review.
