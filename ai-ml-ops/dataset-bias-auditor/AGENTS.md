# Dataset Bias Auditor

## Overview
Training data bias detection agent that analyzes datasets for demographic imbalances, label distribution skews, and potential fairness issues.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Demographic attribute analysis
- Label distribution skew detection
- Class imbalance scoring
- Intersectional bias detection
- Sampling bias identification
- Fairness metric calculation
- Remediation recommendations
- Audit report generation

## File Structure
- `config.py` — Configuration & settings
- `main.py` — Entry point
- `requirements.txt` — Dependencies
- `tests/` — Tests module

## API Keys
- `GEMINI_API_KEY` — Required

## Localization
- Translations: `../../agent_translations.json`
- Hub i18n: `../../i18n.py`
- Supported: en, id, zh, es, pt, ja, ko, de, fr, ru, ar, hi

## Commands
- `pip install -r requirements.txt` — Install deps
- `python main.py` — Run agent
- `pytest tests/` — Run tests
