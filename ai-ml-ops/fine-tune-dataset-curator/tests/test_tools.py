import pytest
import os
import json
import pandas as pd
from agent.tools import (
    load_dataset, clean_dataset, deduplicate_dataset,
    format_openai, format_huggingface, validate_dataset, save_dataset,
    split_dataset, balance_dataset, get_stats
)

# Sample data fixtures
@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame([
        {'instruction': 'Hello', 'output': 'Hi there'},
        {'instruction': 'Bye', 'output': 'Goodbye'}
    ])
    path = tmp_path / "test.csv"
    df.to_csv(path, index=False)
    return str(path)

@pytest.fixture
def sample_jsonl(tmp_path):
    data = [
        {'prompt': 'Hello', 'completion': 'Hi'},
        {'prompt': 'Test', 'completion': 'Passed'}
    ]
    path = tmp_path / "test.jsonl"
    with open(path, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')
    return str(path)

def test_load_dataset_csv(sample_csv):
    # load_dataset takes a single string argument 'filepath'
    data = load_dataset.invoke({"filepath": sample_csv})
    assert len(data) == 2
    assert 'instruction' in data[0]

def test_load_dataset_jsonl(sample_jsonl):
    data = load_dataset.invoke({"filepath": sample_jsonl})
    assert len(data) == 2
    assert 'prompt' in data[0]

def test_clean_dataset():
    raw_data = [
        {'text': '  clean me  '},
        {},
        {'text': None},
        {'valid': 'yes'}
    ]
    cleaned = clean_dataset.invoke({"data": raw_data})
    assert len(cleaned) == 2
    assert cleaned[0]['text'] == 'clean me'
    assert cleaned[1]['valid'] == 'yes'

def test_deduplicate_dataset():
    raw_data = [
        {'id': 1, 'text': 'unique'},
        {'id': 1, 'text': 'unique'},
        {'id': 2, 'text': 'different'}
    ]
    deduped = deduplicate_dataset.invoke({"data": raw_data})
    assert len(deduped) == 2

def test_format_openai():
    data = [{'instruction': 'Hi', 'output': 'Hello'}]
    jsonl_str = format_openai.invoke({"data": data})
    lines = jsonl_str.split('\n')
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert 'messages' in obj
    assert len(obj['messages']) == 3  # system, user, assistant

def test_save_dataset(tmp_path):
    data = [{'a': 1}, {'a': 2}]
    filepath = str(tmp_path / "saved.json")
    result = save_dataset.invoke({"data": data, "filepath": filepath})
    assert "saved successfully" in result
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        loaded = json.load(f)
    assert len(loaded) == 2

def test_validate_dataset():
    data = [{'text': 'valid'}, {}]
    report = validate_dataset.invoke({"data": data})
    assert report['total_entries'] == 2
    assert report['valid_entries'] == 1
    assert len(report['issues']) > 0

def test_split_dataset():
    data = [{'id': i} for i in range(10)]
    split = split_dataset.invoke({"data": data, "test_size": 0.2})
    assert len(split['train']) == 8
    assert len(split['validation']) == 2

def test_balance_dataset():
    data = [
        {'label': 'A', 'val': 1},
        {'label': 'A', 'val': 2},
        {'label': 'A', 'val': 3},
        {'label': 'B', 'val': 4}
    ]
    # Undersample A to match B (count 1)
    balanced = balance_dataset.invoke({"data": data, "target_column": 'label', "method": 'undersample'})
    assert len(balanced) == 2

    # Oversample B to match A (count 3)
    balanced_over = balance_dataset.invoke({"data": data, "target_column": 'label', "method": 'oversample'})
    assert len(balanced_over) == 6

def test_get_stats():
    data = [{'text': 'hello world'}]
    stats = get_stats.invoke({"data": data})
    assert stats['count'] == 1
    assert stats['approx_total_tokens'] > 0
