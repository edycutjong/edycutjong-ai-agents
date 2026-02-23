from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class DesignToken(BaseModel):
    name: str = Field(..., description="The name of the token (e.g., 'primary-500', 'spacing-md')")
    value: str = Field(..., description="The value of the token (e.g., '#3B82F6', '16px', '1rem')")
    type: str = Field(..., description="The type of token (color, spacing, typography, borderRadius, borderWidth, shadow, opacity, etc.)")
    description: Optional[str] = Field(None, description="Description of the token")

    # For typography, we might want composite values, but for now string value is most flexible
    # and we can let the LLM format it (e.g., "16px/1.5 Inter") or we can parse it later.
    # However, W3C spec often breaks typography into objects.
    # For this agent, we will keep it simple as string values or allow complex values if we used a more complex model.
    # But to keep it robust for CSS generation, string values are often best.

class TokenSet(BaseModel):
    name: str = Field("global", description="Name of the token set (e.g., 'light', 'dark', 'core')")
    tokens: List[DesignToken] = Field(default_factory=list)

class DesignSpecs(BaseModel):
    """Container for the extracted design system"""
    theme_name: str = Field("default", description="Name of the theme")
    token_sets: List[TokenSet] = Field(default_factory=list)
