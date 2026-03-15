import pytest
import os
import json
import pandas as pd
from agent.tools import (
    load_dataset, clean_dataset,
    format_openai, format_huggingface, validate_dataset, save_dataset,
    balance_dataset, get_stats
)

def test_load_dataset_json(tmp_path):
    data = [{"test": 1}]
    path = tmp_path / "test.json"
    with open(path, 'w') as f:
        json.dump(data, f)
    res = load_dataset.invoke({"filepath": str(path)})
    assert len(res) == 1

def test_load_dataset_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_dataset.invoke({"filepath": "does_not_exist.csv"})

def test_load_dataset_unsupported(tmp_path):
    path = tmp_path / "test.txt"
    with open(path, 'w') as f:
        f.write("test")
    with pytest.raises(ValueError, match="Unsupported file format"):
        load_dataset.invoke({"filepath": str(path)})

def test_clean_dataset_not_none():
    data = [{"valid": 123}]
    res = clean_dataset.invoke({"data": data})
    assert len(res) == 1
    assert res[0]["valid"] == 123

def test_format_openai_cases():
    data = [
        {"messages": [{"role": "user", "content": "hi"}]},
        {"instruction": "do this", "input": "input txt", "output": "done"},
        {"prompt": "say hi", "completion": "hi"},
        {"unknown": "format"}
    ]
    res = format_openai.invoke({"data": data})
    lines = res.split('\n')
    assert len(lines) == 3
    assert 'messages' in lines[0]

def test_format_huggingface():
    data = [{"test": 1}]
    res = format_huggingface.invoke({"data": data})
    assert len(res) == 1

def test_save_dataset_formats(tmp_path):
    # test string data
    path1 = tmp_path / "newdir" / "test1.txt"
    save_dataset.invoke({"data": "string data", "filepath": str(path1)})
    assert os.path.exists(path1)
    
    # test dict data saving as jsonl
    path2 = tmp_path / "test2.jsonl"
    save_dataset.invoke({"data": [{"a": 1}], "filepath": str(path2)})
    assert os.path.exists(path2)
    
    # test dict data saving as csv
    path3 = tmp_path / "test3.csv"
    save_dataset.invoke({"data": [{"a": 1}], "filepath": str(path3)})
    assert os.path.exists(path3)
    
    # test dict data saving as fallback json
    path4 = tmp_path / "test4.unknown"
    save_dataset.invoke({"data": [{"a": 1}], "filepath": str(path4)})
    assert os.path.exists(path4)

def test_validate_dataset_empty():
    res = validate_dataset.invoke({"data": []})
    assert len(res["issues"]) > 0

def test_balance_dataset_cases():
    data = [{"category": "A"}, {"category": "A"}, {"category": "B"}]
    # empty data
    assert balance_dataset.invoke({"data": [], "target_column": "x"}) == []
    # missing column
    assert len(balance_dataset.invoke({"data": data, "target_column": "missing"})) == 3
    # unknown method
    assert len(balance_dataset.invoke({"data": data, "target_column": "category", "method": "unknown"})) == 3

def test_get_stats_empty():
    res = get_stats.invoke({"data": []})
    assert res["count"] == 0
