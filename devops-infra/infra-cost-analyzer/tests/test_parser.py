import pytest
import pandas as pd
from io import StringIO
from agent.parser import parse_billing_csv

def test_parse_aws_billing():
    csv_data = """lineItem/ProductCode,lineItem/ResourceId,lineItem/UnblendedCost,lineItem/CurrencyCode,lineItem/UsageAmount,lineItem/UsageType,lineItem/UsageStartDate,product/region
AmazonEC2,i-001,1.2,USD,24.0,RunInstances,2023-10-01,us-east-1
"""
    file_obj = StringIO(csv_data)
    df = parse_billing_csv(file_obj, provider="aws")

    assert 'Service' in df.columns
    assert 'ResourceID' in df.columns
    assert df.iloc[0]['Service'] == 'AmazonEC2'
    assert df.iloc[0]['Cost'] == 1.2

def test_parse_gcp_billing():
    csv_data = """service.description,sku.id,cost,currency,usage.amount,usage.unit,usage_start_time,location.location
Compute Engine,instance-gcp-1,2.5,USD,24.0,hour,2023-10-01,us-central1
"""
    file_obj = StringIO(csv_data)
    df = parse_billing_csv(file_obj, provider="gcp")

    assert 'Service' in df.columns
    assert df.iloc[0]['Service'] == 'Compute Engine'
    assert df.iloc[0]['Cost'] == 2.5

def test_parse_invalid_csv():
    # Provide a CSV with header but invalid/missing expected columns
    file_obj = StringIO("invalid,csv\nval1,val2")
    # Should probably raise error or return partial df depending on implementation
    # Current impl expects specific columns or fills defaults
    df = parse_billing_csv(file_obj, provider="generic")
    assert 'Cost' in df.columns
    assert not df.empty
    assert df.iloc[0]['Cost'] == 0.0 # Default fill
