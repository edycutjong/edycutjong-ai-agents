from pathlib import Path
from typing import List, Dict, Set, Tuple

class DependencyGraph:
    """
    Manages the relationship between assets and their usage in the codebase.
    """

    def __init__(self, assets: List[Path], references: Dict[Path, Set[Path]]):
        self.assets = assets
        self.references = references
        self.unused_assets = []
        self.used_assets = []
        self._analyze()

    def _analyze(self):
        """
        Categorizes assets into used and unused.
        """
        self.unused_assets = []
        self.used_assets = []

        for asset in self.assets:
            if asset in self.references and len(self.references[asset]) > 0:
                self.used_assets.append(asset)
            else:
                self.unused_assets.append(asset)

    def get_unused_assets(self) -> List[Path]:
        return self.unused_assets

    def get_used_assets(self) -> List[Path]:
        return self.used_assets

    def get_usage_details(self, asset: Path) -> List[Path]:
        return list(self.references.get(asset, []))

    def get_stats(self) -> Dict[str, any]:
        total_size = sum(f.stat().st_size for f in self.assets)
        unused_size = sum(f.stat().st_size for f in self.unused_assets)

        return {
            "total_assets": len(self.assets),
            "used_assets": len(self.used_assets),
            "unused_assets": len(self.unused_assets),
            "total_size_bytes": total_size,
            "unused_size_bytes": unused_size,
            "savings_percentage": (unused_size / total_size * 100) if total_size > 0 else 0
        }

if __name__ == "__main__":
    pass
