from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class MigrationStep(BaseModel):
    id: int
    description: str = Field(..., description="Description of the migration step")
    sql_up: str = Field(..., description="SQL command to apply the migration")
    sql_down: str = Field(..., description="SQL command to revert the migration")
    risk_level: Literal["low", "medium", "high"] = Field("low", description="Risk level of this step")
    estimated_duration_seconds: int = Field(0, description="Estimated time to execute in seconds")

class BreakingChange(BaseModel):
    description: str = Field(..., description="Description of the breaking change")
    impact: str = Field(..., description="Impact on existing applications")
    mitigation: str = Field(..., description="Suggested mitigation strategy")

class DataIntegrityCheck(BaseModel):
    description: str = Field(..., description="Description of the check")
    query: str = Field(..., description="SQL query to validate data integrity")
    expected_result: str = Field(..., description="Expected result of the query")

class MigrationPlan(BaseModel):
    steps: List[MigrationStep] = Field(default_factory=list)
    breaking_changes: List[BreakingChange] = Field(default_factory=list)
    integrity_checks: List[DataIntegrityCheck] = Field(default_factory=list)
    total_estimated_duration_seconds: int = Field(0)
    summary: str = Field(..., description="High-level summary of the migration")
