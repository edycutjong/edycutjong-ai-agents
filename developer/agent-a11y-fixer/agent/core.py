import os
from bs4 import BeautifulSoup
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from agent.utils import parse_html

class A11yFixer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required.")
        self.llm = ChatOpenAI(temperature=0, api_key=self.api_key, model="gpt-4")

    def analyze_element(self, element_html: str, context: str = "") -> dict:
        """Use LLM to analyze an element for a11y issues and suggest fixes."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert accessibility (WCAG) auditor. Analyze the following HTML element and identify ANY accessibility issues. If issues exist, provide a fixed HTML version and a description of the issues. Focus on: missing alt text, missing ARIA labels, improper heading hierarchy, form label associations, and keyboard navigation support. Respond in JSON format with keys: 'issues' (list of strings), 'recommendations' (list of strings), 'fixed_html' (string). If no issues, return empty lists and the original HTML."),
            ("user", "Context: {context}\\nElement: {element}")
        ])
        
        # Note: In a real app we'd use StructuredOutput, but using simple prompting here for the boilerplate
        chain = prompt | self.llm
        response = chain.invoke({"context": context, "element": element_html})
        
        # very basic json extraction for boilerplate
        import json
        import re
        content = response.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                pass
        return {"issues": [], "recommendations": [], "fixed_html": element_html}

    def scan_html(self, html_content: str):
        """Scan full HTML document and return structured issues and fixed document."""
        soup = parse_html(html_content)
        issues_list = []
        
        # 1. Image alt text check
        for img in soup.find_all('img'):
            if not img.get('alt'):
                issues_list.append({
                    "type": "Missing Alt Text",
                    "element": str(img),
                    "description": "Image is missing 'alt' attribute.",
                    "recommendation": 'Add a descriptive alt attribute or alt="" for decorative images.'
                })
        
        # 2. Form labels
        for input_el in soup.find_all(['input', 'textarea', 'select']):
            if input_el.get('type') not in ['submit', 'button', 'hidden']:
                input_id = input_el.get('id')
                has_label = False
                if input_id:
                    label = soup.find('label', attrs={'for': input_id})
                    if label: has_label = True
                
                # Check for implicit label wrapping
                if not has_label and input_el.find_parent('label'):
                    has_label = True
                    
                if not has_label:
                    issues_list.append({
                        "type": "Missing Form Label",
                        "element": str(input_el),
                        "description": "Form control does not have an associated label.",
                        "recommendation": "Add a <label> with 'for' matching the input 'id', or wrap the input in a <label>."
                    })
                    
        # 3. Skip Navigation
        if not soup.find('a', href="#main"):
            issues_list.append({
                "type": "Missing Skip Link",
                "element": "<body>",
                "description": "No skip navigation link found.",
                "recommendation": "Add a hidden-by-default link at the top of the body that links to the main content area (e.g., <a href=\\"#main\\">Skip to main content</a>)."
            })

        return {
            "issues": issues_list,
            "fixed_document": str(soup) # Boilerplate doesn't auto-patch everything yet
        }
