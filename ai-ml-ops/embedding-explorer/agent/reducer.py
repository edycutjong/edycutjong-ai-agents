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
            return np.array([])  # pragma: no cover

        # If input dim <= target dim, return as is (or pad/slice if strictly needed, but usually we just return)
        if embeddings.shape[1] <= self.n_components:
            return embeddings  # pragma: no cover

        if self.method == "pca":
            reducer = PCA(n_components=self.n_components, **self.kwargs)
        elif self.method == "tsne":
            # t-SNE perplexity must be less than n_samples
            n_samples = embeddings.shape[0]
            perplexity = self.kwargs.get('perplexity', 30)
            if n_samples <= perplexity:
                perplexity = max(1, n_samples - 1)  # pragma: no cover
                self.kwargs['perplexity'] = perplexity  # pragma: no cover

            reducer = TSNE(n_components=self.n_components, **self.kwargs)
        elif self.method == "umap":  # pragma: no cover
            try:  # pragma: no cover
                import umap  # pragma: no cover
                reducer = umap.UMAP(n_components=self.n_components, **self.kwargs)  # pragma: no cover
            except ImportError:  # pragma: no cover
                print("UMAP not installed, falling back to PCA")  # pragma: no cover
                reducer = PCA(n_components=self.n_components)  # pragma: no cover
        else:
            raise ValueError(f"Unsupported reduction method: {self.method}")  # pragma: no cover

        return reducer.fit_transform(embeddings)
