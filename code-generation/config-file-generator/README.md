# Config File Generator ⚙️

Generate ESLint, Prettier, TSConfig, EditorConfig, gitignore, Dockerfile, and GitHub Actions configs from presets.

## Quick Start

```bash
pip install -r requirements.txt

python main.py generate eslint --preset react
python main.py generate prettier --save
python main.py scaffold eslint,prettier,tsconfig --save
python main.py list
python main.py detect --path .
```

## Running Tests

```bash
python -m pytest tests/ -v
```
