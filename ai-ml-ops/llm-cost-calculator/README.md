# LLM Cost Calculator 💰

Track token usage across AI providers, compare pricing, forecast monthly spending, and find cheaper alternatives.

## Features

- **Cost Calculation** — Instant pricing for any model/token combo
- **Model Comparison** — Side-by-side cost comparison across 24 models
- **Provider Analytics** — Breakdown by OpenAI, Anthropic, Google, Mistral, Meta
- **Usage Logging** — Track API calls with labels
- **Cost Reports** — Generate detailed breakdowns (text or Markdown)
- **Monthly Forecasting** — Project spending based on recent usage
- **Budget Alerts** — Check spend against thresholds
- **Cheap Alternatives** — Find cost-saving model swaps

## Quick Start

```bash
pip install -r requirements.txt

# Calculate a single call
python main.py calc gpt-4o 1000 500

# Compare all models
python main.py compare 10000 5000

# Find cheaper alternatives
python main.py cheapest gpt-4-turbo

# Log usage and generate reports
python main.py log gpt-4o 5000 2000 --label chat
python main.py log claude-3.5-sonnet 8000 4000 --label analysis
python main.py report
python main.py report --markdown

# Forecast and budget
python main.py forecast --days 7
python main.py budget 50.00

# Browse models
python main.py models
python main.py providers
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests are pure Python — no API keys needed.

## Project Structure

```
llm-cost-calculator/
├── main.py              # CLI with 9 subcommands
├── config.py            # Settings
├── requirements.txt     # Dependencies
├── agent/
│   ├── pricing.py       # 24 models, 5 providers pricing DB
│   ├── calculator.py    # Cost computation, reports, forecasting
│   └── storage.py       # JSON-based usage logging
└── tests/
    ├── conftest.py      # Shared fixtures
    ├── test_pricing.py  # Pricing tests (10)
    ├── test_calculator.py # Calculator tests (12)
    └── test_storage.py  # Storage tests (6)
```

## Supported Models (24)

| Provider | Models |
|----------|--------|
| OpenAI | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-4, gpt-3.5-turbo, o1, o1-mini, o3-mini |
| Anthropic | claude-3.5-sonnet, claude-3.5-haiku, claude-3-opus, claude-3-sonnet, claude-3-haiku |
| Google | gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash |
| Mistral | mistral-large, mistral-small, codestral |
| Meta | llama-3.1-405b, llama-3.1-70b, llama-3.1-8b |
