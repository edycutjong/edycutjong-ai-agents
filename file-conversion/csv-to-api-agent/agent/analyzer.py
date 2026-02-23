import pandas as pd
from typing import Dict, Any, List

class Analyzer:
    """
    Analyzes a CSV file to infer its schema (column names and data types).
    """

    def __init__(self, file_path_or_buffer: Any):
        """
        Initializes the Analyzer with a file path or file-like object.
        """
        try:
            # First, read without date parsing
            self.df = pd.read_csv(file_path_or_buffer)

            # Try to convert object columns to datetime if possible
            for col in self.df.columns:
                if self.df[col].dtype == 'object':
                    try:
                        # Attempt to parse as datetime, but don't force it if it creates NaTs for valid strings
                        # We use errors='raise' to catch non-datetimes
                        # However, to_datetime with errors='raise' will fail if *any* value is not a date.
                        # We want to check if the *column* is effectively a date.
                        # A better heuristic might be needed, but for now let's try a sample.
                        sample = self.df[col].dropna().head(10)
                        if not sample.empty:
                            pd.to_datetime(sample, errors='raise')
                            # If successful, convert the whole column
                            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    except (ValueError, TypeError):
                        pass # Keep as object (string)
        except Exception as e:
            # Reraise or handle?
            # If it's empty or bad format, pandas will raise
            raise ValueError(f"Failed to read CSV: {e}")

    def get_preview(self, rows: int = 5) -> pd.DataFrame:
        """Returns a preview of the dataframe."""
        return self.df.head(rows)

    def infer_schema(self) -> List[Dict[str, str]]:
        """
        Infers the schema of the CSV.
        Returns a list of dictionaries, each containing 'name' and 'type'.
        Maps pandas dtypes to Python/SQLAlchemy compatible types.
        """
        schema = []
        for column in self.df.columns:
            dtype = self.df[column].dtype
            col_type = "str"  # Default

            if pd.api.types.is_integer_dtype(dtype):
                col_type = "int"
            elif pd.api.types.is_float_dtype(dtype):
                col_type = "float"
            elif pd.api.types.is_bool_dtype(dtype):
                col_type = "bool"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                col_type = "datetime"

            # Simple sanitization for column names to be valid python identifiers
            safe_name = "".join([c if c.isalnum() else "_" for c in str(column)]).lower()
            # Remove leading/trailing underscores and ensure not empty
            safe_name = safe_name.strip("_")
            if not safe_name:
                safe_name = f"col_{self.df.columns.get_loc(column)}"
            elif safe_name[0].isdigit():
                safe_name = f"col_{safe_name}"

            # Avoid duplicates
            existing_names = [s['name'] for s in schema]
            original_safe_name = safe_name
            counter = 1
            while safe_name in existing_names:
                safe_name = f"{original_safe_name}_{counter}"
                counter += 1

            schema.append({
                "original_name": str(column),
                "name": safe_name,
                "type": col_type
            })
        return schema
