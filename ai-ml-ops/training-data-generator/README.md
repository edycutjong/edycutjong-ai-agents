# Training Data Generator 📚
Generate synthetic LLM training datasets with templates, variations, and validation.
## Quick Start
```bash
python main.py generate --category qa --vars topic=Python definition="a programming language" --count 10
python main.py validate dataset.json
python main.py templates
python -m pytest tests/ -v
```
