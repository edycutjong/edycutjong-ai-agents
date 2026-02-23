import os
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from agent.monorepo_agent import MonorepoAgent
from agent.state import MonorepoConfig

def test_agent_structure_creation(base_config):
    # Setup
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
