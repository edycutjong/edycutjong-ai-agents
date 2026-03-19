# API Latency Budget Tracker

Agent that monitors API endpoint latency against Service Level Objective (SLO) budgets. Alerts when Error/Latency Budgets are being consumed too quickly.

## Usage

```bash
pip install -r requirements.txt
pytest --cov=. # run tests

# Run active synthesis probes
python main.py --config config.example.yaml

# Parse passive access logs
python main.py --config config.example.yaml --logs access.json --format markdown
```
