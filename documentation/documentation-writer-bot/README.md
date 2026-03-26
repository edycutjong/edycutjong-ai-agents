# Documentation Writer Bot

Agent that reads codebases and generates/updates documentation folders.

## Features
- Scan file structure\n- Read code (functions/classes)\n- Generate Markdown docs\n- Update existing docs (diff aware)\n- Create diagrams (Mermaid)\n- API reference generation\n- Commit changes\n- Tone configuration

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
