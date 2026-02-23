import pandas as pd
import requests

class DataLoader:
    @staticmethod
    def load_csv(file_buffer):
        """Loads data from a CSV file buffer (e.g., from st.file_uploader)."""
        try:
            # If it's bytes, wrap in BytesIO, but pandas often handles it if it has a read method
            # streamlit UploadedFile behaves like a file object
            df = pd.read_csv(file_buffer)
            return df
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")

    @staticmethod
    def load_api_json(url):
        """Loads data from a JSON API endpoint."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # If data is a list of dicts, pandas can handle it directly
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to find a list inside the dict (common API structure)
                found_list = False
                for key, value in data.items():
                    if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        df = pd.DataFrame(value)
                        found_list = True
                        break
                if not found_list:
                    # If no list found, treat as single record or key-value pairs
                    df = pd.DataFrame([data])
            else:
                raise ValueError("API response format not supported (must be JSON list or dict).")
            return df
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error fetching data from API: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing API data: {e}")
