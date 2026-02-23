import json
import os
from typing import List, Dict, Any
from datetime import datetime

class Reporter:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_report(self, results: List[Dict[str, Any]], format: str = "json") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"accessibility_report_{timestamp}"

        if format.lower() == "json":
            output_path = os.path.join(self.output_dir, f"{filename}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            return output_path

        elif format.lower() == "markdown":
            output_path = os.path.join(self.output_dir, f"{filename}.md")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Accessibility Report - {timestamp}\n\n")
                f.write(f"Total Images Processed: {len(results)}\n\n")

                for i, item in enumerate(results, 1):
                    f.write(f"## Image {i}\n")
                    f.write(f"**Source:** `{item.get('src')}`\n")
                    f.write(f"**File:** `{item.get('filepath')}`\n")
                    f.write(f"**Context:** {item.get('context', 'N/A')}\n")
                    f.write(f"**Suggested Alt Text:** {item.get('suggested_alt')}\n")
                    f.write("---\n")
            return output_path

        else:
            raise ValueError(f"Unsupported format: {format}")
