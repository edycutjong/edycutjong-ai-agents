import os
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, items):
        self.items = items
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_markdown(self):
        """
        Generates a markdown report of the review findings.
        """
        if not self.items:
            return "# UI Copy Review Report\n\nNo issues found or no items reviewed."

        report = [
            f"# UI Copy Review Report",
            f"**Generated:** {self.timestamp}",
            f"**Items Reviewed:** {len(self.items)} with issues found.\n",
            "---"
        ]

        for i, item in enumerate(self.items):
            report.append(f"## Issue #{i+1}")
            report.append(f"**Text:** `{item['text']}`")
            if item.get('line'):
                report.append(f"**Line:** {item['line']}")
            if item.get('type'):
                report.append(f"**Type:** {item['type']}")
            if item.get('tag'):
                report.append(f"**Tag:** `<{item['tag']}>`")
            if item.get('attribute'):
                report.append(f"**Attribute:** `{item['attribute']}`")
            if item.get('context'):
                report.append(f"**Context:**\n```\n{item['context']}\n```")

            report.append("\n**Findings:**")
            for check, result in item.get('issues', {}).items():
                report.append(f"- **{check}:** {result}")

            report.append("\n---")

        return "\n".join(report)

    def save_report(self, output_path="copy_review_report.md"):
        content = self.generate_markdown()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Report saved to {output_path}")

    def generate_json(self):
        return json.dumps(self.items, indent=2)
