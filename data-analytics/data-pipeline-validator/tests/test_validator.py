import pytest
import pandas as pd
from agent.core import DataValidator

def test_validate_counts_match(source_df, dest_df):
    validator = DataValidator()
    result = validator.validate_counts(source_df, dest_df)
    assert result['source_count'] == 5
    assert result['dest_count'] == 5
    assert result['match'] is True
    assert result['diff'] == 0

def test_validate_counts_mismatch(source_df, dest_df_mismatch):
    validator = DataValidator()
    result = validator.validate_counts(source_df, dest_df_mismatch)
    assert result['source_count'] == 5
    assert result['dest_count'] == 4
    assert result['match'] is False
    assert result['diff'] == -1

def test_validate_schema_match(source_df, dest_df):
    validator = DataValidator()
    result = validator.validate_schema(source_df, dest_df)
    assert result['schema_match'] is True
    assert not result['missing_columns']
    assert not result['type_mismatches']

def test_validate_schema_mismatch(source_df, dest_df_schema_change):
    validator = DataValidator()
    result = validator.validate_schema(source_df, dest_df_schema_change)
    assert result['schema_match'] is False
    assert 'id' in result['missing_columns']
    # user_id is extra, but missing_columns specifically looks for source columns missing in dest
    assert 'user_id' in result['extra_columns']
    # score type mismatch (float vs int)
    # Wait, pandas might cast int to int64 or int32 depending on platform
    # But source is float (80.5), dest is int (80)
    assert 'score' in result['type_mismatches']

def test_check_data_quality(source_df):
    validator = DataValidator()
    result = validator.check_data_quality(source_df, "source")
    assert result['label'] == "source"
    assert result['total_rows'] == 5
    assert result['duplicate_rows'] == 0
    assert not result['null_columns']

def test_compare_distributions(source_df, dest_df):
    validator = DataValidator()
    result = validator.compare_distributions(source_df, dest_df)
    assert 'score' in result
    assert result['score']['source_mean'] == result['score']['dest_mean']
    assert result['score']['mean_diff_pct'] == 0

def test_run_full_validation(source_df, dest_df):
    validator = DataValidator()
    result = validator.run_full_validation(source_df, dest_df)
    assert 'row_counts' in result
    assert 'schema' in result
    assert 'source_quality' in result
    assert 'dest_quality' in result
    assert 'distributions' in result
