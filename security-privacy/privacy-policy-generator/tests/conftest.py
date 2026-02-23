import sys
from pathlib import Path

# Add project root to sys.path
root = Path(__file__).parents[1]
sys.path.append(str(root))
