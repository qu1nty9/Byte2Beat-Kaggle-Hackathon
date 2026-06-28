# Byte2Beat Project Schema

This file adapts the LLM-wiki working pattern for the Byte2Beat hackathon workspace.

## Layers

1. Raw sources: `docs/`
   - Treat files in `docs/` as source-of-truth inputs.
   - Do not edit or overwrite raw competition documents or provided datasets.
   - If a derived copy is needed, write it under `outputs/` or document the derivation in `scripts/`.

2. Wiki: `research/`
   - LLM-maintained markdown knowledge base.
   - Update this layer whenever a source is ingested, a major experiment is run, or a project decision changes.
   - Prefer short, linkable pages over a single large note once the project grows.

3. Code and experiments
   - Reusable logic belongs in `src/byte2beat/`.
   - One-off utilities belong in `scripts/`.
   - Kaggle-facing notebooks belong in `notebooks/`.
   - Generated artifacts belong in `outputs/`.

## Required Wiki Files

- `research/index.md`: content-oriented table of key pages and artifacts.
- `research/log.md`: append-only chronological project log.
- `research/project_plan.md`: active strategy, milestones, and research tracks.
- `research/source_inventory.md`: source summaries and provenance notes.
- `research/data_audit.md`: dataset shape, quality issues, and modeling implications.

## Source Ingest Workflow

When processing a new document or dataset:

1. Read or profile the source directly from `docs/` or another cited raw location.
2. Add a source summary to `research/source_inventory.md`.
3. Update any affected topic page.
4. Append an entry to `research/log.md` using `## [YYYY-MM-DD] type | title`.
5. If the source affects project scope, update `research/project_plan.md`.

## Experiment Workflow

Each experiment should record:

- Research question.
- Dataset and exact input file path.
- Target variable and unit of analysis.
- Cleaning and exclusion rules.
- Split strategy and leakage risks.
- Model or analysis method.
- Primary and secondary metrics.
- Result table or figure path.
- Interpretation and limitations.

## Competition Constraints

- The final Kaggle Writeup must be public and should document the process honestly, including failed attempts.
- A public notebook is expected in the project files.
- A public demo link is optional but useful if the project has an interactive product.
- External datasets are allowed only when ethically sourced, de-identified, and cited with provenance.
- Generative AI may support coding, documentation, and visualization, but it must not be the core source of the research idea or main hypothesis. Written submissions should be authored by the team, and AI usage must be disclosed.
- Notify Hack4Health organizers before public publication such as a preprint, blog post, conference submission, GitHub release, or similar visibility push.

## Style

- Keep project-facing notes factual and citation-oriented.
- Separate observations from decisions.
- Prefer reproducible scripts over manual spreadsheet edits.
- Keep negative results; they are useful for the Kaggle writeup and future article.

