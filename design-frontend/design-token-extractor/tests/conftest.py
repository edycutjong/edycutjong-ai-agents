import pytest
import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from agent.models import DesignToken, TokenSet

@pytest.fixture
def sample_tokens():
    return TokenSet(
        name="test-theme",
        tokens=[
            DesignToken(name="primary-500", value="#3B82F6", type="color", description="Primary brand color"),
            DesignToken(name="spacing-md", value="16px", type="spacing"),
            DesignToken(name="font-base", value="16px", type="fontSize"),
        ]
    )
