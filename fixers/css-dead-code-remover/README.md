# Css Dead Code Remover

Identify unused CSS selectors.

## Features
- Crawl pages/components\n- Match selectors\n- Identify coverage\n- Purge capabilities\n- Safe-list checking\n- Media query audits\n- Visual regression check\n- Minify

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
