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
            self.themes_dir = themes_dir
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
        if not os.path.exists(self.themes_dir):
            return []

        themes = [
            f.replace('.json', '')
            for f in os.listdir(self.themes_dir)
            if f.endswith('.json')
        ]
        return sorted(themes)

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
        if not theme_name.endswith('.json'):
            filename = f"{theme_name}.json"
        else:
            filename = theme_name

        path = os.path.join(self.themes_dir, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Theme '{theme_name}' not found at {path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding theme {filename}: {e}")
