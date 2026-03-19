from typing import Dict, Any, List

def calculate_drift(expected: Dict[str, Any], actual: Dict[str, Any], ignore_rules: Dict[str, Any] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Compares the expected schema from migrations to the actual ORM models.
    Finds missing columns, shadow columns, orphaned tables, and missing tables.
    Also handles ignoring specified tables/columns.
    """
    drifts = {}
    ignore_rules = ignore_rules or {}
    ignore_tables = ignore_rules.get("tables", [])
    ignore_columns = ignore_rules.get("columns", [])
    ignore_drift_types = ignore_rules.get("drift_types", [])

    def add_drift(table: str, drift_type: str, details: str, field: str = None):
        if drift_type in ignore_drift_types:
            return
        if table not in drifts:
            drifts[table] = []
        drifts[table].append({
            "type": drift_type,
            "field": field,
            "details": details
        })

    # Find orphaned tables (in migration but missing in ORM)
    for table_name, schema_data in expected.items():
        if table_name in ignore_tables:
            continue
            
        if table_name not in actual:
            add_drift(table_name, "missing_table", f"Table '{table_name}' is in migrations but missing in ORM.")
            continue
            
        expected_cols = schema_data.get("columns", {})
        actual_cols = actual[table_name].get("columns", {})
        
        # Check columns expected -> actual (missing in ORM)
        for col_name, col_data in expected_cols.items():
            if col_name in ignore_columns:
                continue
                
            if col_name not in actual_cols:
                add_drift(table_name, "missing_column", f"Column '{col_name}' is in migrations but missing in ORM model.", col_name)
            else:
                # Check nullability
                if col_data["nullable"] != actual_cols[col_name]["nullable"]:
                    e_null = "NULL" if col_data["nullable"] else "NOT NULL"
                    a_null = "NULL" if actual_cols[col_name]["nullable"] else "NOT NULL"
                    add_drift(table_name, "nullability_mismatch", f"Column '{col_name}' nullability mismatch (Migration: {e_null}, ORM: {a_null})", col_name)

    # Find shadow tables and columns (in ORM but missing in migrations)
    for table_name, model_data in actual.items():
        if table_name in ignore_tables:
            continue
            
        if table_name not in expected:
            add_drift(table_name, "shadow_table", f"Table '{table_name}' is in ORM but missing in migrations.")
            continue
            
        expected_cols = expected[table_name].get("columns", {})
        actual_cols = model_data.get("columns", {})
        
        for col_name in actual_cols:
            if col_name in ignore_columns:
                continue
                
            if col_name not in expected_cols:
                add_drift(table_name, "shadow_column", f"Column '{col_name}' is in ORM but missing in migrations.", col_name)

    return drifts
