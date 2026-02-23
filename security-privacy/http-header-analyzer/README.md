# HTTP Header Analyzer 🔒
Analyze HTTP response headers for security best practices and grading.
## Quick Start
```bash
echo '{"Strict-Transport-Security": "max-age=31536000"}' | python main.py analyze -
python -m pytest tests/ -v
```
