"""
Sprint 2 Day 08
Profitability Ratio Unit Tests
"""

import unittest

from src.analytics.ratios import FinancialRatios


class TestProfitabilityRatios(unittest.TestCase):

    # -------------------------------------------------
    # TEST 1
    # Net Profit Margin - Normal Case
    # -------------------------------------------------

    def test_net_profit_margin_normal(self):

        result = FinancialRatios.net_profit_margin(
            120,
            1000
        )

        self.assertEqual(result, 12.00)

    # -------------------------------------------------
    # TEST 2
    # Net Profit Margin - Sales = 0
    # -------------------------------------------------

    def test_net_profit_margin_zero_sales(self):

        result = FinancialRatios.net_profit_margin(
            100,
            0
        )

        self.assertIsNone(result)

    # -------------------------------------------------
    # TEST 3
    # Operating Margin
    # -------------------------------------------------

    def test_operating_margin(self):

        result = FinancialRatios.operating_profit_margin(
            250,
            1000
        )

        self.assertEqual(result, 25.00)

    # -------------------------------------------------
    # TEST 4
    # ROE
    # -------------------------------------------------

    def test_roe(self):

        result = FinancialRatios.roe(
            200,
            400,
            600
        )

        self.assertEqual(result, 20.00)

    # -------------------------------------------------
    # TEST 5
    # Negative Equity
    # -------------------------------------------------

    def test_roe_negative_equity(self):

        result = FinancialRatios.roe(
            100,
            -500,
            200
        )

        self.assertIsNone(result)

    # -------------------------------------------------
    # TEST 6
    # ROCE
    # -------------------------------------------------

    def test_roce(self):

        result = FinancialRatios.roce(
            300,
            500,
            500,
            500
        )

        self.assertEqual(result, 20.00)

    # -------------------------------------------------
    # TEST 7
    # ROA
    # -------------------------------------------------

    def test_roa(self):

        result = FinancialRatios.roa(
            200,
            4000
        )

        self.assertEqual(result, 5.00)

        # =====================================================
    # DEBT TO EQUITY RATIO
    # =====================================================

    @staticmethod
    def debt_to_equity(
        borrowings,
        equity_capital,
        reserves
    ):
        """
        Debt to Equity Ratio

        Formula:
        Borrowings /
        (Equity Capital + Reserves)

        Rules:
        - Borrowings = 0 → return 0
        - Equity <= 0 → return None
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
        """
        D/E > 5

        Financial sector is excluded.
        """

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
        Interest Coverage Ratio

        Formula:
        (Operating Profit + Other Income)
        /
        Interest

        interest = 0
            return None
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
        """
        Interest = 0

        Debt Free
        """

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
        """
        Warning when
        Interest Coverage < 1.5
        """

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
        Net Debt

        Borrowings - Investments
        """

        return (
            (borrowings or 0)
            -
            (investments or 0)
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
        Asset Turnover

        Sales /
        Total Assets
        """

        if total_assets is None or total_assets <= 0:
            return None

        return round(
            sales / total_assets,
            2
        )
    
    # -------------------------------------------------
    # TEST 8
    # OPM Cross Check
    # -------------------------------------------------

    def test_opm_mismatch(self):

        result = FinancialRatios.check_opm(
            20,
            23
        )

        self.assertFalse(result)


if __name__ == "__main__":

    unittest.main(verbosity=2)