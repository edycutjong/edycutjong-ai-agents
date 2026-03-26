# Component Documenter

Reads React/Vue/Svelte components and generates Storybook-style documentation.

## Features
- Parse component props/types
- Generate interactive examples
- Document component variants
- Create usage guidelines
- Generate prop tables
- Extract JSDoc/TSDoc comments
- Support React/Vue/Svelte/Angular
- Export as MDX/Markdown

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
