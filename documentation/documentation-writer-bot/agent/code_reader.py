import os

class CodeReader:
    @staticmethod
    def read_file(file_path: str) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            return "" # Skip binary or non-utf8 files
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""
