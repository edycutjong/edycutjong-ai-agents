# Oauth Flow Debugger

Traces OAuth 2.0 flows step-by-step, identifies misconfigurations, and suggests fixes.

## Features
- Trace authorization code flow
- Trace client credentials flow
- Inspect token payloads (JWT decode)
- Validate redirect URI configurations
- Check scope permissions
- Detect common misconfigurations
- Generate flow sequence diagrams
- Test token refresh cycles

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
