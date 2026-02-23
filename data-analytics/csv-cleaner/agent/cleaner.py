"""Core CSV cleaning engine."""
from __future__ import annotations

import csv
import io
import logging
from dataclasses import dataclass, field
from datetime import datetime

import pandas as pd
import chardet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CleaningReport:
    """Report of all cleaning actions taken."""
    original_rows: int = 0
    final_rows: int = 0
    original_columns: int = 0
    encoding_detected: str = ""
    encoding_fixed: bool = False
    duplicates_removed: int = 0
    missing_values_filled: int = 0
    whitespace_trimmed: int = 0
    type_fixes: int = 0
    date_standardized: int = 0
    actions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "original_rows": self.original_rows,
            "final_rows": self.final_rows,
            "original_columns": self.original_columns,
            "rows_removed": self.original_rows - self.final_rows,
            "encoding_detected": self.encoding_detected,
            "encoding_fixed": self.encoding_fixed,
            "duplicates_removed": self.duplicates_removed,
            "missing_values_filled": self.missing_values_filled,
            "whitespace_trimmed": self.whitespace_trimmed,
            "type_fixes": self.type_fixes,
            "date_standardized": self.date_standardized,
            "actions": self.actions,
        }

    def to_markdown(self) -> str:
        lines = [
            "# CSV Cleaning Report",
            "",
            f"**Original rows:** {self.original_rows}",
            f"**Final rows:** {self.final_rows}",
            f"**Rows removed:** {self.original_rows - self.final_rows}",
            f"**Columns:** {self.original_columns}",
            "",
            "## Actions Taken",
        ]
        for i, action in enumerate(self.actions, 1):
            lines.append(f"{i}. {action}")
        return "\n".join(lines)


