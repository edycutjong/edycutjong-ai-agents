import os

try:
    from fpdf import FPDF
except ImportError:  # pragma: no cover
    FPDF = None  # pragma: no cover

def save_to_markdown(content, filename):
    """Saves content to a Markdown file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)  # pragma: no cover
        self.cell(0, 10, 'Press Release', 0, 1, 'C')  # pragma: no cover

    def footer(self):
        self.set_y(-15)  # pragma: no cover
        self.set_font('Arial', 'I', 8)  # pragma: no cover
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')  # pragma: no cover

def save_to_pdf(content, filename):
    """Saves content to a PDF file using FPDF."""
    if FPDF is None:
        raise ImportError("fpdf library is not installed. Please install it via 'pip install fpdf'.")  # pragma: no cover

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Simple sanitization to avoid encoding issues with standard FPDF fonts
    # In a production app, we'd use a unicode-compatible font.
    safe_content = content.encode('latin-1', 'replace').decode('latin-1')

    pdf.multi_cell(0, 10, safe_content)
    pdf.output(filename)
    return filename
