import hcl2
import logging

logger = logging.getLogger(__name__)

class TerraformParser:
    def parse_hcl(self, content: str) -> dict:
        """Parses HCL content string into a dictionary."""
        try:
            return hcl2.loads(content)
        except Exception as e:
            logger.error(f"Error parsing HCL: {e}")
            return {}

    def parse_file(self, filepath: str) -> dict:
        """Parses a Terraform file."""
        try:
            with open(filepath, 'r') as file:
                return hcl2.load(file)
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return {}
