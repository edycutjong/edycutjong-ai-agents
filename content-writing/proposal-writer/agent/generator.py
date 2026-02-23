import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from .models import Proposal
try:
    from ..config import MODEL_NAME, TEMPERATURE, OPENAI_API_KEY
except ImportError:
    # Fallback for when running as script/main where parent is in path but not as package
    import config
    MODEL_NAME = config.MODEL_NAME
    TEMPERATURE = config.TEMPERATURE
    OPENAI_API_KEY = config.OPENAI_API_KEY

class ProposalGenerator:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        self.llm = ChatOpenAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            api_key=OPENAI_API_KEY
        )

        # Load system prompt
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'system_prompt.txt')
        with open(prompt_path, 'r') as f:
            self.system_prompt = f.read()

        self.parser = PydanticOutputParser(pydantic_object=Proposal)

    def generate_proposal(self, requirements: str) -> Proposal:
        """
        Generates a proposal based on the given requirements.
        """

        # We use with_structured_output for newer models/langchain versions if possible,
        # but PydanticOutputParser is also reliable.
        # Let's use standard chain with parser instructions.

        prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}\n\n{format_instructions}"),
            ("user", "Project Requirements:\n{requirements}")
        ])

        chain = prompt | self.llm | self.parser

        try:
            proposal = chain.invoke({
                "system_prompt": self.system_prompt,
                "format_instructions": self.parser.get_format_instructions(),
                "requirements": requirements
            })
            return proposal
        except Exception as e:
            # Fallback or retry logic could be added here
            raise RuntimeError(f"Failed to generate proposal: {e}")
