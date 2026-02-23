from typing import List, Optional
from pydantic import BaseModel, Field

class PackageConfig(BaseModel):
    name: str
    description: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)

class MonorepoConfig(BaseModel):
    project_name: str
    package_manager: str = "pnpm"  # pnpm, npm, yarn, bun
    monorepo_tool: str = "turbo"  # turbo, nx
    packages: List[PackageConfig] = Field(default_factory=list)
    apps: List[PackageConfig] = Field(default_factory=list)
    ci_provider: str = "github-actions"
    include_changesets: bool = True
    include_linting: bool = True
    include_testing: bool = True

class AgentState(BaseModel):
    config: MonorepoConfig
    current_step: str = "init"
    logs: List[str] = Field(default_factory=list)
