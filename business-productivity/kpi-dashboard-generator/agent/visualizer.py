import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class Visualizer:
    @staticmethod
    def create_trend_chart(df, date_col, value_col, title="Trend Analysis", aggregation='sum'):
        """Creates a time-series trend chart."""
        try:
            # Ensure date column is datetime
            df_chart = df.copy()
            try:
                df_chart[date_col] = pd.to_datetime(df_chart[date_col])
            except:
                return None # If date conversion fails

            # Aggregate by date if needed
            if aggregation == 'sum':
                df_agg = df_chart.groupby(date_col)[value_col].sum().reset_index()
            elif aggregation == 'avg' or aggregation == 'mean':
                df_agg = df_chart.groupby(date_col)[value_col].mean().reset_index()
            else:
                 df_agg = df_chart # Raw data

            fig = px.line(df_agg, x=date_col, y=value_col, title=title, markers=True)
            fig.update_layout(template="plotly_dark", autosize=True)
            return fig
        except Exception as e:
            return None

    @staticmethod
    def create_bar_chart(df, category_col, value_col, title="Category Analysis", aggregation='sum'):
        """Creates a bar chart for categorical data."""
        try:
            df_chart = df.copy()
            if aggregation == 'sum':
                df_agg = df_chart.groupby(category_col)[value_col].sum().reset_index()
            elif aggregation == 'avg' or aggregation == 'mean':
                 df_agg = df_chart.groupby(category_col)[value_col].mean().reset_index()
            elif aggregation == 'count':
                 df_agg = df_chart.groupby(category_col).size().reset_index(name=value_col)
            else:
                 df_agg = df_chart

            # Sort by value
            if value_col in df_agg.columns:
                df_agg = df_agg.sort_values(by=value_col, ascending=False)

            fig = px.bar(df_agg, x=category_col, y=value_col, title=title)
            fig.update_layout(template="plotly_dark", autosize=True)
            return fig
        except Exception as e:
            return None
