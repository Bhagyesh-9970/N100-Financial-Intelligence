"""
Sprint 2 Day 09

Leverage & Efficiency Ratio Tests
"""

import unittest

from src.analytics.ratios import FinancialRatios


class TestLeverageRatios(unittest.TestCase):

    # =====================================================
    # TEST 1
    # Debt Free Company
    # =====================================================

    def test_debt_equity_debt_free(self):

        result = FinancialRatios.debt_to_equity(
            0,
            500,
            500
        )

        self.assertEqual(result, 0)

    # =====================================================
    # TEST 2
    # Negative Equity
    # =====================================================

    def test_debt_equity_negative_equity(self):

        result = FinancialRatios.debt_to_equity(
            100,
            -500,
            100
        )

        self.assertIsNone(result)

    # =====================================================
    # TEST 3
    # Normal D/E
    # =====================================================

    def test_debt_equity_normal(self):

        result = FinancialRatios.debt_to_equity(
            300,
            400,
            600
        )

        self.assertEqual(result, 0.30)

    # =====================================================
    # TEST 4
    # High Leverage Flag
    # =====================================================

    def test_high_leverage_flag(self):

        result = FinancialRatios.high_leverage_flag(
            6.2,
            "Information Technology"
        )

        self.assertTrue(result)

    # =====================================================
    # TEST 5
    # Financial Sector Exemption
    # =====================================================

    def test_financial_sector_exemption(self):

        result = FinancialRatios.high_leverage_flag(
            8.5,
            "Financials"
        )

        self.assertFalse(result)

    # =====================================================
    # TEST 6
    # Interest = 0
    # =====================================================

    def test_interest_coverage_none(self):

        result = FinancialRatios.interest_coverage_ratio(
            500,
            100,
            0
        )

        self.assertIsNone(result)

    # =====================================================
    # TEST 7
    # Debt Free Label
    # =====================================================

    def test_debt_free_label(self):

        label = FinancialRatios.icr_label(0)

        self.assertEqual(label, "Debt Free")

    # =====================================================
    # TEST 8
    # ICR Warning
    # =====================================================

    def test_icr_warning(self):

        result = FinancialRatios.icr_warning(1.2)

        self.assertTrue(result)

    # =====================================================
    # BONUS TEST
    # Asset Turnover
    # =====================================================

    def test_asset_turnover(self):

        result = FinancialRatios.asset_turnover(
            1200,
            400
        )

        self.assertEqual(result, 3.00)

    # =====================================================
    # BONUS TEST
    # Net Debt
    # =====================================================

    def test_net_debt(self):

        result = FinancialRatios.net_debt(
            500,
            120
        )

        self.assertEqual(result, 380)


if __name__ == "__main__":

    unittest.main(verbosity=2)