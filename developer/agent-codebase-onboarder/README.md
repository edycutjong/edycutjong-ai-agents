# Codebase Onboarder

Generates 'Getting Started' guides by analyzing repo structure, README, package files, and key source files.

## Features
- Scan repository file structure
- Parse README and documentation
- Identify tech stack from config files
- Generate setup instructions
- Map key directories and their purposes
- Extract environment variable requirements
- Create architecture overview diagram
- List available scripts and commands
- Identify testing framework and patterns
- Export as markdown getting-started guide

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
