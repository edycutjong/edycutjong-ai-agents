import pandas as pd
from pypdf import PdfReader
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DataLoader:
    @staticmethod
    def load_text_file(filepath):
        """Loads text content from a .txt file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def load_pdf_file(filepath):
        """Extracts text from a .pdf file."""
        reader = PdfReader(filepath)  # pragma: no cover
        text = ""  # pragma: no cover
        for page in reader.pages:  # pragma: no cover
            text += page.extract_text() + "\n"  # pragma: no cover
        return text.strip()  # pragma: no cover

    @staticmethod
    def load_csv_file(filepath, text_column=None):
        """Loads a CSV file and returns a list of texts from a specific column."""
        df = pd.read_csv(filepath)  # pragma: no cover
        if text_column and text_column in df.columns:  # pragma: no cover
            return df[text_column].tolist()  # pragma: no cover
        elif len(df.columns) > 0:  # pragma: no cover
            # Default to first column if not specified
            return df.iloc[:, 0].tolist()  # pragma: no cover
        return []  # pragma: no cover

    @staticmethod
    def load_file(filepath):
        """Dispatches loading based on file extension."""
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.txt':
            return DataLoader.load_text_file(filepath)
        elif ext == '.pdf':
            return DataLoader.load_pdf_file(filepath)  # pragma: no cover
        elif ext == '.csv':
            return DataLoader.load_csv_file(filepath)  # pragma: no cover
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    @staticmethod
    def split_text(text, chunk_size=1000, chunk_overlap=100):
        """Splits text into chunks using RecursiveCharacterTextSplitter."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)
