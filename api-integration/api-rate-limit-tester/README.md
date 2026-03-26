# Api Rate Limit Tester

Stress-tests APIs to map rate limits and generates usage documentation.

## Features
- Send configurable request bursts
- Detect rate limit headers (X-RateLimit)
- Map rate limit thresholds
- Identify rate limit reset windows
- Generate rate limit documentation
- Test different auth levels
- Visualize rate limit curves
- Suggest client-side throttling

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
