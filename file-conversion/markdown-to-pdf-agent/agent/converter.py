from fpdf import FPDF
from markdown_it import MarkdownIt
import os

class ThemeFPDF(FPDF):
    def __init__(self, theme):
        super().__init__()
        self.theme = theme

    def header(self):
        # Apply background color to every page
        if 'page' in self.theme and 'bg' in self.theme['page']:
            self.set_fill_color(*self.theme['page']['bg'])
            self.rect(0, 0, self.w, self.h, 'F')
            # Reset fill color? No, caller sets it.

class PDFConverter:
    """
    Converts Markdown content to PDF using FPDF2 and Markdown-It.
    """

    def convert(self, md_content: str, theme: dict, output_path: str) -> bool:
        """
        Converts Markdown string to a PDF file.
        """
        try:
            pdf = ThemeFPDF(theme)
            pdf.add_page()

            # Page settings
            page_style = theme.get('page', {})
            margins = page_style.get('margins', 10)
            pdf.set_margins(margins, margins, margins)

            # Initial Font (Body)
            body_style = theme.get('p', {'font': 'Helvetica', 'size': 11, 'color': [0,0,0]})
            self._set_font(pdf, body_style)

            md = MarkdownIt()
            tokens = md.parse(md_content)

            # State tracking
            current_style = body_style
            in_table = False
            table_data = []
            current_row = []
            current_cell_text = ""
            in_blockquote = False
            original_left_margin = margins

            for i, token in enumerate(tokens):

                # --- Blockquotes ---
                if token.type == 'blockquote_open':
                    in_blockquote = True
                    pdf.set_left_margin(original_left_margin + 10)
                    pdf.set_text_color(100, 100, 100) # Gray for quote
                    pdf.set_font(body_style.get('font', 'Helvetica'), 'I', body_style.get('size', 11))

                elif token.type == 'blockquote_close':
                    in_blockquote = False
                    pdf.set_left_margin(original_left_margin)
                    self._set_font(pdf, body_style)
                    pdf.ln(5)

                # --- Tables ---
                elif token.type == 'table_open':
                    in_table = True
                    table_data = []

                elif token.type == 'table_close':
                    in_table = False
                    # Render table
                    if table_data:
                        try:
                            # FPDF2 table rendering
                            # Requires setting font/size?
                            pdf.set_font(body_style.get('font', 'Helvetica'), '', body_style.get('size', 10))
                            pdf.set_text_color(0,0,0)

                            with pdf.table(text_align="LEFT") as table:
                                for row in table_data:
                                    row_cells = table.row()
                                    for cell in row:
                                        row_cells.cell(str(cell))
                        except Exception as e:
                            print(f"Error rendering table: {e}")
                    pdf.ln(5)
                    # Restore body font
                    self._set_font(pdf, body_style)

                elif token.type == 'tr_open':
                    current_row = []
                elif token.type == 'tr_close':
                    table_data.append(current_row)

                elif token.type == 'th_open' or token.type == 'td_open':
                    current_cell_text = ""

                elif token.type == 'th_close' or token.type == 'td_close':
                    current_row.append(current_cell_text)

                # --- Headings ---
                elif token.type == 'heading_open':
                    level = token.tag
                    style = theme.get(level, theme.get('h1'))
                    if not style: style = theme.get('h1')
                    self._set_font(pdf, style)
                    pdf.ln(style.get('margin_top', 5))
                    current_style = style

                elif token.type == 'heading_close':
                    pdf.ln(5)
                    current_style = body_style
                    if not in_blockquote:
                        self._set_font(pdf, current_style)

                # --- Paragraphs ---
                elif token.type == 'paragraph_open':
                    # Don't add newline if inside blockquote?
                    # Or if inside table (already handled)
                    if not in_table:
                        pdf.ln(current_style.get('line_height', 5))

                elif token.type == 'paragraph_close':
                    if not in_table:
                        pdf.ln(2)

                # --- Inline Content ---
                elif token.type == 'inline':
                    if in_table:
                        # Extract text from children for table cells
                        text_content = ""
                        if token.children:
                            for child in token.children:
                                if child.type == 'text':
                                    text_content += child.content
                                elif child.type == 'code_inline':
                                    text_content += child.content
                                elif child.type == 'softbreak':
                                    text_content += " "
                        else:
                            text_content = token.content
                        current_cell_text += text_content
                        continue

                    # Regular inline processing
                    active_styles = set()
                    base_style_str = current_style.get('style', '')
                    if in_blockquote:
                         # Ensure Italic is added to base style
                         if 'I' not in base_style_str:
                             base_style_str += 'I'

                    if 'B' in base_style_str: active_styles.add('B')
                    if 'I' in base_style_str: active_styles.add('I')
                    if 'U' in base_style_str: active_styles.add('U')

                    if token.children:
                        for child in token.children:
                            if child.type == 'text':
                                style_str = "".join(sorted(active_styles))
                                font_family = current_style.get('font', 'Helvetica')
                                font_size = current_style.get('size', 11)

                                if 'CODE' in active_styles:
                                    pdf.set_font("Courier", "", font_size)
                                else:
                                    pdf.set_font(font_family, style_str, font_size)

                                pdf.write(5, child.content)

                            elif child.type == 'strong_open':
                                active_styles.add('B')
                            elif child.type == 'strong_close':
                                if 'B' in active_styles: active_styles.remove('B')
                            elif child.type == 'em_open':
                                active_styles.add('I')
                            elif child.type == 'em_close':
                                if 'I' in active_styles: active_styles.remove('I')
                            elif child.type == 'code_inline':
                                pdf.set_font("Courier", "", current_style.get('size', 11))
                                pdf.write(5, child.content)
                                # Restore
                                style_str = "".join(sorted(active_styles))
                                pdf.set_font(current_style.get('font', 'Helvetica'), style_str, current_style.get('size', 11))
                            elif child.type == 'softbreak':
                                pdf.write(5, " ")
                            elif child.type == 'hardbreak':
                                pdf.ln(5)
                    else:
                        pdf.write(5, token.content)

                # --- Code Blocks ---
                elif token.type == 'fence' or token.type == 'code_block':
                    code_style = theme.get('code', {'font': 'Courier', 'size': 10, 'color': [0,0,0], 'bg': [240,240,240]})
                    pdf.set_font(code_style.get('font', 'Courier'), '', code_style.get('size', 10))
                    pdf.set_text_color(*code_style.get('color', [0,0,0]))

                    if 'bg' in code_style:
                        pdf.set_fill_color(*code_style['bg'])
                        fill = True
                    else:
                        fill = False

                    content = token.content.replace('\t', '    ')
                    pdf.multi_cell(0, 5, content, fill=fill)

                    self._set_font(pdf, body_style)
                    pdf.ln(5)

                # --- Lists ---
                elif token.type == 'list_item_open':
                     pdf.write(5, "  • ")

                elif token.type == 'list_item_close':
                     pdf.ln(5)

            # Output
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            pdf.output(output_path)
            return True

        except Exception as e:
            print(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _set_font(self, pdf, style):
        font = style.get('font', 'Helvetica')
        font_style = style.get('style', '')
        size = style.get('size', 11)
        color = style.get('color', [0, 0, 0])

        pdf.set_font(font, font_style, size)
        pdf.set_text_color(*color)
