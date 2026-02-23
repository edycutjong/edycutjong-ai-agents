import pytest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.reducer import DimensionalityReducer

def test_reduce_pca():
    embeddings = np.random.rand(10, 5)
    reducer = DimensionalityReducer(method="pca", n_components=2)
    reduced = reducer.reduce(embeddings)
    assert reduced.shape == (10, 2)

def test_reduce_tsne():
    embeddings = np.random.rand(10, 5)
    reducer = DimensionalityReducer(method="tsne", n_components=2, perplexity=2)
    reduced = reducer.reduce(embeddings)
    assert reduced.shape == (10, 2)
