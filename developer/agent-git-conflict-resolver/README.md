# Git Conflict Resolver

Parses git merge conflicts and suggests semantic resolutions based on understanding both sides of changes.

## Features
- Parse conflict markers in files
- Analyze both sides of conflicts
- Suggest resolution based on semantic analysis
- Handle common patterns (imports, configs)
- Preserve formatting consistency
- Detect overlapping changes
- Support multiple file types
- Generate resolution preview
- Confidence scoring per resolution
- Batch resolve similar conflicts

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
