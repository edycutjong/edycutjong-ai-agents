import pandas as pd
from typing import Optional

def parse_billing_csv(file_path: str, provider: str = "generic") -> pd.DataFrame:
    """
    Parses a cloud billing CSV file into a standardized DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {e}")

    # Basic normalization based on provider (this is a simplified example)
    if provider == "aws":
        # AWS CUR (Cost and Usage Report) typical columns mapping
        # Trying to find columns that match standard AWS CUR names
        column_mapping = {
            'lineItem/ProductCode': 'Service',
            'lineItem/ResourceId': 'ResourceID',
            'lineItem/UnblendedCost': 'Cost',
            'lineItem/CurrencyCode': 'Currency',
            'lineItem/UsageAmount': 'UsageAmount',
            'lineItem/UsageType': 'UsageUnit', # Rough mapping
            'lineItem/UsageStartDate': 'Date',
            'product/region': 'Region'
        }
        # Rename if columns exist
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        # Remove duplicate columns if any (keep first)
        df = df.loc[:, ~df.columns.duplicated()]

    elif provider == "gcp":
        # GCP Billing Export typical columns
        column_mapping = {
            'service.description': 'Service',
            'sku.id': 'ResourceID', # or resource.name
            'cost': 'Cost',
            'currency': 'Currency',
            'usage.amount': 'UsageAmount',
            'usage.unit': 'UsageUnit',
            'usage_start_time': 'Date',
            'location.location': 'Region'
        }
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        df = df.loc[:, ~df.columns.duplicated()]

    elif provider == "azure":
         # Azure Cost Management
        column_mapping = {
            'ServiceName': 'Service',
            'ResourceId': 'ResourceID',
            'Cost': 'Cost',
            'Currency': 'Currency',
            'Quantity': 'UsageAmount',
            'UnitOfMeasure': 'UsageUnit',
            'Date': 'Date',
            'Location': 'Region'
        }
        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        df = df.loc[:, ~df.columns.duplicated()]

    # Ensure required columns exist, fill with defaults if missing
    required_columns = ['Service', 'ResourceID', 'Cost', 'Date']
    for col in required_columns:
        if col not in df.columns:
            # If strictly required, we might raise an error, but for now let's just warn or fill
            df[col] = "Unknown" if col != 'Cost' else 0.0

    # Convert Cost to numeric
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce').fillna(0.0)

    # Convert Date to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    return df
