from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import Config
from prompts.sop_prompts import (
    TITLE_METADATA_PROMPT,
    PURPOSE_SCOPE_PROMPT,
    SAFETY_COMPLIANCE_PROMPT,
    PROCEDURE_STEPS_PROMPT,
    REVIEW_APPROVAL_PROMPT
)
from agent.diagrams import DiagramGenerator
import logging

logger = logging.getLogger(__name__)

class SOPGenerator:
    def __init__(self, api_key=None, model_name=None):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model_name = model_name or Config.MODEL_NAME

        if not self.api_key:
            raise ValueError("OpenAI API Key is missing. Please set it in .env or pass it explicitly.")

        self.llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model_name,
            temperature=0.3  # Low temperature for technical writing
        )
        self.output_parser = StrOutputParser()
        self.diagram_generator = DiagramGenerator(self.llm)

    def generate_title_metadata(self, process_description):
        logger.info("Generating Title & Metadata...")
        chain = TITLE_METADATA_PROMPT | self.llm | self.output_parser
        return chain.invoke({"process_description": process_description})

    def generate_purpose_scope(self, process_description, audience):
        logger.info("Generating Purpose & Scope...")
        chain = PURPOSE_SCOPE_PROMPT | self.llm | self.output_parser
        return chain.invoke({
            "process_description": process_description,
            "audience": audience
        })

    def generate_safety_compliance(self, process_description):
        logger.info("Generating Safety & Compliance...")
        chain = SAFETY_COMPLIANCE_PROMPT | self.llm | self.output_parser
        return chain.invoke({"process_description": process_description})

    def generate_procedure_steps(self, process_description):
        logger.info("Generating Procedure Steps...")
        chain = PROCEDURE_STEPS_PROMPT | self.llm | self.output_parser
        return chain.invoke({"process_description": process_description})

    def generate_review_approval(self):
        logger.info("Generating Review & Approval section...")
        chain = REVIEW_APPROVAL_PROMPT | self.llm | self.output_parser
        return chain.invoke({})

    def generate_full_sop(self, process_description, audience="General Staff"):
        """Generates the full SOP document."""
        logger.info("Starting SOP Generation Process...")

        title_meta = self.generate_title_metadata(process_description)
        purpose_scope = self.generate_purpose_scope(process_description, audience)
        safety = self.generate_safety_compliance(process_description)
        procedure = self.generate_procedure_steps(process_description)

        # Generate diagram using the helper class
        diagram = self.diagram_generator.generate_mermaid_code(procedure)

        review = self.generate_review_approval()

        full_content = (
            f"{title_meta}\n\n"
            f"{purpose_scope}\n\n"
            f"{safety}\n\n"
            f"## Process Flowchart\n{diagram}\n\n"
            f"{procedure}\n\n"
            f"{review}"
        )

        logger.info("SOP Generation Complete.")
        return full_content
