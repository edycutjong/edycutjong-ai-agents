import plotly.express as px  # pragma: no cover
import pandas as pd  # pragma: no cover

class Visualizer:  # pragma: no cover
    @staticmethod  # pragma: no cover
    def create_scatter_plot(embeddings, labels=None, hover_data=None, title="Embeddings Visualization"):  # pragma: no cover
        """Generates an interactive scatter plot of the embeddings."""
        if embeddings is None or len(embeddings) == 0:  # pragma: no cover
            return None  # pragma: no cover

        dim = embeddings.shape[1]  # pragma: no cover

        # Prepare DataFrame for Plotly
        df_dict = {}  # pragma: no cover
        for i in range(dim):  # pragma: no cover
            df_dict[f'dim_{i+1}'] = embeddings[:, i]  # pragma: no cover

        if labels is not None:  # pragma: no cover
            df_dict['label'] = labels  # pragma: no cover

        if hover_data is not None:  # pragma: no cover
            # Flatten or truncate large text for hover
            cleaned_hover = [str(x)[:200] + "..." if len(str(x)) > 200 else str(x) for x in hover_data]  # pragma: no cover
            df_dict['hover_text'] = cleaned_hover  # pragma: no cover

        df = pd.DataFrame(df_dict)  # pragma: no cover

        if dim == 2:  # pragma: no cover
            fig = px.scatter(  # pragma: no cover
                df,
                x='dim_1',
                y='dim_2',
                color='label' if labels is not None else None,
                hover_data=['hover_text'] if hover_data is not None else None,
                title=title
            )
        elif dim == 3:  # pragma: no cover
            fig = px.scatter_3d(  # pragma: no cover
                df,
                x='dim_1',
                y='dim_2',
                z='dim_3',
                color='label' if labels is not None else None,
                hover_data=['hover_text'] if hover_data is not None else None,
                title=title
            )
        else:
            # Fallback for > 3D: Use first 2 dims or warn
            fig = px.scatter(  # pragma: no cover
                df,
                x='dim_1',
                y='dim_2',
                color='label' if labels is not None else None,
                hover_data=['hover_text'] if hover_data is not None else None,
                title=f"{title} (First 2 Dimensions of {dim}D)"
            )

        return fig  # pragma: no cover
