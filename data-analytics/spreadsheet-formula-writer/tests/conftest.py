import sys
from pathlib import Path

# Add project root to sys.path
# This file is in apps/agents/data-analytics/spreadsheet-formula-writer/tests/
# We want to add apps/agents/data-analytics/spreadsheet-formula-writer/ to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))
