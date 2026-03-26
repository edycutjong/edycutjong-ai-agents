# Dependency Advisor

Scans package.json/requirements.txt for CVEs, outdated packages, and suggests upgrade paths with migration guides.

## Features
- Parse package.json and requirements.txt
- Check NPM/PyPI for latest versions
- Query CVE databases for vulnerabilities
- Generate upgrade priority list
- Create migration guides for breaking changes
- Detect unused dependencies
- License compatibility checking
- Suggest lighter alternatives
- Export dependency report
- Configurable severity thresholds

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
