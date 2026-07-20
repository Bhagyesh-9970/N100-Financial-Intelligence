"""
N100 Financial Intelligence Platform
Sprint 2

Financial Ratio Engine
Day 08 + Day 09
"""

import logging

logger = logging.getLogger(__name__)


class FinancialRatios:
    """
    Financial Ratio Calculation Library
    """

    # =====================================================
    # NET PROFIT MARGIN
    # =====================================================

    @staticmethod
    def net_profit_margin(net_profit, sales):
        """
        Net Profit Margin (%)

        Formula:
        Net Profit / Sales × 100

        Returns:
            None if Sales <= 0
        """

        if sales is None or sales <= 0:
            return None

        return round((net_profit / sales) * 100, 2)

    # =====================================================
    # OPERATING PROFIT MARGIN
    # =====================================================

    @staticmethod
    def operating_profit_margin(operating_profit, sales):
        """
        Operating Profit Margin (%)

        Formula:
        Operating Profit / Sales × 100

        Returns:
            None if Sales <= 0
        """

        if sales is None or sales <= 0:
            return None

        return round((operating_profit / sales) * 100, 2)

    # =====================================================
    # OPM CROSS CHECK
    # =====================================================

    @staticmethod
    def check_opm(
        calculated_opm,
        source_opm,
        company="",
        year="",
        tolerance=1.0
    ):
        """
        Compare calculated OPM with source OPM.

        Returns:
            True  -> Difference within tolerance
            False -> Difference exceeds tolerance
        """

        if calculated_opm is None or source_opm is None:
            return True

        difference = abs(calculated_opm - source_opm)

        if difference > tolerance:

            logger.warning(
                f"OPM Mismatch | "
                f"Company={company} | "
                f"Year={year} | "
                f"Calculated={calculated_opm:.2f} | "
                f"Source={source_opm:.2f} | "
                f"Difference={difference:.2f}"
            )

            return False

        return True

    # =====================================================
    # RETURN ON EQUITY (ROE)
    # =====================================================

    @staticmethod
    def roe(
        net_profit,
        equity_capital,
        reserves
    ):
        """
        Return on Equity (%)
        """

        equity = (
            (equity_capital or 0)
            + (reserves or 0)
        )

        if equity <= 0:
            return None

        return round(
            (net_profit / equity) * 100,
            2
        )

    # =====================================================
    # RETURN ON CAPITAL EMPLOYED (ROCE)
    # =====================================================

    @staticmethod
    def roce(
        ebit,
        equity_capital,
        reserves,
        borrowings
    ):
        """
        Return on Capital Employed (%)
        """

        capital = (
            (equity_capital or 0)
            + (reserves or 0)
            + (borrowings or 0)
        )

        if capital <= 0:
            return None

        return round(
            (ebit / capital) * 100,
            2
        )

    # =====================================================
    # RETURN ON ASSETS (ROA)
    # =====================================================

    @staticmethod
    def roa(
        net_profit,
        total_assets
    ):
        """
        Return on Assets (%)
        """

        if total_assets is None or total_assets <= 0:
            return None

        return round(
            (net_profit / total_assets) * 100,
            2
        )

    # =====================================================
    # FINANCIAL SECTOR CHECK
    # =====================================================

    @staticmethod
    def is_financial_sector(broad_sector):

        if broad_sector is None:
            return False

        return str(broad_sector).strip().lower() == "financials"

    # =====================================================
    # ROCE STATUS
    # =====================================================

    @staticmethod
    def roce_status(
        roce,
        broad_sector
    ):

        if roce is None:
            return "N/A"

        if FinancialRatios.is_financial_sector(
            broad_sector
        ):
            return "Sector Relative"

        if roce >= 15:
            return "Good"

        if roce >= 10:
            return "Average"

        return "Poor"

    # =====================================================
    # DEBT TO EQUITY
    # =====================================================

    @staticmethod
    def debt_to_equity(
        borrowings,
        equity_capital,
        reserves
    ):
        """
        Borrowings /
        (Equity + Reserves)

        Debt Free -> 0
        """

        borrowings = borrowings or 0

        if borrowings == 0:
            return 0

        equity = (
            (equity_capital or 0)
            + (reserves or 0)
        )

        if equity <= 0:
            return None

        return round(
            borrowings / equity,
            2
        )

    # =====================================================
    # HIGH LEVERAGE FLAG
    # =====================================================

    @staticmethod
    def high_leverage_flag(
        debt_equity,
        broad_sector
    ):

        if debt_equity is None:
            return False

        if FinancialRatios.is_financial_sector(
            broad_sector
        ):
            return False

        return debt_equity > 5

    # =====================================================
    # INTEREST COVERAGE RATIO
    # =====================================================

    @staticmethod
    def interest_coverage_ratio(
        operating_profit,
        other_income,
        interest
    ):
        """
        (Operating Profit + Other Income)
        /
        Interest
        """

        if interest is None or interest == 0:
            return None

        earnings = (
            (operating_profit or 0)
            + (other_income or 0)
        )

        return round(
            earnings / interest,
            2
        )

    # =====================================================
    # ICR LABEL
    # =====================================================

    @staticmethod
    def icr_label(
        interest
    ):

        if interest == 0:
            return "Debt Free"

        return ""

    # =====================================================
    # ICR WARNING
    # =====================================================

    @staticmethod
    def icr_warning(
        icr
    ):

        if icr is None:
            return False

        return icr < 1.5

    # =====================================================
    # NET DEBT
    # =====================================================

    @staticmethod
    def net_debt(
        borrowings,
        investments
    ):
        """
        Borrowings - Investments
        """

        return (
            (borrowings or 0)
            - (investments or 0)
        )

    # =====================================================
    # ASSET TURNOVER
    # =====================================================

    @staticmethod
    def asset_turnover(
        sales,
        total_assets
    ):
        """
        Sales /
        Total Assets
        """

        if total_assets is None or total_assets <= 0:
            return None

        return round(
            sales / total_assets,
            2
        )
    