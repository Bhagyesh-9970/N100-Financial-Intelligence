"""
N100 Financial Intelligence Platform
Sprint 2 Final Validation
"""

import sqlite3
import unittest

from src.analytics.ratios import FinancialRatios
from src.analytics.cagr import CAGRCalculator


DB_PATH = "db/nifty100.db"


class Sprint2Validation(unittest.TestCase):

    def test_database_exists(self):

        conn = sqlite3.connect(DB_PATH)

        tables = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        ).fetchall()

        conn.close()

        self.assertGreater(
            len(tables),
            0
        )

    def test_profitability_ratio(self):

        result = FinancialRatios.net_profit_margin(
            200,
            1000
        )

        self.assertEqual(
            result,
            20.0
        )

    def test_roe(self):

        result = FinancialRatios.roe(
            200,
            500,
            500
        )

        self.assertEqual(
            result,
            20.0
        )

    def test_debt_to_equity(self):

        result = FinancialRatios.debt_to_equity(
            500,
            1000
        )

        self.assertEqual(
            result,
            0.5
        )

    def test_cagr(self):

        result = CAGRCalculator.cagr(
            100,
            200,
            5
        )

        self.assertAlmostEqual(
            result,
            14.87,
            places=2
        )


if __name__ == "__main__":

    unittest.main()