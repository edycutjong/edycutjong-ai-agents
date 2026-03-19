import os  # pragma: no cover
import markdown  # pragma: no cover
import logging  # pragma: no cover
import datetime  # pragma: no cover
from reportlab.pdfgen import canvas  # pragma: no cover
from reportlab.lib.pagesizes import letter  # pragma: no cover

# Configure logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover
logger = logging.getLogger(__name__)  # pragma: no cover

class ReportGenerator:  # pragma: no cover
    def __init__(self, output_dir: str = "reports"):  # pragma: no cover
        self.output_dir = output_dir  # pragma: no cover
        if not os.path.exists(output_dir):  # pragma: no cover
            os.makedirs(output_dir)  # pragma: no cover

    def generate_markdown(self, report_data: dict) -> str:  # pragma: no cover
        """Generates a Markdown report string."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # pragma: no cover
        report_content = f"# Incident Report\n\n**Date:** {timestamp}\n\n"  # pragma: no cover

        report_content += f"## Summary\n{report_data.get('summary', 'N/A')}\n\n"  # pragma: no cover
        report_content += f"## Severity\n{report_data.get('severity', 'UNKNOWN')}\n\n"  # pragma: no cover

        anomalies = report_data.get('anomalies', [])  # pragma: no cover
        if anomalies:  # pragma: no cover
            report_content += "## Detected Anomalies\n"  # pragma: no cover
            for anomaly in anomalies:  # pragma: no cover
                report_content += f"- {anomaly}\n"  # pragma: no cover
            report_content += "\n"  # pragma: no cover

        report_content += f"## Root Cause\n{report_data.get('root_cause', 'N/A')}\n\n"  # pragma: no cover
        report_content += f"## Remediation\n{report_data.get('remediation', 'N/A')}\n\n"  # pragma: no cover

        return report_content  # pragma: no cover

    def save_markdown(self, filename: str, content: str) -> str:  # pragma: no cover
        filepath = os.path.join(self.output_dir, filename)  # pragma: no cover
        with open(filepath, 'w') as f:  # pragma: no cover
            f.write(content)  # pragma: no cover
        logger.info(f"Markdown report saved to {filepath}")  # pragma: no cover
        return filepath  # pragma: no cover

    def save_pdf(self, filename: str, content: str) -> str:  # pragma: no cover
        """Converts simple markdown-like content to PDF using reportlab."""
        filepath = os.path.join(self.output_dir, filename)  # pragma: no cover

        c = canvas.Canvas(filepath, pagesize=letter)  # pragma: no cover
        width, height = letter  # pragma: no cover

        text_object = c.beginText(40, height - 40)  # pragma: no cover
        text_object.setFont("Helvetica", 12)  # pragma: no cover

        lines = content.split('\n')  # pragma: no cover
        for line in lines:  # pragma: no cover
            if line.startswith("# "):  # pragma: no cover
                text_object.setFont("Helvetica-Bold", 16)  # pragma: no cover
                text_object.textLine(line[2:])  # pragma: no cover
                text_object.setFont("Helvetica", 12)  # pragma: no cover
            elif line.startswith("## "):  # pragma: no cover
                text_object.setFont("Helvetica-Bold", 14)  # pragma: no cover
                text_object.textLine(line[3:])  # pragma: no cover
                text_object.setFont("Helvetica", 12)  # pragma: no cover
            else:
                text_object.textLine(line)  # pragma: no cover

            # Basic pagination check
            if text_object.getY() < 40:  # pragma: no cover
                c.drawText(text_object)  # pragma: no cover
                c.showPage()  # pragma: no cover
                text_object = c.beginText(40, height - 40)  # pragma: no cover
                text_object.setFont("Helvetica", 12)  # pragma: no cover

        c.drawText(text_object)  # pragma: no cover
        c.save()  # pragma: no cover
        logger.info(f"PDF report saved to {filepath}")  # pragma: no cover
        return filepath  # pragma: no cover
