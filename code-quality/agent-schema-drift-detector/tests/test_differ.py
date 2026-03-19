def test_calculate_drift_basic():
    from lib.differ import calculate_drift
    
    expected = {
        "users": {
            "columns": {
                "id": {"nullable": False},
                "name": {"nullable": False},
                "missing_in_orm": {"nullable": True}
            }
        },
        "missing_table": {
            "columns": {"id": {"nullable": False}}
        }
    }
    
    actual = {
        "users": {
            "columns": {
                "id": {"nullable": False},
                "name": {"nullable": True}, # Nullability mismatch
                "shadow_col": {"nullable": False}
            }
        },
        "shadow_table": {
            "columns": {"id": {"nullable": False}}
        }
    }
    
    drifts = calculate_drift(expected, actual)
    
    assert len(drifts) == 3
    
    # Missing table
    assert "missing_table" in drifts
    assert drifts["missing_table"][0]["type"] == "missing_table"
    
    # Missing column
    assert any(d["type"] == "missing_column" and d["field"] == "missing_in_orm" for d in drifts["users"])
    
    # Nullability mismatch
    assert any(d["type"] == "nullability_mismatch" and d["field"] == "name" for d in drifts["users"])
    
    # Shadow table
    assert drifts["shadow_table"][0]["type"] == "shadow_table"
    
    # Shadow column
    assert any(d["type"] == "shadow_column" and d["field"] == "shadow_col" for d in drifts["users"])

def test_calculate_drift_ignores():
    from lib.differ import calculate_drift
    
    expected = {
        "_ignored_table": {},
        "users": {
            "columns": {
                "id": {"nullable": False},
                "created_at": {"nullable": False}
            }
        }
    }
    
    actual = {
        "_ignored_table2": {},
        "users": {
            "columns": {
                "id": {"nullable": False},
                "updated_at": {"nullable": False}
            }
        }
    }
    
    ignore_rules = {
        "tables": ["_ignored_table", "_ignored_table2"],
        "columns": ["created_at", "updated_at"]
    }
    
    drifts = calculate_drift(expected, actual, ignore_rules)
    assert not drifts # All differences should be ignored

def test_calculate_drift_ignore_types():
    from lib.differ import calculate_drift
    expected = {"users": {"columns": {"id": {"nullable": False}}}}
    actual = {"users": {"columns": {"id": {"nullable": True}}}}
    
    drifts = calculate_drift(expected, actual, {"drift_types": ["nullability_mismatch"]})
    assert not drifts
