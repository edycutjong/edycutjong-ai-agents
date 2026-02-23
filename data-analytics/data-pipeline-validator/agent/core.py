import pandas as pd
import numpy as np
from typing import Dict, Any, Union, Optional
import io

class DataValidator:
    def __init__(self):
        self.report = {}

    def load_data(self, source: Union[str, io.BytesIO], file_type: str = "csv") -> pd.DataFrame:
        """
        Loads data from a file path or file-like object.
        """
        try:
            if file_type == "csv":
                return pd.read_csv(source)
            elif file_type == "parquet":
                return pd.read_parquet(source)
            elif file_type in ["xlsx", "excel"]:
                return pd.read_excel(source)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")

    def validate_counts(self, source_df: pd.DataFrame, dest_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compares row counts between source and destination.
        """
        source_count = len(source_df)
        dest_count = len(dest_df)
        match = source_count == dest_count

        return {
            "source_count": source_count,
            "dest_count": dest_count,
            "match": match,
            "diff": dest_count - source_count
        }

    def validate_schema(self, source_df: pd.DataFrame, dest_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compares columns and data types.
        """
        source_cols = set(source_df.columns)
        dest_cols = set(dest_df.columns)

        missing_in_dest = list(source_cols - dest_cols)
        extra_in_dest = list(dest_cols - source_cols)

        common_cols = source_cols.intersection(dest_cols)
        type_mismatches = {}

        for col in common_cols:
            source_type = str(source_df[col].dtype)
            dest_type = str(dest_df[col].dtype)
            if source_type != dest_type:
                type_mismatches[col] = {"source": source_type, "dest": dest_type}

        return {
            "missing_columns": missing_in_dest,
            "extra_columns": extra_in_dest,
            "type_mismatches": type_mismatches,
            "schema_match": not missing_in_dest and not type_mismatches # Extra columns might be okay depending on pipeline
        }

    def check_data_quality(self, df: pd.DataFrame, label: str = "data") -> Dict[str, Any]:
        """
        Checks for nulls and duplicates.
        """
        null_counts = df.isnull().sum().to_dict()
        total_rows = len(df)
        duplicate_count = df.duplicated().sum()

        # Filter null counts to only show columns with nulls
        null_counts = {k: v for k, v in null_counts.items() if v > 0}

        return {
            "label": label,
            "total_rows": total_rows,
            "null_columns": null_counts,
            "duplicate_rows": int(duplicate_count),
            "duplicate_ratio": float(duplicate_count / total_rows) if total_rows > 0 else 0
        }

    def compare_distributions(self, source_df: pd.DataFrame, dest_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compares basic stats for numeric columns.
        """
        numeric_cols_source = source_df.select_dtypes(include=[np.number]).columns
        numeric_cols_dest = dest_df.select_dtypes(include=[np.number]).columns

        common_numeric = set(numeric_cols_source).intersection(set(numeric_cols_dest))
        stats_diff = {}

        for col in common_numeric:
            s_stats = source_df[col].describe()
            d_stats = dest_df[col].describe()

            # Simple check: mean difference percentage
            mean_diff = 0
            if s_stats['mean'] != 0:
                mean_diff = abs((d_stats['mean'] - s_stats['mean']) / s_stats['mean'])
            elif d_stats['mean'] != 0:
                mean_diff = 1.0 # Source is 0, dest is not

            stats_diff[col] = {
                "source_mean": float(s_stats['mean']),
                "dest_mean": float(d_stats['mean']),
                "mean_diff_pct": float(mean_diff)
            }

        return stats_diff

    def run_full_validation(self, source_df: pd.DataFrame, dest_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Runs all validation checks.
        """
        results = {
            "row_counts": self.validate_counts(source_df, dest_df),
            "schema": self.validate_schema(source_df, dest_df),
            "source_quality": self.check_data_quality(source_df, "source"),
            "dest_quality": self.check_data_quality(dest_df, "destination"),
            "distributions": self.compare_distributions(source_df, dest_df)
        }
        self.report = results
        return results
