# Figma To Css Agent

Extracts design properties from Figma export files and generates production CSS.

## Features
- Parse Figma JSON exports
- Extract layout properties (flex, grid)
- Generate CSS classes
- Convert colors to CSS variables
- Handle responsive breakpoints
- Generate component CSS modules
- Support SCSS/CSS-in-JS output
- Create design system starter

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
