import sys
import os
import subprocess

def main():
    """Main entry point for the Press Release Writer application."""

    # Check for CLI mode (placeholder)
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("CLI mode is currently under development. Please use the GUI for now.")
        return

    # Launch Streamlit Application
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")

    if not os.path.exists(script_path):
        print(f"Error: app.py not found at {script_path}")
        sys.exit(1)

    print(f"Starting Press Release Writer UI...")
    print(f"Running: streamlit run {script_path}")

    try:
        # Use sys.executable to ensure we use the same python environment
        subprocess.run([sys.executable, "-m", "streamlit", "run", script_path], check=True)
    except KeyboardInterrupt:
        print("\nStopping application...")
    except subprocess.CalledProcessError as e:
        print(f"\nStreamlit application crashed with error code {e.returncode}.")
    except FileNotFoundError:
        print("Error: 'streamlit' module not found. Please install dependencies via 'pip install -r requirements.txt'")

if __name__ == "__main__":
    main()
