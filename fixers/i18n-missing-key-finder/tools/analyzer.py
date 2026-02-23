from typing import Dict, Set, List, Any
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    missing_keys: Dict[str, Set[str]]
    unused_keys: Dict[str, Set[str]]

class Analyzer:
    """
    Analyzes keys to find missing and unused translations.
    """

    def __init__(self, source_keys: Set[str], locales: Dict[str, Dict[str, str]]):
        self.source_keys = source_keys
        self.locales = locales

    def analyze(self) -> AnalysisResult:
        missing = {}
        unused = {}

        for lang, keys in self.locales.items():
            locale_key_set = set(keys.keys())

            # Missing: in source but not in locale
            missing[lang] = self.source_keys - locale_key_set

            # Unused: in locale but not in source
            unused[lang] = locale_key_set - self.source_keys

        return AnalysisResult(missing_keys=missing, unused_keys=unused)
