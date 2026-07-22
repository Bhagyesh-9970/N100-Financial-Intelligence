"""
N100 Financial Intelligence Platform
Sprint 2 - Financial Ratio Engine

Combines:
    - Profit & Loss
    - Balance Sheet
    - Cash Flow
    - CAGR calculations

Generates financial KPIs for every company-year.
"""

import logging

import pandas as pd

from src.analytics.ratios import FinancialRatios
from src.analytics.cagr import CAGRCalculator
from src.analytics.cashflow_kpis import CashFlowKPIs


logger = logging.getLogger(__name__)


class RatioEngine:
    """
    Main financial ratio calculation engine.
    """

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):

        self.ratios = FinancialRatios()

        self.cagr = CAGRCalculator()

        self.cashflow = CashFlowKPIs()

    # =====================================================
    # SAFE NUMERIC VALUE
    # =====================================================

    @staticmethod
    def value(row, column, default=0):

        value = row.get(column, default)

        if pd.isna(value):

            return default

        return value

    # =====================================================
    # MAIN CALCULATION
    # =====================================================

    def calculate(self, dataframe):

        df = dataframe.copy()

        print("\nCalculating profitability ratios...")

        # =================================================
        # PROFITABILITY RATIOS
        # =================================================

        # Net Profit Margin
        df["net_profit_margin_pct"] = df.apply(
            lambda x: FinancialRatios.net_profit_margin(
                self.value(x, "net_profit"),
                self.value(x, "sales")
            ),
            axis=1
        )

        # Operating Profit Margin
        df["operating_profit_margin_pct"] = df.apply(
            lambda x: FinancialRatios.operating_profit_margin(
                self.value(x, "operating_profit"),
                self.value(x, "sales")
            ),
            axis=1
        )

        # ROE
        df["return_on_equity_pct"] = df.apply(
            lambda x: FinancialRatios.roe(
                self.value(x, "net_profit"),
                self.value(x, "equity_capital"),
                self.value(x, "reserves")
            ),
            axis=1
        )

        # ROCE
        df["return_on_capital_employed_pct"] = df.apply(
            lambda x: FinancialRatios.roce(
                self.value(x, "operating_profit")
                + self.value(x, "other_income"),
                self.value(x, "equity_capital"),
                self.value(x, "reserves"),
                self.value(x, "borrowings")
            ),
            axis=1
        )

        # ROA
        df["return_on_assets_pct"] = df.apply(
            lambda x: FinancialRatios.roa(
                self.value(x, "net_profit"),
                self.value(x, "total_assets")
            ),
            axis=1
        )

        # =================================================
        # LEVERAGE RATIOS
        # =================================================

        print("Calculating leverage ratios...")

        # Debt to Equity
        df["debt_to_equity"] = df.apply(
            lambda x: FinancialRatios.debt_to_equity(
                self.value(x, "borrowings"),
                self.value(x, "equity_capital"),
                self.value(x, "reserves")
            ),
            axis=1
        )

        # High Leverage Flag
        df["high_leverage_flag"] = df.apply(
            lambda x: FinancialRatios.high_leverage_flag(
                self.value(x, "debt_to_equity"),
                x.get("broad_sector", None)
            ),
            axis=1
        )

        # Interest Coverage Ratio
        df["interest_coverage"] = df.apply(
            lambda x: FinancialRatios.interest_coverage_ratio(
                self.value(x, "operating_profit"),
                self.value(x, "other_income"),
                self.value(x, "interest")
            ),
            axis=1
        )

        # ICR Label
        df["icr_label"] = df["interest_coverage"].apply(
            FinancialRatios.icr_label
        )

        # ICR Warning
        df["icr_warning_flag"] = df["interest_coverage"].apply(
            FinancialRatios.icr_warning
        )

        # Net Debt
        df["net_debt_cr"] = df.apply(
            lambda x: FinancialRatios.net_debt(
                self.value(x, "borrowings"),
                self.value(x, "investments")
            ),
            axis=1
        )

        # Asset Turnover
        df["asset_turnover"] = df.apply(
            lambda x: FinancialRatios.asset_turnover(
                self.value(x, "sales"),
                self.value(x, "total_assets")
            ),
            axis=1
        )

        # =================================================
        # CASH FLOW KPIs
        # =================================================

        print("Calculating cash flow KPIs...")

        # Free Cash Flow
        df["free_cash_flow_cr"] = df.apply(
            lambda x: CashFlowKPIs.free_cash_flow(
                self.value(x, "operating_activity"),
                self.value(x, "investing_activity")
            ),
            axis=1
        )

        # CFO Quality
        df["cfo_quality_score"] = df.apply(
            lambda x: CashFlowKPIs.cfo_quality_score(
                self.value(x, "operating_activity"),
                self.value(x, "net_profit")
            ),
            axis=1
        )

        # CFO Quality Label
        df["cfo_quality_label"] = df[
            "cfo_quality_score"
        ].apply(
            CashFlowKPIs.cfo_quality_label
        )

        # CapEx Intensity
        df["capex_intensity_pct"] = df.apply(
            lambda x: CashFlowKPIs.capex_intensity(
                self.value(x, "investing_activity"),
                self.value(x, "sales")
            ),
            axis=1
        )

        # CapEx Classification
        df["capex_classification"] = df[
            "capex_intensity_pct"
        ].apply(
            CashFlowKPIs.capex_classification
        )

        # FCF Conversion
        df["fcf_conversion_rate_pct"] = df.apply(
            lambda x: CashFlowKPIs.fcf_conversion_rate(
                self.value(x, "operating_activity"),
                self.value(x, "investing_activity"),
                self.value(x, "operating_profit")
            ),
            axis=1
        )

        # =================================================
        # EPS
        # =================================================

        df["earnings_per_share"] = df.apply(
            lambda x: self.value(x, "eps"),
            axis=1
        )

        # =================================================
        # BOOK VALUE PER SHARE
        # =================================================

        if "shares_outstanding" in df.columns:

            df["book_value_per_share"] = df.apply(
                lambda x: FinancialRatios.book_value_per_share(
                    self.value(x, "equity_capital")
                    + self.value(x, "reserves"),
                    self.value(x, "shares_outstanding")
                ),
                axis=1
            )

        else:

            df["book_value_per_share"] = None

        # =================================================
        # DIVIDEND PAYOUT RATIO
        # =================================================

        if "dividend_payout" in df.columns:

            df["dividend_payout_ratio_pct"] = df[
                "dividend_payout"
            ]

        else:

            df["dividend_payout_ratio_pct"] = None

        # =================================================
        # TOTAL DEBT
        # =================================================

        df["total_debt_cr"] = df.apply(
            lambda x: self.value(x, "borrowings"),
            axis=1
        )

        # =================================================
        # CASH FROM OPERATIONS
        # =================================================

        df["cash_from_operations_cr"] = df.apply(
            lambda x: self.value(
                x,
                "operating_activity"
            ),
            axis=1
        )

        # =================================================
        # CAGR CALCULATIONS
        # =================================================

        print("Calculating CAGR metrics...")

        if "company_id" in df.columns:

            df = df.sort_values(
                ["company_id", "year"]
            )

            # Revenue CAGR
            df["revenue_cagr_5yr"] = (
                df.groupby("company_id")["sales"]
                .transform(
                    lambda series:
                    self.cagr.rolling_cagr(
                        series,
                        years=5
                    )
                )
            )

            # PAT CAGR
            df["pat_cagr_5yr"] = (
                df.groupby("company_id")["net_profit"]
                .transform(
                    lambda series:
                    self.cagr.rolling_cagr(
                        series,
                        years=5
                    )
                )
            )

            # EPS CAGR
            df["eps_cagr_5yr"] = (
                df.groupby("company_id")["eps"]
                .transform(
                    lambda series:
                    self.cagr.rolling_cagr(
                        series,
                        years=5
                    )
                )
            )

        else:

            df["revenue_cagr_5yr"] = None

            df["pat_cagr_5yr"] = None

            df["eps_cagr_5yr"] = None

        # =================================================
        # COMPOSITE QUALITY SCORE
        # =================================================

        df["composite_quality_score"] = df.apply(
            self.calculate_quality_score,
            axis=1
        )

        print("Ratio calculations completed.")

        return df

    # =====================================================
    # QUALITY SCORE
    # =====================================================

    @staticmethod
    def calculate_quality_score(row):

        score = 0

        # Profitability
        if (
            row.get(
                "net_profit_margin_pct",
                0
            ) is not None
            and row.get(
                "net_profit_margin_pct",
                0
            ) > 10
        ):

            score += 25

        # ROE
        if (
            row.get(
                "return_on_equity_pct",
                0
            ) is not None
            and row.get(
                "return_on_equity_pct",
                0
            ) > 15
        ):

            score += 25

        # Leverage
        debt_equity = row.get(
            "debt_to_equity",
            0
        )

        if debt_equity is not None and debt_equity < 1:

            score += 25

        # Cash Flow
        cfo_quality = row.get(
            "cfo_quality_score",
            0
        )

        if cfo_quality is not None and cfo_quality >= 1:

            score += 25

        return score