import pandas as pd

from src.etl.normaliser import DataNormalizer


def test_normalize_ticker_removes_suffix():
    assert DataNormalizer.normalize_ticker("tcs.ns") == "TCS"


def test_normalize_company_name_strips_whitespace():
    assert DataNormalizer.normalize_company_name("  Tata Ltd  ") == "Tata Ltd"


def test_normalize_year_handles_fy24():
    assert DataNormalizer.normalize_year("FY24") == 2024


def test_normalize_year_handles_range():
    assert DataNormalizer.normalize_year("2024-25") == 2024


def test_normalize_numeric_parses_commas_and_percent():
    assert DataNormalizer.normalize_numeric("1,234.5%") == 1234.5


def test_normalize_missing_replaces_empty_strings():
    assert DataNormalizer.normalize_missing("") is None


def test_normalize_missing_handles_na_values():
    assert DataNormalizer.normalize_missing(pd.NA) is None


def test_normalize_missing_handles_common_placeholders():
    assert DataNormalizer.normalize_missing("N/A") is None


def test_normalize_column_name_converts_spaces():
    assert DataNormalizer.normalize_column_name("Net Profit %") == "net_profit_pct"


def test_normalize_dataframe_drops_duplicates_and_changes_columns():
    df = pd.DataFrame({"Company Name": ["A", "A"], "Net Profit %": [10, 10]})
    normalized = DataNormalizer.normalize_dataframe(df)
    assert list(normalized.columns) == ["company_name", "net_profit_pct"]
    assert len(normalized) == 1
