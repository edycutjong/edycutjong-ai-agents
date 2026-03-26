# Gas Fee Estimator

Ethereum and L2 gas fee optimization advisor that predicts optimal transaction timing and recommends the cheapest execution window.

## Features
- Real-time gas price tracking (slow/standard/fast)
- Historical gas price patterns
- Optimal send-time prediction
- L2 vs L1 cost comparison
- EIP-1559 base fee analysis
- Transaction cost estimation by type
- Gas price alerts
- Weekly gas report generation

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
