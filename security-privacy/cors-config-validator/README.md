# CORS Config Validator 🔒
Validate CORS configurations for security best practices.
## Quick Start
```bash
echo '{"allow_origins": ["*"], "allow_credentials": true}' | python main.py validate -
python -m pytest tests/ -v
```
