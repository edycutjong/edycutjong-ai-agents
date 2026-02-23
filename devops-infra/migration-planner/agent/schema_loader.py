from pathlib import Path

class SchemaLoader:
    def load_from_file(self, filepath: str) -> str:
        """Loads schema content from a SQL/DDL file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {filepath}")

        with open(path, "r") as f:
            return f.read()

    def load_from_directory(self, directory: str) -> str:
        """Loads all .sql files from a directory and concatenates them."""
        path = Path(directory)
        if not path.exists() or not path.is_dir():
            raise NotADirectoryError(f"Directory not found: {directory}")

        schema_content = []
        for file in sorted(path.glob("*.sql")):
             with open(file, "r") as f:
                schema_content.append(f"-- File: {file.name}\n" + f.read())

        return "\n\n".join(schema_content)
