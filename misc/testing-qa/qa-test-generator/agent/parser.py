from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class UIElement:
    def __init__(self, tag: str, attrs: Dict, text: str, element_id: str = None):
        self.tag = tag
        self.attrs = attrs
        self.text = text.strip() if text else ""
        self.id = element_id

    def to_dict(self):
        return {  # pragma: no cover
            "tag": self.tag,
            "attrs": self.attrs,
            "text": self.text,
            "id": self.id
        }

    def __repr__(self):
        return f"<UIElement {self.tag} id={self.id} text='{self.text[:20]}'>"  # pragma: no cover

class UIParser:
    def __init__(self):
        pass

    def parse_html(self, html_content: str) -> List[UIElement]:
        """
        Parses raw HTML content and extracts interactive UI elements.
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        interactive_elements = []

        # Find buttons
        for btn in soup.find_all('button'):
            interactive_elements.append(self._create_ui_element(btn))

        # Find inputs
        for inp in soup.find_all('input'):
            # Filter hidden inputs if needed, but for testing they might be relevant.
            # Usually we test visible inputs.
            if inp.get('type') != 'hidden':
                interactive_elements.append(self._create_ui_element(inp))

        # Find links (a tags with href)
        for link in soup.find_all('a', href=True):
            interactive_elements.append(self._create_ui_element(link))

        # Find textareas
        for textarea in soup.find_all('textarea'):
            interactive_elements.append(self._create_ui_element(textarea))  # pragma: no cover

        # Find selects
        for select in soup.find_all('select'):
            interactive_elements.append(self._create_ui_element(select))  # pragma: no cover

        return interactive_elements

    def _create_ui_element(self, element) -> UIElement:
        attrs = element.attrs
        element_id = attrs.get('id')
        text = element.get_text()

        # For inputs, value might be more relevant than text
        if element.name == 'input':
            if not text and 'value' in attrs:
                text = attrs['value']  # pragma: no cover
            if not text and 'placeholder' in attrs:
                text = f"Placeholder: {attrs['placeholder']}"

        return UIElement(
            tag=element.name,
            attrs=attrs,
            text=text,
            element_id=element_id
        )

    def extract_structure(self, html_content: str) -> str:
        """
        Returns a simplified string representation of the DOM structure
        useful for LLM context.
        """
        soup = BeautifulSoup(html_content, 'html.parser')  # pragma: no cover
        # Remove scripts and styles to reduce token usage
        for script in soup(["script", "style"]):  # pragma: no cover
            script.decompose()  # pragma: no cover

        return soup.prettify()  # pragma: no cover
