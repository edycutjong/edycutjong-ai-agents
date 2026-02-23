import sys
import os
import pytest

# Add project root to path so we can import 'agent' and 'config'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
