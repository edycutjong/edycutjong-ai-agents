import os
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
import logging
import re

logger = logging.getLogger(__name__)

class SOPExporter:
    def __init__(self, output_dir="output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def save_markdown(self, content, filename="SOP.md"):
        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"Saving Markdown to {filepath}...")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            logger.info("Markdown saved successfully.")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save Markdown: {e}")
            raise

    def save_pdf(self, content, filename="SOP.pdf"):
        filepath = os.path.join(self.output_dir, filename)
        logger.info(f"Saving PDF to {filepath}...")

        try:
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=18)
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

            # Simple Markdown to ReportLab conversion (very basic)
            # Converting Markdown to HTML first is easier if we had an HTML->PDF converter
            # But here we will just parse line by line for headers and text

            flowables = []

            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    flowables.append(Spacer(1, 12))
                    continue

                if line.startswith('# '):
                    # H1
                    text = line[2:]
                    flowables.append(Paragraph(text, styles['Title']))
                    flowables.append(Spacer(1, 12))
                elif line.startswith('## '):
                    # H2
                    text = line[3:]
                    flowables.append(Paragraph(text, styles['Heading2']))
                    flowables.append(Spacer(1, 12))
                elif line.startswith('### '):
                    # H3
                    text = line[4:]
                    flowables.append(Paragraph(text, styles['Heading3']))
                    flowables.append(Spacer(1, 12))
                elif line.startswith('- ') or line.startswith('* '):
                    # Bullet point
                    text = f"• {line[2:]}"
                    flowables.append(Paragraph(text, styles['BodyText']))
                elif re.match(r'^\d+\.', line):
                    # Numbered list
                    flowables.append(Paragraph(line, styles['BodyText']))
                elif line.startswith('```mermaid'):
                    # Skip mermaid blocks for PDF or just show as code
                    flowables.append(Paragraph("[Mermaid Diagram Placeholder]", styles['Code']))
                elif line.startswith('```'):
                    continue
                else:
                    # Normal text
                    flowables.append(Paragraph(line, styles['BodyText']))

            doc.build(flowables)
            logger.info("PDF saved successfully.")
            return filepath
        except Exception as e:
            logger.error(f"Failed to save PDF: {e}")
            # Do not raise, just log error as PDF is secondary
            return None
