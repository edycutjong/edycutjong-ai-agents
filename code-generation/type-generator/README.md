# Type Generator 🔷
Generate TypeScript interfaces, Python dataclasses, and Zod schemas from JSON.
## Quick Start
```bash
python main.py generate data.json --format typescript --name User
python main.py generate data.json --format python
python main.py generate data.json --format zod
python -m pytest tests/ -v
```
