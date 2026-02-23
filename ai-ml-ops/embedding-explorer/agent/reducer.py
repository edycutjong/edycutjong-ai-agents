from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np

class DimensionalityReducer:
    def __init__(self, method="pca", n_components=2, **kwargs):
        self.method = method.lower()
        self.n_components = n_components
        self.kwargs = kwargs

    def reduce(self, embeddings):
        """Reduces the dimensionality of embeddings."""
        if embeddings is None or len(embeddings) == 0:
            return np.array([])

        # If input dim <= target dim, return as is (or pad/slice if strictly needed, but usually we just return)
        if embeddings.shape[1] <= self.n_components:
            return embeddings

        if self.method == "pca":
            reducer = PCA(n_components=self.n_components, **self.kwargs)
        elif self.method == "tsne":
            # t-SNE perplexity must be less than n_samples
            n_samples = embeddings.shape[0]
            perplexity = self.kwargs.get('perplexity', 30)
            if n_samples <= perplexity:
                perplexity = max(1, n_samples - 1)
                self.kwargs['perplexity'] = perplexity

            reducer = TSNE(n_components=self.n_components, **self.kwargs)
        elif self.method == "umap":
            try:
                import umap
                reducer = umap.UMAP(n_components=self.n_components, **self.kwargs)
            except ImportError:
                print("UMAP not installed, falling back to PCA")
                reducer = PCA(n_components=self.n_components)
        else:
            raise ValueError(f"Unsupported reduction method: {self.method}")

        return reducer.fit_transform(embeddings)
