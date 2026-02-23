# Env File Auditor 🔍
Audit .env files for missing values, exposed secrets, and duplicates.
## Quick Start
```bash
python main.py audit .env
python main.py compare .env .env.production
python main.py template .env > .env.example
python -m pytest tests/ -v
```