class CSVCleaner:
    """Clean messy CSV files: encoding, duplicates, missing values, types, whitespace."""

    def __init__(self):
        self.report = CleaningReport()

    def detect_encoding(self, raw_bytes: bytes) -> str:
        """Detect file encoding using chardet."""
        result = chardet.detect(raw_bytes)
        encoding = result.get("encoding", "utf-8") or "utf-8"
        self.report.encoding_detected = encoding
        return encoding

    def load_csv(self, filepath: str = None, content: str = None, raw_bytes: bytes = None) -> pd.DataFrame:
        """Load CSV from file path, string content, or raw bytes."""
        if raw_bytes is not None:
            encoding = self.detect_encoding(raw_bytes)
            content = raw_bytes.decode(encoding, errors="replace")
            if encoding.lower() not in ("utf-8", "ascii"):
                self.report.encoding_fixed = True
                self.report.actions.append(f"Converted encoding from {encoding} to UTF-8")

        if content is not None:
            df = pd.read_csv(io.StringIO(content))
        elif filepath is not None:
            with open(filepath, "rb") as f:
                return self.load_csv(raw_bytes=f.read())
        else:
            raise ValueError("Provide filepath, content, or raw_bytes")

        self.report.original_rows = len(df)
        self.report.original_columns = len(df.columns)
        return df

    def trim_whitespace(self, df: pd.DataFrame) -> pd.DataFrame:
        """Strip leading/trailing whitespace from all string columns and column names."""
        count = 0
        # Clean column names
        df.columns = df.columns.str.strip()

        # Clean string values
        for col in df.select_dtypes(include=["object"]).columns:
            original = df[col].copy()
            df[col] = df[col].str.strip()
            changed = (original != df[col]).sum()
            count += changed

        if count > 0:
            self.report.whitespace_trimmed = int(count)
            self.report.actions.append(f"Trimmed whitespace in {count} cells")

        return df

    def remove_duplicates(self, df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
        """Remove duplicate rows."""
        before = len(df)
        df = df.drop_duplicates(subset=subset).reset_index(drop=True)
        removed = before - len(df)

        if removed > 0:
            self.report.duplicates_removed = removed
            self.report.actions.append(f"Removed {removed} duplicate rows")

        return df

    def handle_missing_values(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """Handle missing values.

        Args:
            strategy: 'drop' (remove rows), 'fill_mean' (numeric), 'fill_mode', 'fill_empty'
        """
        missing_before = int(df.isnull().sum().sum())

        if missing_before == 0:
            return df

        if strategy == "drop":
            df = df.dropna().reset_index(drop=True)
        elif strategy == "fill_mean":
            for col in df.select_dtypes(include=["number"]).columns:
                df[col] = df[col].fillna(df[col].mean())
            # Fill non-numeric with empty string
            df = df.fillna("")
        elif strategy == "fill_mode":
            for col in df.columns:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])
        elif strategy == "fill_empty":
            df = df.fillna("")
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        missing_after = int(df.isnull().sum().sum())
        filled = missing_before - missing_after

        if filled > 0:
            self.report.missing_values_filled = filled
            self.report.actions.append(f"Handled {filled} missing values (strategy: {strategy})")

        return df

    def standardize_dates(self, df: pd.DataFrame, columns: list[str] | None = None,
                         target_format: str = "%Y-%m-%d") -> pd.DataFrame:
        """Standardize date columns to a consistent format."""
        count = 0
        date_cols = columns or []

        if not date_cols:
            # Auto-detect date columns
            for col in df.select_dtypes(include=["object"]).columns:
                try:
                    pd.to_datetime(df[col], format="mixed")
                    date_cols.append(col)
                except (ValueError, TypeError):
                    pass

        for col in date_cols:
            try:
                parsed = pd.to_datetime(df[col], format="mixed")
                df[col] = parsed.dt.strftime(target_format)
                count += 1
            except (ValueError, TypeError):
                pass

        if count > 0:
            self.report.date_standardized = count
            self.report.actions.append(f"Standardized {count} date column(s) to {target_format}")

        return df

    def fix_column_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attempt to convert columns to appropriate types."""
        count = 0
        for col in df.select_dtypes(include=["object"]).columns:
            # Try numeric
            try:
                df[col] = pd.to_numeric(df[col])
                count += 1
                continue
            except (ValueError, TypeError):
                pass

        if count > 0:
            self.report.type_fixes = count
            self.report.actions.append(f"Fixed types for {count} column(s)")

        return df

    def clean(self, df: pd.DataFrame, missing_strategy: str = "drop",
              remove_dupes: bool = True, fix_types: bool = True,
              standardize_dates_flag: bool = True) -> pd.DataFrame:
        """Run full cleaning pipeline."""
        logger.info("Starting CSV cleaning pipeline...")

        # 1. Trim whitespace
        df = self.trim_whitespace(df)

        # 2. Remove duplicates
        if remove_dupes:
            df = self.remove_duplicates(df)

        # 3. Handle missing values
        df = self.handle_missing_values(df, strategy=missing_strategy)

        # 4. Standardize dates
        if standardize_dates_flag:
            df = self.standardize_dates(df)

        # 5. Fix column types
        if fix_types:
            df = self.fix_column_types(df)

        self.report.final_rows = len(df)
        logger.info(f"Cleaning complete: {self.report.original_rows} → {self.report.final_rows} rows")

        return df

    def save(self, df: pd.DataFrame, filepath: str, encoding: str = "utf-8"):
        """Save cleaned DataFrame to CSV."""
        df.to_csv(filepath, index=False, encoding=encoding)
        self.report.actions.append(f"Saved to {filepath}")

    def get_quality_summary(self, df: pd.DataFrame) -> dict:
        """Generate a data quality summary for the DataFrame."""
        total_cells = df.shape[0] * df.shape[1]
        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "total_cells": total_cells,
            "missing_cells": missing,
            "missing_percent": round((missing / total_cells) * 100, 2) if total_cells > 0 else 0,
            "duplicate_rows": duplicates,
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        }
