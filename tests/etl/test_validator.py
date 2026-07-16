from pathlib import Path
import sys
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.etl.validator import DataValidator

validator = DataValidator()

# -----------------------------
# DQ-01
# -----------------------------
companies = pd.DataFrame({
    "company_id": [1, 2, 2],
    "company_name": ["A", "B", "B"]
})

validator.validate_primary_key(
    companies,
    "company_id",
    "companies"
)

# -----------------------------
# DQ-02
# -----------------------------
financials = pd.DataFrame({
    "company_id": [1, 1],
    "year": [2024, 2024],
    "company_name": ["ABC", "ABC"]
})

validator.validate_company_year(
    financials,
    "profitandloss"
)
# -----------------------------
# DQ-07
# -----------------------------
cashflow = pd.DataFrame({
    "company_name":["ABC"],
    "year":[2024],
    "cash_from_operating_activity":[100],
    "cash_from_investing_activity":[-40],
    "cash_from_financing_activity":[10],
    "net_cash_flow":[80]
})

validator.validate_net_cash(cashflow)

# -----------------------------
# DQ-08
# -----------------------------
tax = pd.DataFrame({
    "company_name":["ABC"],
    "year":[2024],
    "tax_rate":[125]
})

validator.validate_tax_rate(tax)

# -----------------------------
# DQ-12
# -----------------------------
ticker = pd.DataFrame({
    "company_name":["A","B"],
    "ticker":["TCS","TCS"]
})

validator.validate_duplicate_ticker(ticker)

validator.summary()

validator.export_failures()