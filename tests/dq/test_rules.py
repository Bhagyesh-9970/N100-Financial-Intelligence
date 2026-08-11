import pandas as pd

from src.etl.validator import DataValidator


def test_primary_key_validation_flags_duplicates():
    validator = DataValidator()
    df = pd.DataFrame([{"company_id": "TCS", "company_name": "TCS"}, {"company_id": "TCS", "company_name": "TCS"}])
    validator.validate_primary_key(df, "company_id", "companies")
    assert not validator.get_failures().empty


def test_company_year_validation_flags_duplicates():
    validator = DataValidator()
    df = pd.DataFrame([{"company_id": "TCS", "year": 2024}, {"company_id": "TCS", "year": 2024}])
    validator.validate_company_year(df, "profitandloss")
    assert not validator.get_failures().empty


def test_foreign_key_validation_flags_invalid_parent():
    validator = DataValidator()
    child = pd.DataFrame([{"company_id": "XYZ", "year": 2024}])
    parent = pd.DataFrame([{"company_id": "TCS"}])
    validator.validate_foreign_key(child, parent, "company_id", "profitandloss")
    assert not validator.get_failures().empty


def test_balance_sheet_validation_flags_mismatch():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "total_assets": 100, "total_liabilities": 30, "total_equity": 60}])
    validator.validate_balance_sheet(df)
    assert not validator.get_failures().empty


def test_opm_validation_flags_mismatch():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "sales": 100, "operating_profit": 10, "opm": 30}])
    validator.validate_opm(df)
    assert not validator.get_failures().empty


def test_positive_sales_validation_flags_negative_sales():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "sales": -10}])
    validator.validate_positive_sales(df)
    assert not validator.get_failures().empty


def test_tax_rate_validation_flags_invalid_value():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "tax_rate": 120}])
    validator.validate_tax_rate(df)
    assert not validator.get_failures().empty


def test_dividend_validation_flags_excess():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "dividend": 100, "net_profit": 50}])
    validator.validate_dividend(df)
    assert not validator.get_failures().empty


def test_url_validation_flags_bad_url():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "url": "not-a-url"}])
    validator.validate_url(df, column="url")
    assert not validator.get_failures().empty


def test_eps_validation_flags_sign_mismatch():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "eps": 10, "net_profit": -5}])
    validator.validate_eps(df)
    assert not validator.get_failures().empty


def test_duplicate_ticker_validation_flags_duplicates():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "ticker": "TCS"}, {"company_name": "TCS", "ticker": "TCS"}])
    validator.validate_duplicate_ticker(df)
    assert not validator.get_failures().empty


def test_year_coverage_validation_flags_low_coverage():
    validator = DataValidator()
    df = pd.DataFrame([{"company_id": "TCS", "year": 2024}, {"company_id": "TCS", "year": 2025}])
    validator.validate_year_coverage(df)
    assert not validator.get_failures().empty


def test_null_validation_flags_missing_values():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "sales": None}])
    validator.validate_nulls(df, ["sales"])
    assert not validator.get_failures().empty


def test_numeric_validation_flags_non_numeric_values():
    validator = DataValidator()
    df = pd.DataFrame([{"company_name": "TCS", "year": 2024, "sales": "not-a-number"}])
    validator.validate_numeric(df, ["sales"])
    assert not validator.get_failures().empty
