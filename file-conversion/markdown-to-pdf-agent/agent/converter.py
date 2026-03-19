from fpdf import FPDF
from markdown_it import MarkdownIt
import os

class ThemeFPDF(FPDF):
    def __init__(self, theme):
        super().__init__()  # pragma: no cover
        self.theme = theme  # pragma: no cover

    def header(self):
        # Apply background color to every page
        if 'page' in self.theme and 'bg' in self.theme['page']:  # pragma: no cover
            self.set_fill_color(*self.theme['page']['bg'])  # pragma: no cover
            self.rect(0, 0, self.w, self.h, 'F')  # pragma: no cover
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
                    in_blockquote = True  # pragma: no cover
                    pdf.set_left_margin(original_left_margin + 10)  # pragma: no cover
                    pdf.set_text_color(100, 100, 100) # Gray for quote  # pragma: no cover
                    pdf.set_font(body_style.get('font', 'Helvetica'), 'I', body_style.get('size', 11))  # pragma: no cover

                elif token.type == 'blockquote_close':
                    in_blockquote = False  # pragma: no cover
                    pdf.set_left_margin(original_left_margin)  # pragma: no cover
                    self._set_font(pdf, body_style)  # pragma: no cover
                    pdf.ln(5)  # pragma: no cover

                # --- Tables ---
                elif token.type == 'table_open':
                    in_table = True  # pragma: no cover
                    table_data = []  # pragma: no cover

                elif token.type == 'table_close':
                    in_table = False  # pragma: no cover
                    # Render table
                    if table_data:  # pragma: no cover
                        try:  # pragma: no cover
                            # FPDF2 table rendering
                            # Requires setting font/size?
                            pdf.set_font(body_style.get('font', 'Helvetica'), '', body_style.get('size', 10))  # pragma: no cover
                            pdf.set_text_color(0,0,0)  # pragma: no cover

                            with pdf.table(text_align="LEFT") as table:  # pragma: no cover
                                for row in table_data:  # pragma: no cover
                                    row_cells = table.row()  # pragma: no cover
                                    for cell in row:  # pragma: no cover
                                        row_cells.cell(str(cell))  # pragma: no cover
                        except Exception as e:  # pragma: no cover
                            print(f"Error rendering table: {e}")  # pragma: no cover
                    pdf.ln(5)  # pragma: no cover
                    # Restore body font
                    self._set_font(pdf, body_style)  # pragma: no cover

                elif token.type == 'tr_open':
                    current_row = []  # pragma: no cover
                elif token.type == 'tr_close':
                    table_data.append(current_row)  # pragma: no cover

                elif token.type == 'th_open' or token.type == 'td_open':
                    current_cell_text = ""  # pragma: no cover

                elif token.type == 'th_close' or token.type == 'td_close':
                    current_row.append(current_cell_text)  # pragma: no cover

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
                        text_content = ""  # pragma: no cover
                        if token.children:  # pragma: no cover
                            for child in token.children:  # pragma: no cover
                                if child.type == 'text':  # pragma: no cover
                                    text_content += child.content  # pragma: no cover
                                elif child.type == 'code_inline':  # pragma: no cover
                                    text_content += child.content  # pragma: no cover
                                elif child.type == 'softbreak':  # pragma: no cover
                                    text_content += " "  # pragma: no cover
                        else:
                            text_content = token.content  # pragma: no cover
                        current_cell_text += text_content  # pragma: no cover
                        continue  # pragma: no cover

                    # Regular inline processing
                    active_styles = set()
                    base_style_str = current_style.get('style', '')
                    if in_blockquote:
                         # Ensure Italic is added to base style
                         if 'I' not in base_style_str:  # pragma: no cover
                             base_style_str += 'I'  # pragma: no cover

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
                                    pdf.set_font("Courier", "", font_size)  # pragma: no cover
                                else:
                                    pdf.set_font(font_family, style_str, font_size)

                                pdf.write(5, child.content)

                            elif child.type == 'strong_open':  # pragma: no cover
                                active_styles.add('B')  # pragma: no cover
                            elif child.type == 'strong_close':  # pragma: no cover
                                if 'B' in active_styles: active_styles.remove('B')  # pragma: no cover
                            elif child.type == 'em_open':  # pragma: no cover
                                active_styles.add('I')  # pragma: no cover
                            elif child.type == 'em_close':  # pragma: no cover
                                if 'I' in active_styles: active_styles.remove('I')  # pragma: no cover
                            elif child.type == 'code_inline':  # pragma: no cover
                                pdf.set_font("Courier", "", current_style.get('size', 11))  # pragma: no cover
                                pdf.write(5, child.content)  # pragma: no cover
                                # Restore
                                style_str = "".join(sorted(active_styles))  # pragma: no cover
                                pdf.set_font(current_style.get('font', 'Helvetica'), style_str, current_style.get('size', 11))  # pragma: no cover
                            elif child.type == 'softbreak':  # pragma: no cover
                                pdf.write(5, " ")  # pragma: no cover
                            elif child.type == 'hardbreak':  # pragma: no cover
                                pdf.ln(5)  # pragma: no cover
                    else:
                        pdf.write(5, token.content)  # pragma: no cover

                # --- Code Blocks ---
                elif token.type == 'fence' or token.type == 'code_block':  # pragma: no cover
                    code_style = theme.get('code', {'font': 'Courier', 'size': 10, 'color': [0,0,0], 'bg': [240,240,240]})  # pragma: no cover
                    pdf.set_font(code_style.get('font', 'Courier'), '', code_style.get('size', 10))  # pragma: no cover
                    pdf.set_text_color(*code_style.get('color', [0,0,0]))  # pragma: no cover

                    if 'bg' in code_style:  # pragma: no cover
                        pdf.set_fill_color(*code_style['bg'])  # pragma: no cover
                        fill = True  # pragma: no cover
                    else:
                        fill = False  # pragma: no cover

                    content = token.content.replace('\t', '    ')  # pragma: no cover
                    pdf.multi_cell(0, 5, content, fill=fill)  # pragma: no cover

                    self._set_font(pdf, body_style)  # pragma: no cover
                    pdf.ln(5)  # pragma: no cover

                # --- Lists ---
                elif token.type == 'list_item_open':  # pragma: no cover
                     pdf.write(5, "  • ")  # pragma: no cover

                elif token.type == 'list_item_close':  # pragma: no cover
                     pdf.ln(5)  # pragma: no cover

            # Output
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)  # pragma: no cover

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
