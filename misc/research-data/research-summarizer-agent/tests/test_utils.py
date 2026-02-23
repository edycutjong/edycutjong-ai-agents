import os
import unittest
from utils.pdf_generator import generate_pdf

class TestPDFGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        markdown_text = """
# Title
## Subtitle
Some **bold** and *italic* text.
- List item 1
- List item 2
[Link](http://example.com)
"""
        output_path = "test_output.pdf"

        try:
            result_path = generate_pdf(markdown_text, output_path)
            self.assertTrue(os.path.exists(result_path))
            self.assertEqual(result_path, output_path)
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
