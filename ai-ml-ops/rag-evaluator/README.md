# Rag Evaluator

Tests RAG pipeline quality by measuring retrieval accuracy and answer relevance.

## Features
- Define evaluation test cases
- Measure retrieval precision/recall
- Score answer faithfulness
- Detect hallucinations vs source
- Compare different RAG configurations
- Generate evaluation reports
- Support multiple vector stores
- Benchmark latency and cost

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
