# Sop Generator

Reads processes and workflows, generates Standard Operating Procedures with step-by-step instructions.

## Features
- Accept process description input
- Generate numbered step-by-step procedures
- Add decision trees for conditional steps
- Include safety/compliance notes
- Generate review and approval workflows
- Add version control metadata
- Include visual aids and diagrams
- Export as formatted Markdown/PDF

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
