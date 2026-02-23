import pandas as pd
import json
import os
from jinja2 import Template

CHART_JS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div style="width: 80%; margin: auto;">
        <canvas id="myChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const data = {{ data }};
        const config = {
            type: '{{ chart_type }}',
            data: {
                labels: data.map(row => row['{{ x_col }}']),
                datasets: [{
                    label: '{{ y_col }}',
                    data: data.map(row => row['{{ y_col }}']),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: '{{ title }}'
                    }
                }
            }
        };
        new Chart(ctx, config);
    </script>
</body>
</html>
"""

def generate_js_chart(df: pd.DataFrame, chart_type: str, x: str, y: str, title: str, output_path: str):
    """
    Generates an HTML file with a Chart.js chart.

    Args:
        df: The Pandas DataFrame containing the data.
        chart_type: The type of chart to generate (e.g., 'bar', 'line', 'scatter').
        x: The column name for the x-axis (labels).
        y: The column name for the y-axis (values).
        title: The title of the chart.
        output_path: The path where the HTML file will be saved.
    """

    # Convert DataFrame to list of dicts for Jinja2
    data_records = df.to_dict(orient='records')

    template = Template(CHART_JS_TEMPLATE)
    html_content = template.render(
        title=title,
        data=json.dumps(data_records),
        chart_type=chart_type,
        x_col=x,
        y_col=y
    )

    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(html_content)

    return output_path
