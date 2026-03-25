# Model Drift Detector

## Overview
ML model performance monitoring agent that detects data drift, concept drift, and prediction quality degradation over time.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Statistical drift detection (KS, PSI, chi-square)
- Feature distribution monitoring
- Prediction accuracy tracking
- Drift severity scoring
- Automated alert generation
- Retraining recommendation
- Baseline comparison reports
- Visual drift dashboard data

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
