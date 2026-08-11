import pandas as pd

from src.analytics.ratios import FinancialRatios


def test_roe_positive_equity():
    assert FinancialRatios.roe(100, 1000, 0) == 10.0


def test_roe_negative_equity():
    assert FinancialRatios.roe(100, -1000, 0) is None


def test_roe_zero_equity():
    assert FinancialRatios.roe(100, 0, 0) is None


def test_debt_free_ratio():
    assert FinancialRatios.debt_to_equity(0, 100, 50) == 0


def test_normal_debt_to_equity():
    assert FinancialRatios.debt_to_equity(100, 200, 50) == 0.5


def test_interest_coverage_normal():
    assert FinancialRatios.interest_coverage_ratio(100, 20, 20) == 6.0


def test_interest_coverage_zero_interest():
    assert FinancialRatios.interest_coverage_ratio(100, 20, 0) is None


def test_asset_turnover_normal():
    assert FinancialRatios.asset_turnover(1000, 2000) == 0.5


def test_net_profit_margin_zero_sales():
    assert FinancialRatios.net_profit_margin(100, 0) is None


def test_operating_profit_margin_normal():
    assert FinancialRatios.operating_profit_margin(100, 400) == 25.0


def test_opm_check():
    assert FinancialRatios.check_opm(25.0, 24.0, company="A", year="2024") is True


def test_opm_check_mismatch():
    assert FinancialRatios.check_opm(30.0, 24.0, company="A", year="2024") is False


def test_icr_warning():
    assert FinancialRatios.icr_warning(1.0) is True


def test_high_leverage_flag():
    assert FinancialRatios.high_leverage_flag(6, "Energy") is True


def test_high_leverage_flag_financials():
    assert FinancialRatios.high_leverage_flag(10, "Financials") is False


def test_roce_status_good():
    assert FinancialRatios.roce_status(20, "Energy") == "Good"


def test_roce_status_poor():
    assert FinancialRatios.roce_status(5, "Energy") == "Poor"


def test_roa_normal():
    assert FinancialRatios.roa(100, 1000) == 10.0


def test_roa_zero_assets():
    assert FinancialRatios.roa(100, 0) is None
