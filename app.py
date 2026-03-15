"""Root entrypoint for Streamlit.

This file exists so that `streamlit run app.py` works from the project root,
as expected by the devcontainer.json configuration. All application logic
lives in _scripts/app.py.
"""
import importlib
import sys
from pathlib import Path

# Ensure _scripts is importable
scripts_dir = Path(__file__).parent / "_scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

# Import and run the actual app module
# Streamlit executes the top-level code on import, so importing is sufficient.
import runpy
runpy.run_path(str(scripts_dir / "app.py"), run_name="__main__")
