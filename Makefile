PYTHON ?= .venv/bin/python
PIP ?= .venv/bin/pip

.PHONY: setup audit eda baseline models sensitivity errors uncertainty submission-check ecg notebook final-notebook all check

setup:
	python -m venv .venv
	$(PIP) install -r requirements.txt

audit:
	$(PYTHON) scripts/profile_data.py

eda:
	$(PYTHON) scripts/eda_tabular.py
	$(PYTHON) scripts/generate_eda_figures.py

baseline:
	$(PYTHON) scripts/baseline_tabular_numpy.py

models:
	$(PYTHON) scripts/model_comparison.py

sensitivity:
	$(PYTHON) scripts/cleaning_sensitivity.py

errors:
	$(PYTHON) scripts/error_analysis.py

uncertainty:
	$(PYTHON) scripts/uncertainty_threshold_analysis.py

submission-check:
	$(PYTHON) scripts/check_submission_assets.py

ecg:
	$(PYTHON) scripts/profile_ecg_schema.py

notebook:
	$(PYTHON) -m nbconvert --to notebook --execute --inplace notebooks/01_eda_and_baseline.ipynb

final-notebook:
	$(PYTHON) -m nbconvert --to notebook --execute --inplace notebooks/02_final_kaggle_notebook.ipynb

all: audit eda baseline models sensitivity errors uncertainty ecg

check:
	$(PYTHON) -m py_compile scripts/*.py src/byte2beat/*.py
	$(PYTHON) scripts/check_submission_assets.py
