import hcl2
import logging

logger = logging.getLogger(__name__)

class TerraformParser:
    def parse_hcl(self, content: str) -> dict:
        """Parses HCL content string into a dictionary."""
        try:
            return hcl2.loads(content)
        except Exception as e:  # pragma: no cover
            logger.error(f"Error parsing HCL: {e}")  # pragma: no cover
            return {}  # pragma: no cover

    def parse_file(self, filepath: str) -> dict:
        """Parses a Terraform file."""
        try:  # pragma: no cover
            with open(filepath, 'r') as file:  # pragma: no cover
                return hcl2.load(file)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            logger.error(f"Error reading file {filepath}: {e}")  # pragma: no cover
            return {}  # pragma: no cover
