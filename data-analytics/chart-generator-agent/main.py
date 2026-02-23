import argparse
import sys
import pandas as pd
import os
from agent.data_loader import load_data
from agent.llm_engine import LLMEngine
from agent.python_plotter import generate_python_chart
from agent.js_generator import generate_js_chart
from config import Config

def main():
    parser = argparse.ArgumentParser(description="AI Chart Generator Agent")
    parser.add_argument("file_path", help="Path to the CSV or JSON data file")
    parser.add_argument("query", help="Natural language query for the chart")
    parser.add_argument("--output", default=Config.OUTPUT_DIR, help="Output directory")

    args = parser.parse_args()

    try:
        # 1. Load Data
        print(f"Loading data from {args.file_path}...")
        df = load_data(args.file_path)

        # 2. Analyze Schema
        columns = {col: str(df[col].dtype) for col in df.columns}
        print(f"Data Schema: {columns}")

        # 3. Process Request with LLM
        print("Processing request with LLM...")
        llm_engine = LLMEngine()
        chart_config = llm_engine.process_request(columns, args.query)

        print(f"Generated Configuration: {chart_config}")

        # 4. Generate Chart
        tool = chart_config.get("tool")
        chart_type = chart_config.get("chart_type")
        x_col = chart_config.get("x_column")
        y_col = chart_config.get("y_column")
        title = chart_config.get("title")

        # Ensure output directory exists
        os.makedirs(args.output, exist_ok=True)

        if tool == "python":
            output_file = f"{args.output}/chart.png"
            generate_python_chart(df, chart_type, x_col, y_col, title, output_file)
            print(f"Chart saved to {output_file}")

        elif tool == "js":
            output_file = f"{args.output}/chart.html"
            generate_js_chart(df, chart_type, x_col, y_col, title, output_file)
            print(f"Interactive chart saved to {output_file}")

        else:
            print(f"Unknown tool: {tool}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
