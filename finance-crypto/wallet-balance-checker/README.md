# Wallet Balance Checker

Multi-chain cryptocurrency wallet portfolio viewer that aggregates balances across Ethereum, Solana, Bitcoin, and L2 networks into a unified dashboard.

## Features
- Multi-chain support (ETH, SOL, BTC, Polygon, Arbitrum)
- ERC-20/SPL token balance detection
- USD/EUR value conversion
- Portfolio allocation breakdown
- Transaction history summary
- NFT holdings detection
- Gas cost estimation
- Export as JSON report

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
