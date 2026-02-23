import json
import os
import sys
from typing import List, Dict, Any, Optional

# Add the project root to sys.path to handle imports from directories with hyphens
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from agent.parsers import (
    parse_android_manifest,
    parse_ios_plist,
    parse_chrome_manifest,
    parse_web_package,
    identify_file_type
)
# Note: config.py is in the project root, so we import it directly if sys.path is set correctly
try:
    from config import OPENAI_API_KEY, MODEL_NAME
except ImportError:
    # If running from a different context, try relative import or specific path
    sys.path.append(project_root)
    from config import OPENAI_API_KEY, MODEL_NAME

from prompts.audit_prompts import (
    PERMISSION_ANALYSIS_PROMPT,
    JUSTIFICATION_DOC_PROMPT
)

class AnalysisResult(BaseModel):
    risk_level: str = Field(description="Risk Level of the permission set (Low, Medium, High, Critical)")
    summary: str = Field(description="Short summary of findings")
    analysis: List[Dict[str, str]] = Field(description="Detailed analysis of each permission")

class PermissionAuditorAgent:
    def __init__(self):
        if not OPENAI_API_KEY:
            # Fallback or error - for now, let's assume it's set or handled by user providing it in UI if missing
            pass

        self.llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME if MODEL_NAME else "gpt-4-turbo",
            temperature=0
        )

        # We need to tell the LLM how to format the output for the parser
        self.parser = JsonOutputParser(pydantic_object=AnalysisResult)

    def parse_manifest_file(self, content: Any, filename: str) -> tuple[List[str], str]:
        """
        Parses the manifest content based on filename/content type.
        Returns (permissions_list, detected_platform).
        """
        file_type = identify_file_type(content, filename)
        permissions = []

        if file_type == "android":
            permissions = parse_android_manifest(content)
        elif file_type == "ios":
            permissions = parse_ios_plist(content)
        elif file_type == "chrome":
            permissions = parse_chrome_manifest(content)
        elif file_type == "web":
            permissions = parse_web_package(content)

        return permissions, file_type

    def analyze_permissions(self, permissions: List[str], app_description: str, platform: str) -> Dict[str, Any]:
        """
        Analyzes the permissions using the LLM.
        """
        # Create a prompt that includes the format instructions
        prompt = PromptTemplate(
            template=PERMISSION_ANALYSIS_PROMPT + "\n\n{format_instructions}",
            input_variables=["app_description", "platform", "permissions"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

        chain = prompt | self.llm | self.parser

        try:
            result = chain.invoke({
                "app_description": app_description,
                "platform": platform,
                "permissions": json.dumps(permissions, indent=2)
            })
            return result
        except Exception as e:
            return {
                "risk_level": "Unknown",
                "summary": f"Error during analysis: {str(e)}",
                "analysis": []
            }

    def generate_justification(self, permissions: List[str], app_description: str) -> str:
        """
        Generates a justification document.
        """
        prompt = PromptTemplate(
            template=JUSTIFICATION_DOC_PROMPT,
            input_variables=["app_description", "permissions"]
        )

        chain = prompt | self.llm

        try:
            result = chain.invoke({
                "app_description": app_description,
                "permissions": "\n- ".join(permissions)
            })
            return result.content
        except Exception as e:
            return f"Error generating justification: {str(e)}"
