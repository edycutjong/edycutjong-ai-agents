# Chart Generator Agent

Takes data and natural language queries, generates chart code (Chart.js, D3, Matplotlib).

## Features
- Accept CSV/JSON data input
- Parse natural language chart requests
- Generate Chart.js configurations
- Generate D3.js visualizations
- Generate Matplotlib/Seaborn plots
- Auto-select appropriate chart type
- Customize colors, labels, axes
- Export as HTML/PNG/SVG

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
