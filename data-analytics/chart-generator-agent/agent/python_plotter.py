import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_python_chart(df: pd.DataFrame, chart_type: str, x: str, y: str = None, title: str = "Chart", output_path: str = "output/chart.png", **kwargs):
    """
    Generates a chart using Matplotlib/Seaborn and saves it to a file.

    Args:
        df: The Pandas DataFrame containing the data.
        chart_type: The type of chart to generate (e.g., 'bar', 'line', 'scatter', 'hist', 'box').
        x: The column name for the x-axis.
        y: The column name for the y-axis (optional for some chart types).
        title: The title of the chart.
        output_path: The path where the chart image will be saved.
        **kwargs: Additional keyword arguments for the plotting function.
    """
    plt.figure(figsize=(10, 6))

    try:
        if chart_type == 'bar':
            if y is None:
                raise ValueError("Bar chart requires both x and y columns.")
            sns.barplot(data=df, x=x, y=y, **kwargs)
        elif chart_type == 'line':
            if y is None:
                raise ValueError("Line chart requires both x and y columns.")
            sns.lineplot(data=df, x=x, y=y, **kwargs)
        elif chart_type == 'scatter':
            if y is None:
                raise ValueError("Scatter chart requires both x and y columns.")
            sns.scatterplot(data=df, x=x, y=y, **kwargs)
        elif chart_type == 'hist':
            sns.histplot(data=df, x=x, **kwargs)
        elif chart_type == 'box':
            sns.boxplot(data=df, x=x, y=y, **kwargs)
        else:
            raise ValueError(f"Unsupported chart type: {chart_type}")

        plt.title(title)
        plt.tight_layout()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        plt.savefig(output_path)
        plt.close()

        return output_path
    except Exception as e:
        plt.close()
        raise e
