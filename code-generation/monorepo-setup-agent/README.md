# Monorepo Setup Agent

Scaffolds monorepo structures with workspaces, shared packages, and CI pipelines.

## Features
- Generate Turborepo/Nx workspace
- Create shared package structure
- Configure npm/pnpm workspaces
- Set up shared tsconfig
- Generate CI pipeline configs
- Add changeset configuration
- Create package publishing setup
- Include documentation templates

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
