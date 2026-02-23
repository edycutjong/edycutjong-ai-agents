import os
from .utils import logger

def insert_docstring(filepath: str, lineno: int, docstring: str) -> bool:
    """
    Inserts a docstring into a file at the specified line number.

    Args:
        filepath: Path to the file.
        lineno: The line number where the function/class definition starts (1-based).
        docstring: The docstring content to insert.

    Returns:
        True if successful, False otherwise.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Adjust for 0-based indexing
        start_index = lineno - 1

        if start_index < 0 or start_index >= len(lines):
            return False

        # Find the line with the colon which ends the definition header
        # This handles multi-line definitions
        insertion_index = start_index
        while insertion_index < len(lines):
            # Strip comments and whitespace
            line = lines[insertion_index].split('#', 1)[0].strip()
            if line.endswith(':'):
                break
            insertion_index += 1

        if insertion_index >= len(lines):
            return False

        # Determine indentation
        # We look at the indentation of the definition line
        def_line = lines[start_index]
        indentation = len(def_line) - len(def_line.lstrip())
        docstring_indentation = " " * (indentation + 4)

        # Format the docstring
        formatted_docstring = f'{docstring_indentation}"""\n'
        for line in docstring.split('\n'):
            if line.strip():
                formatted_docstring += f'{docstring_indentation}{line}\n'
            else:
                formatted_docstring += '\n'
        formatted_docstring += f'{docstring_indentation}"""\n'

        # Insert the docstring
        lines.insert(insertion_index + 1, formatted_docstring)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return True

    except Exception as e:
        logger.error(f"Error inserting docstring in {filepath}: {e}")
        return False
