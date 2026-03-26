# Token Price Tracker

Real-time cryptocurrency price monitoring agent with configurable alerts, portfolio tracking, and market trend analysis across multiple exchanges.

## Features
- Real-time price fetching from CoinGecko/CoinMarketCap
- Multi-token watchlist management
- Price alert thresholds (above/below)
- Portfolio value calculator
- 24h/7d/30d trend analysis
- Historical price chart data export
- Market cap & volume tracking
- JSON/CSV export

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
