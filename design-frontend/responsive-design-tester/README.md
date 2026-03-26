# Responsive Design Tester

Screenshots web pages at multiple viewports and flags layout issues automatically.

## Features
- Capture screenshots at multiple breakpoints
- Detect layout overflow issues
- Flag text truncation problems
- Check touch target sizes on mobile
- Compare against design mockups
- Generate responsive audit report
- Support custom viewport sizes
- Test horizontal scrolling issues

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
