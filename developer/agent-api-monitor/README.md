# Api Monitor

Agent that monitors API endpoints for uptime, response time, and schema changes. Alerts on anomalies.

## Features
- Endpoint health check scheduling
- Response time tracking and graphing
- Schema change detection (JSON diff)
- Alert notifications (webhook)
- Status page generation
- Historical uptime calculation
- Multi-region checking
- Custom assertion rules
- SSL certificate expiry monitoring
- Dashboard with charts

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
