import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

class SchemaParser:
    """
    Parses SQL CREATE TABLE statements to extract schema information.
    """

    def parse(self, sql_content: str) -> dict:
        """
        Parses SQL content and returns a dictionary representation of the schema.

        Args:
            sql_content (str): The SQL content containing CREATE TABLE statements.

        Returns:
            dict: A dictionary where keys are table names and values are table details (columns, types, constraints).
        """
        parsed = sqlparse.parse(sql_content)
        schema = {}

        for statement in parsed:
            if statement.get_type() == 'CREATE':
                table_info = self._extract_table_info(statement)
                if table_info:
                    schema[table_info['name']] = table_info

        return schema

    def _extract_table_info(self, statement):
        """
        Extracts table name and columns from a CREATE TABLE statement.
        """
        table_name = None
        columns = []

        # Simple extraction logic - this can be enhanced for complex SQL
        # Using string manipulation for simplicity as sqlparse tree traversal for DDL is complex

        # Convert statement to string and remove comments
        stmt_str = str(statement)

        # Extract table name
        # Looking for "CREATE TABLE [IF NOT EXISTS] table_name"
        tokens = [t for t in statement.tokens if not t.is_whitespace]

        create_idx = -1
        table_idx = -1

        for i, token in enumerate(tokens):
            if token.match(Keyword.DDL, 'CREATE'):
                create_idx = i
            if token.match(Keyword, 'TABLE'):
                table_idx = i
                break

        if create_idx == -1 or table_idx == -1:
            return None

        # The table name should be the next identifier
        identifier = tokens[table_idx + 1]

        # Handle "IF NOT EXISTS"
        if identifier.match(Keyword, 'IF NOT EXISTS'):
             identifier = tokens[table_idx + 2]

        table_name = identifier.get_real_name()

        # Extract columns
        # Columns are usually inside parentheses after table name
        # We find the content inside the first pair of parentheses

        stmt_str_normalized = ' '.join(stmt_str.split()) # normalize whitespace
        start_paren = stmt_str_normalized.find('(')
        end_paren = stmt_str_normalized.rfind(')')

        if start_paren != -1 and end_paren != -1:
            column_defs = stmt_str_normalized[start_paren+1:end_paren].split(',')
            for col_def in column_defs:
                col_def = col_def.strip()
                if not col_def:
                    continue

                # Check if it's a constraint (PRIMARY KEY, FOREIGN KEY, etc.)
                upper_col_def = col_def.upper()
                if upper_col_def.startswith("PRIMARY KEY") or \
                   upper_col_def.startswith("FOREIGN KEY") or \
                   upper_col_def.startswith("CONSTRAINT") or \
                   upper_col_def.startswith("UNIQUE") or \
                   upper_col_def.startswith("KEY") or \
                   upper_col_def.startswith("INDEX"):
                    # For now, we skip parsing explicit constraint lines and focus on column definitions
                    # Advanced parsing would handle these to build relationships
                    continue

                parts = col_def.split()
                if len(parts) >= 2:
                    col_name = parts[0].strip('"`[]')
                    col_type = parts[1]
                    # basic constraints
                    is_pk = "PRIMARY KEY" in upper_col_def
                    is_not_null = "NOT NULL" in upper_col_def

                    columns.append({
                        "name": col_name,
                        "type": col_type,
                        "pk": is_pk,
                        "not_null": is_not_null,
                        "raw": col_def
                    })

        return {
            "name": table_name,
            "columns": columns
        }
