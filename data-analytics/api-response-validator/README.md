# API Response Validator 🔍
Validate API responses against schemas with type checking and pattern matching.
## Quick Start
```bash
echo '{"id": 1, "name": "test"}' | python main.py validate - --status 200
python -m pytest tests/ -v
```
