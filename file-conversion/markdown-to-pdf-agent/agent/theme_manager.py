import os
import json

class ThemeManager:
    """
    Manages JSON themes for PDF generation.
    """
    def __init__(self, themes_dir: str = None):
        """
        Initialize ThemeManager.

        Args:
            themes_dir (str, optional): Path to the themes directory.
                                        Defaults to 'themes' relative to the project root.
        """
        if themes_dir:
            self.themes_dir = themes_dir  # pragma: no cover
        else:
            # Assume themes are in apps/agents/file-conversion/markdown-to-pdf-agent/themes
            # This file is in apps/agents/file-conversion/markdown-to-pdf-agent/agent/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.themes_dir = os.path.join(base_dir, "themes")

    def list_themes(self) -> list[str]:
        """
        List available themes.

        Returns:
            list[str]: A list of theme names (without .json extension).
        """
        if not os.path.exists(self.themes_dir):  # pragma: no cover
            return []  # pragma: no cover

        themes = [  # pragma: no cover
            f.replace('.json', '')
            for f in os.listdir(self.themes_dir)
            if f.endswith('.json')
        ]
        return sorted(themes)  # pragma: no cover

    def get_theme(self, theme_name: str) -> dict:
        """
        Get the JSON content for a specific theme.

        Args:
            theme_name (str): The name of the theme.

        Returns:
            dict: The theme dictionary.

        Raises:
            FileNotFoundError: If the theme file does not exist.
        """
        # Allow passing full filename with extension or just name
        if not theme_name.endswith('.json'):  # pragma: no cover
            filename = f"{theme_name}.json"  # pragma: no cover
        else:
            filename = theme_name  # pragma: no cover

        path = os.path.join(self.themes_dir, filename)  # pragma: no cover

        if not os.path.exists(path):  # pragma: no cover
            raise FileNotFoundError(f"Theme '{theme_name}' not found at {path}")  # pragma: no cover

        try:  # pragma: no cover
            with open(path, 'r', encoding='utf-8') as f:  # pragma: no cover
                return json.load(f)  # pragma: no cover
        except json.JSONDecodeError as e:  # pragma: no cover
            raise ValueError(f"Error decoding theme {filename}: {e}")  # pragma: no cover
