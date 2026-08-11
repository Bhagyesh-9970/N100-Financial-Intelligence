import pandas as pd

from src.nlp.parser import parse_analysis_text
from src.nlp.pros_cons_generator import generate_pros_cons
from src.analytics.cashflow_kpis import build_cashflow_intelligence


def test_parse_analysis_text_extracts_period_and_value():
    parsed = parse_analysis_text("10 Years: 21%")
    assert parsed == (10, 21.0)

    assert parse_analysis_text("not a match") is None


def test_generate_pros_cons_returns_pro_and_con_for_company():
    company_df = pd.DataFrame(
        [{
            "company_id": "TEST",
            "year": "2024",
            "sales": [100, 120, 140, 160, 180],
            "net_profit": [10, 12, 15, 18, 20],
            "operating_profit": [20, 24, 30, 34, 38],
            "equity_capital": [50, 55, 60, 64, 70],
            "reserves": [20, 22, 24, 26, 28],
            "borrowings": [10, 8, 6, 4, 2],
            "cash_from_operating_activity": [15, 18, 20, 21, 16],
            "cash_from_investing_activity": [-5, -6, -7, -6, -6],
            "cash_from_financing_activity": [-2, -3, -4, -5, -6],
            "dividend_payout": [30, 30, 30, 30, 30],
            "eps": [1.0, 1.2, 1.4, 1.7, 2.0],
            "interest": [1.0, 1.1, 1.2, 1.3, 1.4],
            "other_income": [1.0, 1.0, 1.0, 1.0, 1.0],
            "total_assets": [70, 72, 74, 76, 78],
        }]
    )
    rows = generate_pros_cons(company_df, company_id="TEST", company_name="Test Co")
    assert len(rows) >= 2
    assert any(r["type"] == "pro" for r in rows)
    assert any(r["type"] == "con" for r in rows)


def test_build_cashflow_intelligence_returns_expected_columns():
    df = pd.DataFrame([
        {
            "company_id": "TEST",
            "sector": "Industrials",
            "year": 2024,
            "cash_from_operating_activity": 120,
            "cash_from_investing_activity": -40,
            "cash_from_financing_activity": -20,
            "net_profit": 100,
            "sales": 1000,
            "borrowings": [30, 30, 30, 28, 25],
            "operating_profit": 200,
        }
    ])
    result = build_cashflow_intelligence(df)
    assert {"company_id", "sector", "cfo_quality_score", "cfo_quality_label"}.issubset(result.columns)
    assert result.loc[0, "company_id"] == "TEST"
