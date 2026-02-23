# API Changelog Differ 📋

Compare OpenAPI/Swagger specs and detect breaking changes, deprecations, and new features.

## Quick Start
```bash
pip install -r requirements.txt
python main.py diff old_spec.json new_spec.json
python main.py diff old.json new.json --fail-on-breaking
python -m pytest tests/ -v
```
