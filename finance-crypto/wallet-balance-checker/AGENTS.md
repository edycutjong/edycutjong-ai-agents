# Wallet Balance Checker

## Overview
Multi-chain cryptocurrency wallet portfolio viewer that aggregates balances across Ethereum, Solana, Bitcoin, and L2 networks into a unified dashboard.

## Tech
- Python 3.10+
- LangChain
- Gemini API
- pytest

## Features
- Multi-chain support (ETH, SOL, BTC, Polygon, Arbitrum)
- ERC-20/SPL token balance detection
- USD/EUR value conversion
- Portfolio allocation breakdown
- Transaction history summary
- NFT holdings detection
- Gas cost estimation
- Export as JSON report

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
