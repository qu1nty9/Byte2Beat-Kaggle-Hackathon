# Source Inventory

## Competition Documents

### `docs/Byte2Beat - description.pdf`

Kaggle-facing description. The hackathon asks participants to build AI or computational solutions for cardiovascular challenges, including early detection, progression forecasting, or interpretability of risk factors. It specifies a Kaggle Writeup as the final report, a public notebook as project code, and an optional public product/demo link.

Rubric signal from the PDF: usefulness, informativeness, documentation quality, and novelty are each worth 15 points for 60 total.

### `docs/drive-download-20260627T215828Z-3-001/Byte2Beat Competition Packet.docx`

Detailed competition packet. It frames the challenge as AI for cardiovascular health and encourages prediction, risk assessment, disease detection, physiological analysis, explainable AI, and medically relevant applications. It recommends EDA, reproducibility, GPU resources for deep learning, and clear discussion of model errors and limitations.

### `docs/drive-download-20260627T215828Z-3-001/Hack4Health Hackathon Rules General.docx`

Rules and deliverables. The project must address a biomedical, computational science, or digital health problem. External datasets are allowed when ethically sourced, de-identified, privacy-compliant, and cited.

Deliverables include a repository with data pipelines, model code, reproducibility scaffolds, documentation, and evaluation notes, plus a summary document or poster-style draft covering problem framing, methods, results, limitations, next steps, and societal impact.

Important AI policy: generative AI can support coding, documentation, and visualization, but it cannot be the core source of the research idea or main hypothesis. Written submissions must be authored by the team and AI use must be disclosed.

Publishing note: organizers should be notified before public publication such as a preprint, blog post, conference submission, GitHub release, or similar visibility.

### `docs/drive-download-20260627T215828Z-3-001/Byte2Beat Project Ideas.xlsm`

Idea catalog with 102 project ideas, dataset suggestions, method tags, and feasibility caveats. The summary sheet highlights datasets including MIMIC-IV, NHANES, All of Us, MESA, ARIC, ClinicalTrials.gov, and others. Many ideas are explicitly framed as exploratory secondary-data analogues.

## Provided Datasets

### Cardiac Failure

Files:

- `docs/drive-download-20260627T215828Z-3-001/Datasets/Cardiac Failure/cardio_base.csv`
- `docs/drive-download-20260627T215828Z-3-001/Datasets/Cardiac Failure/cardiac_failure_processed.csv`

The base file is semicolon-separated and has 70,000 rows with target `cardio`. The processed file appears to be the same data with scaled age and an extra unnamed index column.

### Heart Attack

File:

- `docs/drive-download-20260627T215828Z-3-001/Datasets/Heart Attack/heart_processed.csv`

Small tabular dataset with 918 rows and target `HeartDisease`. It is already one-hot encoded for several categorical variables.

### ECG Timeseries

File:

- `docs/drive-download-20260627T215828Z-3-001/Datasets/ECG Timeseries/ecg_timeseries.csv`

Large CSV, approximately 632 MB. Initial inspection shows 528 rows and 123,995 columns including an index-like first column. It should not be loaded naively in early experiments. Use specialized readers, sampling, conversion to a more efficient format, and feature extraction.

