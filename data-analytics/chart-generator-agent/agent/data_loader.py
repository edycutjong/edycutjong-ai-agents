import pandas as pd
import json

def load_data(file_path: str) -> pd.DataFrame:
    """Loads data from a CSV or JSON file into a Pandas DataFrame."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.json'):
        return pd.read_json(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")
