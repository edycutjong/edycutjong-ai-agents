import os
import markdown
import logging
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_markdown(self, report_data: dict) -> str:
        """Generates a Markdown report string."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_content = f"# Incident Report\n\n**Date:** {timestamp}\n\n"

        report_content += f"## Summary\n{report_data.get('summary', 'N/A')}\n\n"
        report_content += f"## Severity\n{report_data.get('severity', 'UNKNOWN')}\n\n"

        anomalies = report_data.get('anomalies', [])
        if anomalies:
            report_content += "## Detected Anomalies\n"
            for anomaly in anomalies:
                report_content += f"- {anomaly}\n"
            report_content += "\n"

        report_content += f"## Root Cause\n{report_data.get('root_cause', 'N/A')}\n\n"
        report_content += f"## Remediation\n{report_data.get('remediation', 'N/A')}\n\n"

        return report_content

    def save_markdown(self, filename: str, content: str) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)
        logger.info(f"Markdown report saved to {filepath}")
        return filepath

    def save_pdf(self, filename: str, content: str) -> str:
        """Converts simple markdown-like content to PDF using reportlab."""
        filepath = os.path.join(self.output_dir, filename)

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        text_object = c.beginText(40, height - 40)
        text_object.setFont("Helvetica", 12)

        lines = content.split('\n')
        for line in lines:
            if line.startswith("# "):
                text_object.setFont("Helvetica-Bold", 16)
                text_object.textLine(line[2:])
                text_object.setFont("Helvetica", 12)
            elif line.startswith("## "):
                text_object.setFont("Helvetica-Bold", 14)
                text_object.textLine(line[3:])
                text_object.setFont("Helvetica", 12)
            else:
                text_object.textLine(line)

            # Basic pagination check
            if text_object.getY() < 40:
                c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(40, height - 40)
                text_object.setFont("Helvetica", 12)

        c.drawText(text_object)
        c.save()
        logger.info(f"PDF report saved to {filepath}")
        return filepath
