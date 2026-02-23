import pytest
from agent.state import MonorepoConfig, PackageConfig

@pytest.fixture
def base_config():
    return MonorepoConfig(
        project_name="test-repo",
        package_manager="pnpm",
        monorepo_tool="turbo",
        packages=[PackageConfig(name="@repo/utils")],
        ci_provider="github-actions"
    )
