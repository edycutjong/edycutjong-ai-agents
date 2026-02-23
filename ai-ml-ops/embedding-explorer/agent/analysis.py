from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import NearestNeighbors
import numpy as np

class Analyzer:
    @staticmethod
    def find_clusters(embeddings, method="kmeans", n_clusters=5):
        """Finds clusters in the embeddings."""
        if embeddings is None or len(embeddings) == 0:
            return []

        if method == "kmeans":
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans.fit(embeddings)
            return kmeans.labels_
        else:
            raise ValueError(f"Unsupported clustering method: {method}")

    @staticmethod
    def find_outliers(embeddings, method="isolation_forest", contamination=0.05):
        """Detects outliers in the embeddings."""
        if embeddings is None or len(embeddings) == 0:
            return []

        if method == "isolation_forest":
            iso = IsolationForest(contamination=contamination, random_state=42)
            iso.fit(embeddings)
            # 1: Inlier, -1: Outlier. We can return boolean or the raw prediction.
            return iso.predict(embeddings)
        else:
            raise ValueError(f"Unsupported outlier detection method: {method}")

    @staticmethod
    def find_nearest_neighbors(embeddings, query_embedding, k=5):
        """Finds the indices and distances of the k nearest neighbors."""
        if embeddings is None or len(embeddings) == 0:
            return [], []

        # Ensure query_embedding is 2D array (1, n_features)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)

        nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(embeddings)
        distances, indices = nbrs.kneighbors(query_embedding)
        return indices[0], distances[0]
