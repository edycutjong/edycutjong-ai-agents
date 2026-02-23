import plotly.express as px
import pandas as pd

class Visualizer:
    @staticmethod
    def create_scatter_plot(embeddings, labels=None, hover_data=None, title="Embeddings Visualization"):
        """Generates an interactive scatter plot of the embeddings."""
        if embeddings is None or len(embeddings) == 0:
            return None

        dim = embeddings.shape[1]

        # Prepare DataFrame for Plotly
        df_dict = {}
        for i in range(dim):
            df_dict[f'dim_{i+1}'] = embeddings[:, i]

        if labels is not None:
            df_dict['label'] = labels

        if hover_data is not None:
            # Flatten or truncate large text for hover
            cleaned_hover = [str(x)[:200] + "..." if len(str(x)) > 200 else str(x) for x in hover_data]
            df_dict['hover_text'] = cleaned_hover

        df = pd.DataFrame(df_dict)

        if dim == 2:
            fig = px.scatter(
                df,
                x='dim_1',
                y='dim_2',
                color='label' if labels is not None else None,
                hover_data=['hover_text'] if hover_data is not None else None,
                title=title
            )
        elif dim == 3:
            fig = px.scatter_3d(
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
            fig = px.scatter(
                df,
                x='dim_1',
                y='dim_2',
                color='label' if labels is not None else None,
                hover_data=['hover_text'] if hover_data is not None else None,
                title=f"{title} (First 2 Dimensions of {dim}D)"
            )

        return fig
