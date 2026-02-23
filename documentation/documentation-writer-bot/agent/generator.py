from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agent.code_reader import CodeReader
from prompts.templates import MODULE_DOC_TEMPLATE, MERMAID_TEMPLATE, API_REF_TEMPLATE
from config import config

class DocGenerator:
    def __init__(self, tone: str = None):
        self.tone = tone or config.DEFAULT_TONE
        self.llm = ChatOpenAI(model=config.MODEL_NAME, api_key=config.OPENAI_API_KEY)

    def generate_doc(self, file_path: str) -> str:
        code = CodeReader.read_file(file_path)
        if not code:
            return ""

        prompt = PromptTemplate.from_template(MODULE_DOC_TEMPLATE)
        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({
                "tone": self.tone,
                "filename": file_path,
                "code": code
            })
        except Exception as e:
            return f"Error generating documentation: {e}"

    def generate_mermaid(self, file_path: str) -> str:
        code = CodeReader.read_file(file_path)
        if not code:
            return ""

        prompt = PromptTemplate.from_template(MERMAID_TEMPLATE)
        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({
                "code": code
            })
        except Exception as e:
            return f"Error generating mermaid diagram: {e}"

    def generate_api_ref(self, file_path: str) -> str:
        code = CodeReader.read_file(file_path)
        if not code:
            return ""

        prompt = PromptTemplate.from_template(API_REF_TEMPLATE)
        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({
                "code": code
            })
        except Exception as e:
            return f"Error generating API reference: {e}"
