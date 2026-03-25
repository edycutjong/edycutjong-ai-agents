# Gas Fee Estimator

## Overview
Ethereum and L2 gas fee optimization advisor that predicts optimal transaction timing and recommends the cheapest execution window.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Real-time gas price tracking (slow/standard/fast)
- Historical gas price patterns
- Optimal send-time prediction
- L2 vs L1 cost comparison
- EIP-1559 base fee analysis
- Transaction cost estimation by type
- Gas price alerts
- Weekly gas report generation

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
