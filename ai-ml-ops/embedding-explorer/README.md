# Embedding Explorer

Visualizes and searches vector embeddings, finds clusters, outliers, and nearest neighbors.

## Features
- Load embeddings from files/databases
- Reduce dimensions (t-SNE/UMAP)
- Visualize clusters interactively
- Find nearest neighbors for queries
- Detect outlier embeddings
- Compare embedding models
- Export visualizations
- Support text/image embeddings

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
