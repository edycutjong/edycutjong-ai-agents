# Token Price Tracker

## Overview
Real-time cryptocurrency price monitoring agent with configurable alerts, portfolio tracking, and market trend analysis across multiple exchanges.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Real-time price fetching from CoinGecko/CoinMarketCap
- Multi-token watchlist management
- Price alert thresholds (above/below)
- Portfolio value calculator
- 24h/7d/30d trend analysis
- Historical price chart data export
- Market cap & volume tracking
- JSON/CSV export

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
