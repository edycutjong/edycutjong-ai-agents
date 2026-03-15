import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from agent.monorepo_agent import MonorepoAgent
from agent.state import MonorepoConfig

def test_agent_structure_creation(base_config):
    # Setup
    Path(base_config.project_name).mkdir(parents=True, exist_ok=True)
    if Path(base_config.project_name).exists():
        shutil.rmtree(base_config.project_name)

    # Mock Generator
    with patch("agent.monorepo_agent.MonorepoGenerator") as MockGenerator:
        mock_gen = MockGenerator.return_value
        mock_gen.generate_package_json.return_value = "{}"
        mock_gen.generate_tsconfig.return_value = "{}"
        mock_gen.generate_ci_config.return_value = "steps: []"
        mock_gen.generate_readme.return_value = "# README"

        agent = MonorepoAgent(base_config)
        agent.run()

        # Assertions
        root = Path(base_config.project_name)
        assert root.exists()
        assert (root / "apps").exists()
        assert (root / "packages").exists()
        assert (root / "package.json").exists()
        assert (root / "tsconfig.json").exists()
        assert (root / ".github/workflows/ci.yml").exists()
        assert (root / ".changeset/config.json").exists()

        # Check if utils package was created (from fixture)
        assert (root / "packages/utils").exists()

    # Cleanup
    if Path(base_config.project_name).exists():
        shutil.rmtree(base_config.project_name)


def test_get_context(base_config):
    """Cover agent/monorepo_agent.py line 15: _get_context returns model_dump."""
    with patch("agent.monorepo_agent.MonorepoGenerator"):
        agent = MonorepoAgent(base_config)
        ctx = agent._get_context()
        assert ctx["project_name"] == base_config.project_name
        assert isinstance(ctx, dict)


def test_nx_creates_tools_dir(tmp_path):
    """Cover agent/monorepo_agent.py line 32: nx creates tools/ directory."""
    nx_config = MonorepoConfig(
        project_name=str(tmp_path / "nx-project"),
        package_manager="pnpm",
        monorepo_tool="nx",
        packages=[],
        ci_provider="github-actions",
        include_changesets=False
    )

    with patch("agent.monorepo_agent.MonorepoGenerator") as MockGenerator:
        mock_gen = MockGenerator.return_value
        mock_gen.generate_package_json.return_value = "{}"
        mock_gen.generate_tsconfig.return_value = "{}"
        mock_gen.generate_ci_config.return_value = "steps: []"
        mock_gen.generate_readme.return_value = "# README"

        agent = MonorepoAgent(nx_config)
        agent.run()

        root = Path(nx_config.project_name)
        assert (root / "tools").exists()

    if root.exists():
        shutil.rmtree(str(root))
