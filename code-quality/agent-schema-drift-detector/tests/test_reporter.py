def test_formatters():
    from lib.reporter import format_json, format_markdown, format_table
    import json
    
    drifts = {
        "users": [
            {"type": "missing_column", "field": "age", "details": "missing age"}
        ]
    }
    
    # JSON
    json_out = format_json(drifts)
    assert "missing_column" in json_out
    assert json.loads(json_out) == drifts
    
    # Markdown
    md_out = format_markdown(drifts)
    assert "## Schema Drift Report" in md_out
    assert "`users`" in md_out
    assert "missing_column" in md_out
    
    # Markdown empty
    md_empty = format_markdown({})
    assert "No schema drift detected" in md_empty
    
    # Table
    table_out = format_table(drifts)
    assert table_out.title == "Schema Drift Report"
    assert len(table_out.rows) == 1
    
    # Table empty
    table_empty = format_table({})
    assert table_empty.title == "Schema Drift Report"
    assert len(table_empty.rows) == 1
