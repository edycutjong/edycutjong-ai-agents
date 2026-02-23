import frontmatter
import os

class MarkdownParser:
    """
    Parses Markdown files to extract frontmatter metadata and content.
    """

    def parse_file(self, filepath: str) -> dict:
        """
        Parses a Markdown file.

        Args:
            filepath (str): Path to the markdown file.

        Returns:
            dict: A dictionary containing 'metadata' (dict) and 'content' (str).
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            return {
                'metadata': post.metadata,
                'content': post.content
            }
        except Exception as e:
            raise ValueError(f"Error parsing file {filepath}: {e}")

    def parse_string(self, text: str) -> dict:
        """
        Parses a Markdown string.

        Args:
            text (str): The markdown content.

        Returns:
            dict: A dictionary containing 'metadata' (dict) and 'content' (str).
        """
        try:
            post = frontmatter.loads(text)
            return {
                'metadata': post.metadata,
                'content': post.content
            }
        except Exception as e:
             raise ValueError(f"Error parsing string: {e}")
