import os
from pypdf import PdfReader
from fpdf import FPDF

def read_pdf(file_path):
    """
    Reads a PDF file and extracts its text.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def create_pdf(text, filename="output.pdf"):
    """
    Creates a simple PDF from text.
    Handles basic line wrapping.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    # Simple line wrapping
    pdf.multi_cell(0, 10, text)

    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    pdf.output(filename)
    return filename
