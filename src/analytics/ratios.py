"""
N100 Financial Intelligence Platform
Sprint 2 - Day 08

Financial Ratio Engine
Profitability Ratios
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

        Formula:
        Net Profit /
        (Equity Capital + Reserves)

        Returns:
            None if Equity <= 0
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

        Formula:
        EBIT /
        (Equity + Reserves + Borrowings)

        Returns:
            None if Capital <= 0
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

        Formula:
        Net Profit /
        Total Assets

        Returns:
            None if Total Assets <= 0
        """

        if total_assets is None or total_assets <= 0:
            return None

        return round(
            (net_profit / total_assets) * 100,
            2
        )

    # =====================================================
    # FINANCIAL SECTOR ROCE CHECK
    # =====================================================

    @staticmethod
    def is_financial_sector(broad_sector):
        """
        Returns True if company belongs
        to Financials sector.
        """

        if broad_sector is None:
            return False

        return str(broad_sector).strip().lower() == "financials"

    # =====================================================
    # ROCE BENCHMARK
    # =====================================================

    @staticmethod
    def roce_status(
        roce,
        broad_sector
    ):
        """
        Returns benchmark status.

        Financial companies:
            Benchmark not applicable.

        Others:
            Good >= 15%
            Average 10-15%
            Poor <10%
        """

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