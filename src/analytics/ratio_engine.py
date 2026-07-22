"""
N100 Financial Intelligence Platform
Sprint 2 - Day 12

Financial Ratio Engine
"""

import pandas as pd

from src.analytics.ratios import FinancialRatios
from src.analytics.cashflow_kpis import CashFlowKPIs
from src.analytics.cagr import CAGRCalculator


class RatioEngine:
    """
    Computes all financial KPIs
    for every company-year.
    """

    def calculate(self, dataframe):

        df = dataframe.copy()

        # =====================================================
        # PROFITABILITY RATIOS
        # =====================================================

        df["net_profit_margin_pct"] = df.apply(
            lambda x: FinancialRatios.net_profit_margin(
                x["net_profit"],
                x["sales"]
            ),
            axis=1
        )

        df["operating_profit_margin_pct"] = df.apply(
            lambda x: FinancialRatios.operating_profit_margin(
                x["operating_profit"],
                x["sales"]
            ),
            axis=1
        )

        df["return_on_equity_pct"] = df.apply(
            lambda x: FinancialRatios.roe(
                x["net_profit"],
                x["equity_capital"],
                x["reserves"]
            ),
            axis=1
        )

        df["return_on_assets_pct"] = df.apply(
            lambda x: FinancialRatios.roa(
                x["net_profit"],
                x["total_assets"]
            ),
            axis=1
        )

        # =====================================================
        # LEVERAGE RATIOS
        # =====================================================

        df["debt_to_equity"] = df.apply(
            lambda x: FinancialRatios.debt_to_equity(
                x["borrowings"],
                x["equity_capital"],
                x["reserves"]
            ),
            axis=1
        )

        df["interest_coverage"] = df.apply(
            lambda x: FinancialRatios.interest_coverage_ratio(
                x["operating_profit"],
                x["other_income"],
                x["interest"]
            ),
            axis=1
        )

        df["asset_turnover"] = df.apply(
            lambda x: FinancialRatios.asset_turnover(
                x["sales"],
                x["total_assets"]
            ),
            axis=1
        )

        # =====================================================
        # CASH FLOW KPIs
        # =====================================================

        df["free_cash_flow_cr"] = df.apply(
            lambda x: CashFlowKPIs.free_cash_flow(
                x["cash_from_operating_activity"],
                x["cash_from_investing_activity"]
            ),
            axis=1
        )

        df["fcf_conversion_pct"] = df.apply(
            lambda x: CashFlowKPIs.fcf_conversion(
                x["free_cash_flow_cr"],
                x["operating_profit"]
            ),
            axis=1
        )

        return df