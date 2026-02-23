import re
import html
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

def generate_pdf(markdown_text: str, output_path: str):
    """
    Generates a PDF from markdown text using ReportLab.
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story = []

    # Simple markdown parsing
    lines = markdown_text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            Story.append(Spacer(1, 12))
            continue

        style = styles["Normal"]

        # Determine style based on markdown headers
        if line.startswith('# '):
            style = styles["Heading1"]
            content = line[2:]
        elif line.startswith('## '):
            style = styles["Heading2"]
            content = line[3:]
        elif line.startswith('### '):
            style = styles["Heading3"]
            content = line[4:]
        else:
            content = line

        # Escape HTML entities first to prevent XML parsing errors
        content = html.escape(content)

        # Apply markdown formatting (converting to ReportLab XML tags)
        # Bold **text** -> <b>text</b>
        content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', content)
        # Italic *text* -> <i>text</i>
        content = re.sub(r'\*(.*?)\*', r'<i>\1</i>', content)

        # Links [text](url) -> <a href="url" color="blue">text</a>
        # Note: We need to unescape the URL part if it was escaped, but ReportLab expects proper XML attributes.
        # Actually, simpler to just match and replace carefully.
        # Since we escaped everything, [text](url) became [text](url) but < > & are safe.
        # But wait, if URL contains & it became &amp;.

        def link_replacer(match):
            text = match.group(1)
            url = match.group(2)
            return f'<a href="{url}" color="blue">{text}</a>'

        content = re.sub(r'\[(.*?)\]\((.*?)\)', link_replacer, content)

        try:
            p = Paragraph(content, style)
            Story.append(p)
        except Exception:
            # Fallback: strip tags if parsing fails
            clean_content = re.sub('<[^<]+?>', '', content)
            p = Paragraph(clean_content, styles["Normal"])
            Story.append(p)

    doc.build(Story)
    return output_path
