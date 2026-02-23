import pandas as pd
import json
import os
import tiktoken
from typing import List, Dict, Any, Union
from langchain.tools import tool

@tool
def load_dataset(filepath: str) -> List[Dict[str, Any]]:
    """
    Loads a dataset from a CSV, JSON, or JSONL file.
    Returns a list of dictionaries.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
        return df.to_dict(orient='records')
    elif filepath.endswith('.json'):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif filepath.endswith('.jsonl'):
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        return data
    else:
        raise ValueError("Unsupported file format. Please use .csv, .json, or .jsonl")

@tool
def clean_dataset(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cleans the dataset by removing empty entries and stripping whitespace
    from string values.
    """
    cleaned_data = []
    for entry in data:
        # Check if entry is empty
        if not entry:
            continue

        cleaned_entry = {}
        has_content = False
        for k, v in entry.items():
            if isinstance(v, str):
                cleaned_val = v.strip()
                if cleaned_val:
                    cleaned_entry[k] = cleaned_val
                    has_content = True
            elif v is not None:
                cleaned_entry[k] = v
                has_content = True

        if has_content:
            cleaned_data.append(cleaned_entry)

    return cleaned_data

@tool
def deduplicate_dataset(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Removes exact duplicate entries from the dataset.
    """
    # Convert list of dicts to list of tuples to make them hashable for set
    seen = set()
    deduped_data = []
    for entry in data:
        # Sort keys to ensure consistent order
        entry_tuple = tuple(sorted((k, str(v)) for k, v in entry.items()))
        if entry_tuple not in seen:
            seen.add(entry_tuple)
            deduped_data.append(entry)
    return deduped_data

@tool
def format_openai(data: List[Dict[str, Any]], system_prompt: str = "You are a helpful assistant.") -> str:
    """
    Formats the dataset for OpenAI fine-tuning (JSONL with messages).
    Expects input data to have 'instruction'/'input'/'output' or similar keys,
    or already be in 'messages' format.

    Returns a string content of the JSONL file.
    """
    formatted_lines = []

    for entry in data:
        messages = []

        # If already in messages format
        if 'messages' in entry:
            messages = entry['messages']
        # Alpaca-like format (instruction, input, output)
        elif 'instruction' in entry and 'output' in entry:
            messages.append({"role": "system", "content": system_prompt})
            user_content = entry['instruction']
            if entry.get('input'):
                user_content += f"\n\nInput:\n{entry['input']}"
            messages.append({"role": "user", "content": user_content})
            messages.append({"role": "assistant", "content": entry['output']})
        # Simple prompt/completion pair
        elif 'prompt' in entry and 'completion' in entry:
            messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": entry['prompt']})
            messages.append({"role": "assistant", "content": entry['completion']})
        else:
            # Skip unrecognized formats or handle dynamically
            continue

        if messages:
            formatted_lines.append(json.dumps({"messages": messages}))

    return "\n".join(formatted_lines)

@tool
def format_huggingface(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Standardizes the dataset format for Hugging Face (e.g., ensures 'text' column or conversation format).
    This function currently ensures a consistent list of dicts which is compatible with `datasets.Dataset.from_list`.
    """
    # For now, we return the data as is, assuming it's already a list of dicts.
    # In a real scenario, we might want to flatten structures or rename columns.
    return data

@tool
def save_dataset(data: Union[List[Dict[str, Any]], str], filepath: str) -> str:
    """
    Saves the dataset to a file (JSON, JSONL, or CSV).
    If data is a string (e.g., JSONL content), writes it directly.
    """
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if isinstance(data, str):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(data)
    else:
        if filepath.endswith('.json'):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        elif filepath.endswith('.jsonl'):
            with open(filepath, 'w', encoding='utf-8') as f:
                for entry in data:
                    f.write(json.dumps(entry) + '\n')
        elif filepath.endswith('.csv'):
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False)
        else:
            # Default to JSON
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

    return f"Dataset saved successfully to {filepath}"

@tool
def validate_dataset(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validates the dataset checking for structure and basic quality.
    """
    report = {
        "total_entries": len(data),
        "valid_entries": 0,
        "issues": []
    }

    if not data:
        report["issues"].append("Dataset is empty.")
        return report

    valid_count = 0
    for idx, entry in enumerate(data):
        issues = []

        # Check for commonly required fields
        # Ideally, we'd know the target schema. Here we check if it's not empty.
        if not entry:
            issues.append(f"Entry {idx} is empty.")

        if not issues:
            valid_count += 1
        else:
            if len(report["issues"]) < 10: # Limit report size
                report["issues"].extend(issues)

    report["valid_entries"] = valid_count
    return report

@tool
def split_dataset(data: List[Dict[str, Any]], test_size: float = 0.2) -> Dict[str, List[Dict[str, Any]]]:
    """
    Splits the dataset into training and validation sets.
    """
    import random

    # Shuffle data to ensure random split
    shuffled_data = data.copy()
    random.shuffle(shuffled_data)

    split_index = int(len(shuffled_data) * (1 - test_size))
    train_data = shuffled_data[:split_index]
    val_data = shuffled_data[split_index:]

    return {
        "train": train_data,
        "validation": val_data
    }

@tool
def balance_dataset(data: List[Dict[str, Any]], target_column: str, method: str = "undersample") -> List[Dict[str, Any]]:
    """
    Balances the dataset based on a categorical column.
    Methods: 'undersample' (reduce majority class), 'oversample' (duplicate minority class).
    """
    if not data:
        return []

    df = pd.DataFrame(data)

    if target_column not in df.columns:
        # If column not found, return original
        return data

    counts = df[target_column].value_counts()
    min_count = counts.min()
    max_count = counts.max()

    balanced_df = pd.DataFrame()

    if method == "undersample":
        for label in counts.index:
            subset = df[df[target_column] == label]
            balanced_df = pd.concat([balanced_df, subset.sample(min_count)])
    elif method == "oversample":
        for label in counts.index:
            subset = df[df[target_column] == label]
            balanced_df = pd.concat([balanced_df, subset.sample(max_count, replace=True)])
    else:
        return data # Unknown method

    return balanced_df.to_dict(orient='records')

@tool
def get_stats(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates statistics for the dataset including token counts (estimate).
    """
    if not data:
        return {"count": 0, "status": "empty"}

    total_entries = len(data)

    # Token estimation (using tiktoken for gpt-3.5-turbo as a proxy)
    enc = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0

    keys = set()

    for entry in data:
        keys.update(entry.keys())
        text_representation = json.dumps(entry)
        total_tokens += len(enc.encode(text_representation))

    return {
        "count": total_entries,
        "approx_total_tokens": total_tokens,
        "avg_tokens_per_entry": total_tokens / total_entries if total_entries > 0 else 0,
        "columns": list(keys)
    }

# Export tools for the agent
DATASET_TOOLS = [
    load_dataset,
    clean_dataset,
    deduplicate_dataset,
    format_openai,
    format_huggingface,
    save_dataset,
    validate_dataset,
    split_dataset,
    balance_dataset,
    get_stats
]
