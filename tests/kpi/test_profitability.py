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