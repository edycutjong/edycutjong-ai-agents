import re
import os
from pathlib import Path
from typing import Dict, Any, List

def parse_migrations(path: Path, dialect: str, existing_schema: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Parses SQL migration files to build an expected schema representation.
    This is a simplified heuristic parser to extract CREATE TABLE statements 
    and ALTER TABLE ADD COLUMN statements.
    """
    schema = existing_schema or {}

    files_to_parse = []
    if path.is_file():
        files_to_parse.append(path)
    elif path.is_dir():
        files_to_parse = sorted([f for f in path.rglob("*.sql")])
    
    for file_path in files_to_parse:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # Very basic extraction logic forCREATE TABLE
            # Match: CREATE TABLE [IF NOT EXISTS] "table_name" (
            create_tables = re.finditer(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([\"\w\.]+)\s*\((.*?)\);", content, re.IGNORECASE | re.DOTALL)
            for match in create_tables:
                table_name_raw = match.group(1).replace('"', '')
                table_name = table_name_raw.split(".")[-1] # Remove schema prefix if any
                columns_str = match.group(2)
                
                if table_name not in schema:
                    schema[table_name] = {"columns": {}, "indices": []}
                
                # Split columns and extract basic info
                col_defs = [c.strip() for c in columns_str.split(",") if c.strip()]
                for col_def in col_defs:
                    if col_def.upper().startswith(("PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CONSTRAINT", "INDEX")):
                        continue # pragma: no cover
                    
                    parts = col_def.split()
                    if not parts: # pragma: no cover
                        continue
                    
                    col_name = parts[0].strip('"`[]')
                    col_type = parts[1].upper() if len(parts) > 1 else "UNKNOWN"
                    is_nullable = "NOT NULL" not in col_def.upper()
                    
                    schema[table_name]["columns"][col_name] = {
                        "type": col_type,
                        "nullable": is_nullable
                    }
            
            # Very basic ALTER TABLE ADD COLUMN extraction
            # Match: ALTER TABLE "table_name" ADD COLUMN "col_name" type
            alter_tables = re.finditer(r"ALTER\s+TABLE\s+([\"\w\.]+)\s+ADD\s+(?:COLUMN\s+)?[\"`]?(\w+)[\"`]?(?:\s+(.*?))?(?:;|$)", content, re.IGNORECASE)
            for match in alter_tables:
                table_name_raw = match.group(1).replace('"', '')
                table_name = table_name_raw.split(".")[-1]
                col_name = match.group(2)
                col_def_rest = match.group(3) or ""
                
                parts = col_def_rest.split()
                col_type = parts[0].upper() if parts else "UNKNOWN"
                is_nullable = "NOT NULL" not in col_def_rest.upper()
                
                if table_name not in schema: # pragma: no cover
                    schema[table_name] = {"columns": {}, "indices": []}
                    
                schema[table_name]["columns"][col_name] = {
                    "type": col_type,
                    "nullable": is_nullable
                }

    return schema
