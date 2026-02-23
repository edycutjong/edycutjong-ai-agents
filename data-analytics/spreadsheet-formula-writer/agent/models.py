from typing import List, Optional
from pydantic import BaseModel, Field

class FormulaResponse(BaseModel):
    """Structured response for a spreadsheet formula request."""
    formula: str = Field(description="The generated Excel or Google Sheets formula.")
    explanation: str = Field(description="A step-by-step explanation of how the formula works.")
    alternatives: Optional[List[str]] = Field(description="Alternative formulas or approaches if applicable.")
    examples: Optional[List[str]] = Field(description="Examples of how to use the formula with sample data.")
