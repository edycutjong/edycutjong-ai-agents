def parse_schema_text(schema_text: str) -> str:
    """
    Simulates parsing or validating a schema text.
    In a real implementation, this could parse SQL or Prisma schema files.
    For now, it just cleans up whitespace and returns the text.
    """
    if not schema_text:
        return ""
    return schema_text.strip()

def validate_schema_input(schema_text: str) -> bool:
    """
    Simple validation to check if the schema text is not empty.
    """
    return len(parse_schema_text(schema_text)) > 0
