# Permission Auditor

Scans app manifests and configurations for excessive permissions and suggests removals.

## Features
- Parse Android/iOS manifests
- Analyze Chrome extension permissions
- Compare declared vs used permissions
- Flag unnecessary permissions
- Suggest minimal permission set
- Generate permission justification docs
- Check OAuth scope minimality
- Support web app permission policies

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
