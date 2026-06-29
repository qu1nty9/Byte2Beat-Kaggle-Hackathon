# Release Manifest

Release tag: `v1.0.0-kaggle-submission`

Release date: 2026-06-30

Repository: `qu1nty9/Byte2Beat-Kaggle-Hackathon`

Author:

- Yaroslav Kholmirzayev
- yaric.kholm@gmail.com

## Release Scope

This release is the stable Kaggle submission snapshot for:

> From Byte to Beat: Auditing Cardiovascular Risk Before Modeling It

It includes the final writeup, public notebook, data card, model card, reproducibility scripts, generated result tables, generated figures, and quality gate.

## Required Kaggle-Facing Files

| Asset | Path | Status |
|---|---|---|
| Final writeup | `submission/final_kaggle_writeup.md` | Ready for author paste/review in Kaggle |
| Public notebook | `notebooks/02_final_kaggle_notebook.ipynb` | Executed locally top-to-bottom |
| Data card | `submission/data_card.md` | Ready |
| Model card | `submission/model_card.md` | Ready |
| AI disclosure | `research/ai_usage_disclosure.md` | Ready, author should verify wording |
| Claims ledger | `submission/claims_ledger.md` | Ready |
| Figure manifest | `submission/figure_manifest.md` | Ready |

## Automated Validation

Most recent local validation before release:

```bash
make all
make check
```

Expected quality gate summary:

```text
Submission package quality gate passed: 38 assets, 11 tables, 16 figures, 2 notebooks.
```

Notebook validation:

- `notebooks/02_final_kaggle_notebook.ipynb` executed locally top-to-bottom.
- 22 code cells executed.
- 0 error outputs.

## Manual Checks Still Required

These items cannot be fully verified from the local repository:

- Confirm the Kaggle competition page accepts the final writeup format.
- Confirm the public notebook can access the official Kaggle data resource paths.
- Confirm the GitHub repository is public or accessible to judges.
- Confirm raw dataset redistribution/license requirements.
- Notify Hack4Health organizers before any public release beyond Kaggle, if required by rules.

## Canonical Results

Selected model: `hist_gradient_boosting`

Primary dataset: plausibility-cleaned `cardio_base.csv`

Held-out metrics:

- AUROC: 0.8037.
- AUPRC: 0.7892.
- Accuracy: 0.7355.
- Brier score: 0.1795.
- 5-fold CV AUROC: 0.8013 +/- 0.0025.

Bootstrap uncertainty:

- AUROC 95% interval: 0.7970-0.8103.
- AUPRC 95% interval: 0.7796-0.7990.
- Accuracy 95% interval: 0.7290-0.7425.
- Brier score 95% interval: 0.1765-0.1825.

Threshold trade-off:

- Default threshold 0.50: sensitivity 0.6876, specificity 0.7825.
- Threshold 0.35: sensitivity 0.8329, specificity 0.5820.
- Threshold 0.55: sensitivity 0.6451, specificity 0.8215.

## Release Guardrails

- Do not describe the model as clinically validated.
- Do not describe the threshold analysis as a clinical recommendation.
- Do not claim ECG modeling success.
- Do not redistribute raw data unless the competition/license terms permit it.
- Keep AI usage disclosure visible and accurate.
