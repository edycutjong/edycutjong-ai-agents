# Model Drift Detector

ML model performance monitoring agent that detects data drift, concept drift, and prediction quality degradation over time.

## Features
- Statistical drift detection (KS, PSI, chi-square)
- Feature distribution monitoring
- Prediction accuracy tracking
- Drift severity scoring
- Automated alert generation
- Retraining recommendation
- Baseline comparison reports
- Visual drift dashboard data

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
