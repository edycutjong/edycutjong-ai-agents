# DeFi Yield Calculator

## Overview
APY comparison and yield farming calculator across DeFi protocols, with impermanent loss estimation and risk-adjusted return analysis.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- APY/APR comparison across protocols
- Impermanent loss calculator
- Compound interest projection
- Risk-adjusted yield scoring
- Liquidity pool analysis
- Staking reward estimator
- Historical yield trends
- Protocol TVL tracking

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
