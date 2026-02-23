import os
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

class Visualizer:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_treemap(self, dependency_sizes: List[Dict[str, Any]]) -> str:
        """
        Generates a Treemap of dependency sizes.
        Returns the HTML string of the chart.
        """
        if not dependency_sizes:
            return "<div class='text-gray-500'>No size data available</div>"

        # Prepare data for Plotly
        data = []
        for dep in dependency_sizes:
            name = dep.get("name", "unknown")
            size = dep.get("size", 0)
            gzip = dep.get("gzip", 0)
            data.append({"name": name, "size": size, "gzip": gzip, "label": f"{name}<br>{self._format_bytes(size)}"})

        df = pd.DataFrame(data)

        if df.empty:
             return "<div class='text-gray-500'>No size data available</div>"

        fig = px.treemap(df, path=['name'], values='size',
                         hover_data=['gzip'],
                         color='size',
                         color_continuous_scale='RdBu_r',
                         title='Dependency Bundle Size')

        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="#e2e8f0")
        )

        return fig.to_html(full_html=False, include_plotlyjs='cdn')

    def generate_report(self,
                        dependency_sizes: List[Dict[str, Any]],
                        unused_deps: List[str],
                        duplicates: Dict[str, List[str]],
                        suggestions: List[str]) -> str:
        """
        Generates a standalone HTML report with Premium UI.
        """
        treemap_html = self.generate_treemap(dependency_sizes)

        total_size = sum(d.get("size", 0) for d in dependency_sizes)
        formatted_total_size = self._format_bytes(total_size)

        unused_html = "".join([f"<li class='py-2 px-4 bg-gray-800 rounded mb-2 flex items-center'><span class='w-2 h-2 bg-red-500 rounded-full mr-3'></span>{dep}</li>" for dep in unused_deps])
        if not unused_deps:
            unused_html = "<li class='text-gray-500 italic'>No unused dependencies found. Great job!</li>"

        duplicates_html = ""
        if duplicates:
            for pkg, versions in duplicates.items():
                duplicates_html += f"<div class='mb-2'><span class='font-bold text-yellow-400'>{pkg}</span>: {', '.join(versions)}</div>"
        else:
            duplicates_html = "<div class='text-gray-500 italic'>No duplicates found.</div>"

        suggestions_html = "".join([f"<li class='py-3 border-b border-gray-700 last:border-0'>{s}</li>" for s in suggestions])
        if not suggestions:
            suggestions_html = "<li class='text-gray-500 italic'>No suggestions available.</li>"

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dependency Bloat Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; }}
        .gradient-text {{ background: linear-gradient(to right, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .card {{ background: #1e293b; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }}
        .animate-fade-in {{ animation: fadeIn 0.5s ease-out; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style>
</head>
<body class="min-h-screen p-6 md:p-12">
    <div class="max-w-6xl mx-auto animate-fade-in">
        <header class="mb-10 text-center">
            <h1 class="text-5xl font-bold mb-4"><span class="gradient-text">Dependency Bloat Reducer</span></h1>
            <p class="text-xl text-gray-400">Optimize your application's footprint</p>
        </header>

        <!-- Summary Stats -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <div class="card rounded-xl p-6 text-center">
                <div class="text-gray-400 mb-2">Total Bundle Size</div>
                <div class="text-4xl font-bold text-sky-400">{formatted_total_size}</div>
            </div>
            <div class="card rounded-xl p-6 text-center">
                <div class="text-gray-400 mb-2">Unused Packages</div>
                <div class="text-4xl font-bold text-red-400">{len(unused_deps)}</div>
            </div>
            <div class="card rounded-xl p-6 text-center">
                <div class="text-gray-400 mb-2">Duplicates</div>
                <div class="text-4xl font-bold text-yellow-400">{len(duplicates)}</div>
            </div>
        </div>

        <!-- Treemap -->
        <div class="card rounded-xl p-6 mb-10">
            <h2 class="text-2xl font-bold mb-6 border-b border-gray-700 pb-2">Size Visualization</h2>
            <div class="w-full overflow-hidden rounded-lg">
                {treemap_html}
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10">
            <!-- Unused Dependencies -->
            <div class="card rounded-xl p-6">
                <h2 class="text-2xl font-bold mb-4 text-red-400 flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                    Unused Dependencies
                </h2>
                <p class="text-gray-400 mb-4 text-sm">Packages listed in package.json but not imported in source code.</p>
                <ul class="max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                    {unused_html}
                </ul>
            </div>

            <!-- AI Suggestions -->
            <div class="card rounded-xl p-6">
                <h2 class="text-2xl font-bold mb-4 text-purple-400 flex items-center">
                    <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    AI Recommendations
                </h2>
                <p class="text-gray-400 mb-4 text-sm">Smart suggestions to reduce bloat.</p>
                <ul class="space-y-2 text-gray-300">
                    {suggestions_html}
                </ul>
            </div>
        </div>

        <!-- Duplicates -->
        <div class="card rounded-xl p-6 mt-10">
            <h2 class="text-2xl font-bold mb-4 text-yellow-400">Duplicate Packages</h2>
            <p class="text-gray-400 mb-4 text-sm">Packages with multiple versions installed (from lockfile).</p>
            <div class="bg-gray-900 rounded p-4 font-mono text-sm">
                {duplicates_html}
            </div>
        </div>

        <footer class="mt-12 text-center text-gray-500 text-sm">
            Generated by Dependency Bloat Reducer Agent
        </footer>
    </div>
</body>
</html>
        """

        output_path = os.path.join(self.output_dir, "report.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return output_path

    def _format_bytes(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
