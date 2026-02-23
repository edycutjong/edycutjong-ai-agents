import os
from pathlib import Path
from typing import List, Set

class AssetScanner:
    """
    Scans a directory for asset files based on common extensions.
    """

    ASSET_EXTENSIONS = {
        # Images
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp', '.ico', '.tiff',
        # Videos
        '.mp4', '.mov', '.avi', '.webm',
        # Documents
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        # Audio
        '.mp3', '.wav', '.ogg',
        # Fonts
        '.ttf', '.otf', '.woff', '.woff2'
    }

    def __init__(self, root_dir: str, ignore_dirs: List[str] = None):
        self.root_dir = Path(root_dir)
        self.ignore_dirs = set(ignore_dirs) if ignore_dirs else {'.git', 'node_modules', 'dist', 'build', '__pycache__', 'venv', '.next'}

    def scan(self) -> List[Path]:
        """
        Recursively scans the root directory for assets.
        """
        assets = []
        for root, dirs, files in os.walk(self.root_dir):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in self.ASSET_EXTENSIONS:
                    assets.append(file_path)

        return assets

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        scanner = AssetScanner(sys.argv[1])
        assets = scanner.scan()
        for asset in assets:
            print(asset)
    else:
        print("Usage: python file_scanner.py <directory>")
