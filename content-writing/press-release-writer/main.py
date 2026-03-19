import sys
import os
import subprocess

def main():
    """Main entry point for the Press Release Writer application."""

    # Check for CLI mode (placeholder)
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("CLI mode is currently under development. Please use the GUI for now.")  # pragma: no cover
        return  # pragma: no cover

    # Launch Streamlit Application
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")

    if not os.path.exists(script_path):
        print(f"Error: app.py not found at {script_path}")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

    print(f"Starting Press Release Writer UI...")
    print(f"Running: streamlit run {script_path}")

    try:
        # Use sys.executable to ensure we use the same python environment
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path], check=True)
    except KeyboardInterrupt:  # pragma: no cover
        print("\nStopping application...")  # pragma: no cover
    except subprocess.CalledProcessError as e:  # pragma: no cover
        print(f"\nStreamlit application crashed with error code {e.returncode}.")  # pragma: no cover
    except FileNotFoundError:  # pragma: no cover
        print("Error: 'streamlit' module not found. Please install dependencies via 'pip install -r requirements.txt'")  # pragma: no cover

if __name__ == "__main__":
    main()  # pragma: no cover
