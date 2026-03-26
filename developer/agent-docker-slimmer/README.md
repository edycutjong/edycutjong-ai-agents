# Docker Slimmer

Analyzes Dockerfiles and suggests optimizations for smaller images including multi-stage builds and layer caching.

## Features
- Parse Dockerfile instructions
- Suggest multi-stage build patterns
- Recommend smaller base images
- Optimize layer ordering for caching
- Detect unnecessary packages
- Remove build-time only dependencies
- Estimate image size savings
- Suggest .dockerignore improvements
- Security scan base images
- Generate optimized Dockerfile

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
