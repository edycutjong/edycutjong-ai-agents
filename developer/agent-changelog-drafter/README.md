# Changelog Drafter

Reads git log between tags and drafts human-readable changelogs with automatic categorization.

## Features
- Parse git log between version tags
- Categorize commits (feat/fix/docs/chore)
- Group by component or scope
- Generate markdown changelog
- Support conventional commits
- Detect breaking changes
- Link to PR/issue numbers
- Configurable category mappings
- Support monorepo structures
- Export for GitHub Releases

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
