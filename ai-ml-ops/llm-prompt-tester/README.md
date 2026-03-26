# Llm Prompt Tester

Systematic prompt A/B testing agent that evaluates prompt variations across quality, consistency, and cost metrics to find the optimal prompt.

## Features
- Prompt variant management
- A/B testing framework
- Quality scoring (relevance, accuracy, coherence)
- Cost-per-response tracking
- Latency benchmarking
- Consistency measurement across runs
- Side-by-side comparison view
- Best prompt recommendation with confidence

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
