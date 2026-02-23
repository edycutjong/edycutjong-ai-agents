# JSON Schema Generator 📐
Infer JSON Schema from sample data with format detection.
## Quick Start
```bash
echo '{"name":"Alice","email":"a@b.com"}' | python main.py generate -
python main.py generate data.json --title UserSchema
python -m pytest tests/ -v
```
