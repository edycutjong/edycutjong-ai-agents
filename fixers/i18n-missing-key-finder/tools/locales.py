import json
import os
from typing import Dict, Any

class LocaleManager:
    """
    Manages loading and saving of JSON locale files.
    """

    def __init__(self, directory: str):
        self.directory = directory

    def load_locales(self) -> Dict[str, Dict[str, str]]:
        """
        Loads all JSON locale files from the directory.
        Returns a dict of {lang_code: {key: value}}.
        Keys are flattened (dot notation).
        """
        locales = {}
        if not os.path.exists(self.directory):
            return locales

        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                lang = os.path.splitext(filename)[0]
                filepath = os.path.join(self.directory, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        locales[lang] = self.flatten_dict(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON {filepath}: {e}")
                except Exception as e:
                    print(f"Error loading locale {filepath}: {e}")
        return locales

    def save_locale(self, lang: str, data: Dict[str, str], unflatten: bool = True):
        """
        Saves a locale to a JSON file.
        If unflatten is True, it converts dot notation keys back to nested objects.
        """
        filepath = os.path.join(self.directory, f"{lang}.json")
        try:
            content = self.unflatten_dict(data) if unflatten else data

            # Create directory if it doesn't exist
            os.makedirs(self.directory, exist_ok=True)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
                f.write('\n') # Add trailing newline
        except Exception as e:
            print(f"Error saving locale {lang}: {e}")

    @staticmethod
    def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, str]:
        """
        Flattens a nested dictionary.
        {'a': {'b': 'c'}} -> {'a.b': 'c'}
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(LocaleManager.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def unflatten_dict(d: Dict[str, str], sep: str = '.') -> Dict[str, Any]:
        """
        Unflattens a dictionary with dot notation keys.
        {'a.b': 'c'} -> {'a': {'b': 'c'}}
        """
        result = {}
        for key, value in d.items():
            parts = key.split(sep)
            target = result
            for i, part in enumerate(parts[:-1]):
                if part not in target:
                    target[part] = {}
                elif not isinstance(target[part], dict):
                     # Conflict: trying to use a value as a dict
                     # e.g. a='foo', a.b='bar'
                     # We overwrite 'a' with a dict to allow 'a.b'
                     target[part] = {}
                target = target[part]
            target[parts[-1]] = value
        return result
