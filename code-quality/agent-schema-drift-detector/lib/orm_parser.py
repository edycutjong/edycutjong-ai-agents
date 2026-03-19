import re
from pathlib import Path
from typing import Dict, Any

def parse_orm_models(path: Path, existing_models: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Parses ORM definition files (.prisma, .ts drizzle, .py sqlalchemy) to build the actual model representation.
    """
    models = existing_models or {}
    
    files_to_parse = []
    if path.is_file():
        files_to_parse.append(path)
    elif path.is_dir():
        for ext in ["*.prisma", "*.ts", "*.py"]:
            files_to_parse.extend(path.rglob(ext))
            
    for file_path in files_to_parse:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            ext = file_path.suffix.lower()
            
            if ext == ".prisma":
                models = _parse_prisma(content, models)
            elif ext == ".ts":
                models = _parse_drizzle(content, models)
            elif ext == ".py":
                models = _parse_sqlalchemy(content, models)
                
    return models

def _parse_prisma(content: str, models: Dict[str, Any]) -> Dict[str, Any]:
    # Match: model ModelName { ... }
    blocks = re.finditer(r"model\s+(\w+)\s+\{(.*?)\}", content, re.DOTALL)
    for match in blocks:
        model_name = match.group(1).lower() # Prisma usually lowercases table names, or we map it
        body = match.group(2)
        
        # Check for @@map("actual_table_name")
        map_match = re.search(r"@@map\([\"'](.*?)[\"']\)", body)
        table_name = map_match.group(1) if map_match else model_name
        
        if table_name not in models:
            models[table_name] = {"columns": {}, "indices": []}
            
        lines = [line.strip() for line in body.split("\n") if line.strip() and not line.strip().startswith("//")]
        for line in lines:
            if line.startswith("@@"): continue # Model-level attributes
            parts = line.split()
            if len(parts) >= 2:
                col_name = parts[0]
                col_type = parts[1]
                
                # Check for relation fields, typically they have relations like @relation
                if "@relation" in line or col_type.istitle(): 
                    # Relation fields in prisma are usually capitalized Model names
                    if not parts[1].endswith("?") and parts[1] not in ["String", "Int", "Boolean", "Float", "DateTime", "Json", "Bytes", "Decimal", "BigInt"]:
                        continue # Skip relation fields

                # prisma uses Int? for nullable
                is_nullable = col_type.endswith("?")
                clean_type = col_type.replace("?", "")
                
                # Try to find @map("actual_column_name")
                col_map_match = re.search(r"@map\([\"'](.*?)[\"']\)", line)
                actual_col_name = col_map_match.group(1) if col_map_match else col_name
                
                models[table_name]["columns"][actual_col_name] = {
                    "type": clean_type.upper(),
                    "nullable": is_nullable
                }
    return models

def _parse_drizzle(content: str, models: Dict[str, Any]) -> Dict[str, Any]:
    # Basic matching for Drizzle: export const users = pgTable('users', { id: serial('id'), ... })
    blocks = re.finditer(r"(?:pgTable|mysqlTable|sqliteTable)\s*\(\s*[\"'](.*?)[\"']\s*,\s*\{(.*?)\}\s*\)", content, re.DOTALL)
    for match in blocks:
        table_name = match.group(1)
        body = match.group(2)
        
        if table_name not in models:
            models[table_name] = {"columns": {}, "indices": []}
            
        # Very crude splitting by formatting
        col_matches = re.finditer(r"(\w+)\s*:\s*\w+\s*\([\"'](.*?)[\"']\)?(.*?),", body + ",", re.DOTALL)
        for cm in col_matches:
            actual_col_name = cm.group(2) # The DB name passed directly e.g. text('user_name')
            rest = cm.group(3)
            
            is_nullable = ".notNull()" not in rest
            
            models[table_name]["columns"][actual_col_name] = {
                "type": "UNKNOWN", # Simplification as type mapping in drizzle is complex
                "nullable": is_nullable
            }
            
    return models

def _parse_sqlalchemy(content: str, models: Dict[str, Any]) -> Dict[str, Any]:
    # Basic matching for SQLAlchemy models
    # class User(Base): __tablename__ = 'users' id = Column(Integer, primary_key=True)
    blocks = re.split(r"class\s+\w+\(.*?\):", content)
    for block in blocks[1:]:
        table_match = re.search(r"__tablename__\s*=\s*[\"'](.*?)[\"']", block)
        if not table_match:
            continue
            
        table_name = table_match.group(1)
        if table_name not in models:
            models[table_name] = {"columns": {}, "indices": []}
            
        col_matches = re.finditer(r"(\w+)\s*=\s*(?:Column|mapped_column)\s*\((.*?)\)", block)
        for cm in col_matches:
            col_var = cm.group(1)
            args = cm.group(2)
            
            # If the first arg is a string, it's the DB column name, otherwise use the variable name
            name_match = re.match(r"[\"'](.*?)[\"']", args)
            actual_col_name = name_match.group(1) if name_match else col_var
            
            is_nullable = "nullable=False" not in args
            
            models[table_name]["columns"][actual_col_name] = {
                "type": "UNKNOWN", # Simplification
                "nullable": is_nullable
            }
    return models
