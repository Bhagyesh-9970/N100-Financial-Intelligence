import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.nlp.parser import parse_analysis_file
from src.nlp.pros_cons_generator import generate_all_pros_cons
from src.analytics.cashflow_kpis import build_cashflow_intelligence
from src.reports.tearsheet import TearsheetReport
from src.reports.sector_report import SectorReport


def main():
    companies_df = pd.read_csv(ROOT / "data/interim/cleaned/companies.csv")
    companies_df = companies_df.rename(columns={"company_id": "company_id"})
    companies_df["company_id"] = companies_df["company_id"].astype(str)

    cashflow_df = pd.read_csv(ROOT / "data/interim/cleaned/cashflow.csv")
    profit_df = pd.read_csv(ROOT / "data/interim/cleaned/profitandloss.csv")
    balance_df = pd.read_csv(ROOT / "data/interim/cleaned/balancesheet.csv")
    ratios_df = pd.read_csv(ROOT / "data/interim/cleaned/financial_ratios.csv")
    sectors_df = pd.read_csv(ROOT / "data/interim/cleaned/sectors.csv")

    merged = cashflow_df.merge(profit_df[["company_id", "year", "sales", "operating_profit", "opm_percentage", "net_profit", "eps", "dividend_payout"]], on=["company_id", "year"], how="left")
    merged = merged.merge(balance_df[["company_id", "year", "borrowings", "equity_capital", "reserves", "total_assets"]], on=["company_id", "year"], how="left")
    merged = merged.merge(ratios_df[["company_id", "year", "return_on_equity_pct", "debt_to_equity", "interest_coverage", "free_cash_flow_cr", "earnings_per_share", "dividend_payout_ratio_pct", "cash_from_operations_cr"]], on=["company_id", "year"], how="left")
    merged = merged.merge(sectors_df[["company_id", "broad_sector"]], on="company_id", how="left")

    merged = merged.rename(columns={
        "operating_activity": "cash_from_operating_activity",
        "investing_activity": "cash_from_investing_activity",
        "financing_activity": "cash_from_financing_activity",
        "net_cash_flow": "net_cash_flow",
        "broad_sector": "sector",
        "return_on_equity_pct": "roe_pct",
        "opm_percentage": "opm_percentage",
        "dividend_payout_ratio_pct": "dividend_yield_pct",
        "earnings_per_share": "eps",
        "cash_from_operations_cr": "free_cash_flow_cr",
    })

    merged["company_name"] = merged["company_id"]
    merged["roce_pct"] = merged["operating_profit"] / merged.get("total_assets", 0) * 100
    merged = merged[merged["company_id"].isin(companies_df["company_id"].astype(str))]

    parse_analysis_file(ROOT / "data/raw/analysis/analysis.xlsx", ROOT / "output")
    generate_all_pros_cons(companies_df[["company_id"]], merged, output_dir=ROOT / "output")
    build_cashflow_intelligence(merged, output_dir=ROOT / "output")

    tearsheet_report = TearsheetReport(output_dir=ROOT / "reports/tearsheets")
    tearsheet_report.build_batch(companies_df[["company_id", "company_name"]], merged[["company_id", "sales", "net_profit"]], output_dir=ROOT / "reports/tearsheets")

    sector_report = SectorReport(output_dir=ROOT / "reports/sector")
    for sector_name, sector_df in companies_df.merge(sectors_df[["company_id", "broad_sector"]].rename(columns={"broad_sector": "sector"}), on="company_id", how="left").groupby("sector"):
        sector_report.build(sector_name, sector_df, output_path=ROOT / "reports/sector" / f"{sector_name}.pdf")

    print("Sprint 5 outputs generated")


if __name__ == "__main__":
    main()
