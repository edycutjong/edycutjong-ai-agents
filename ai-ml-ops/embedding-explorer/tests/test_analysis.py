import pytest
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.analysis import Analyzer

def test_find_clusters():
    embeddings = np.random.rand(20, 5)
    labels = Analyzer.find_clusters(embeddings, n_clusters=2)
    assert len(labels) == 20
    assert len(set(labels)) == 2

def test_find_outliers():
    embeddings = np.random.rand(20, 5)
    outliers = Analyzer.find_outliers(embeddings, method="isolation_forest", contamination=0.1)
    assert len(outliers) == 20
    assert set(outliers).issubset({-1, 1})

def test_find_nearest_neighbors():
    embeddings = np.array([[0, 0], [1, 1], [2, 2]])
    query = np.array([0.1, 0.1])
    indices, distances = Analyzer.find_nearest_neighbors(embeddings, query, k=1)
    assert indices[0] == 0
    assert distances[0] < 0.2
