# Submission Package

This directory contains team-facing submission materials.

Important policy note: Hack4Health rules state that final written submissions must be authored by the participant/team. Treat these files as evidence organization, structure, and review scaffolding. The final Kaggle Writeup text should be reviewed, edited, and approved by the author before submission.

Run `make submission-check` before publishing. It validates required files, result schemas, claims-ledger and writeup evidence links, notebook execution status, figure readability, and notebook path hygiene.

## Files

- `final_kaggle_writeup.md`: final Kaggle writeup text with title, subtitle, author block, results, limitations, and disclosure.
- `release_manifest.md`: stable release tag, validation status, Kaggle-facing files, and manual checks.
- `kaggle_writeup_team_template.md`: section-by-section template with evidence to include.
- `kaggle_writeup_review_draft.md`: review-ready scaffold for the final Kaggle writeup.
- `data_card.md`: project data card with source, cleaning, risk, and use-boundary notes.
- `model_card.md`: selected model card with intended use, metrics, robustness, and failure modes.
- `result_cards.md`: compact table of key numbers and claims.
- `claims_ledger.md`: claim-by-claim evidence map, confidence level, and overclaiming guardrails.
- `figure_manifest.md`: list of figures, intended use, and supporting claim.
- `final_submission_checklist.md`: final review checklist before Kaggle submission.

## Related Assets

- Public notebook draft: `notebooks/01_eda_and_baseline.ipynb`
- Polished final notebook: `notebooks/02_final_kaggle_notebook.ipynb`
- Research plan: `research/project_plan.md`
- Current writeup draft: `research/kaggle_writeup_draft.md`
- Final Kaggle writeup: `submission/final_kaggle_writeup.md`
- Review-ready writeup draft: `submission/kaggle_writeup_review_draft.md`
- AI disclosure draft: `research/ai_usage_disclosure.md`
- Publication readiness: `paper/publication_readiness.md`
- Release notes: `RELEASE_NOTES.md`
- Release manifest: `submission/release_manifest.md`
