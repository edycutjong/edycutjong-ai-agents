# Incident Summarizer

Parses application logs and alerts to generate structured incident summaries with timeline and root cause analysis.

## Features
- Parse structured and unstructured logs
- Build incident timeline
- Identify error patterns and clusters
- Generate root cause hypothesis
- Create severity classification
- Extract affected services/endpoints
- Suggest remediation steps
- Support multiple log formats (JSON, syslog)
- Generate postmortem template
- Configurable alert thresholds

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
