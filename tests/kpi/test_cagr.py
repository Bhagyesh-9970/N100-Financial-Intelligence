"""
Sprint 2 - Day 10

Unit Tests for CAGR Engine
"""

import unittest

from src.analytics.cagr import (
    CAGRCalculator,
    CAGRFlag
)


class TestCAGRCalculator(unittest.TestCase):

    # =====================================================
    # TEST 1
    # Normal CAGR
    # =====================================================

    def test_normal_cagr(self):

        value, flag = CAGRCalculator.calculate(
            100,
            200,
            5
        )

        self.assertEqual(flag, CAGRFlag.NORMAL.value)

        self.assertIsNotNone(value)

    # =====================================================
    # TEST 2
    # Positive -> Negative
    # =====================================================

    def test_decline_to_loss(self):

        value, flag = CAGRCalculator.calculate(
            100,
            -50,
            5
        )

        self.assertIsNone(value)

        self.assertEqual(
            flag,
            CAGRFlag.DECLINE_TO_LOSS.value
        )

    # =====================================================
    # TEST 3
    # Negative -> Positive
    # =====================================================

    def test_turnaround(self):

        value, flag = CAGRCalculator.calculate(
            -100,
            50,
            5
        )

        self.assertIsNone(value)

        self.assertEqual(
            flag,
            CAGRFlag.TURNAROUND.value
        )

    # =====================================================
    # TEST 4
    # Negative -> Negative
    # =====================================================

    def test_both_negative(self):

        value, flag = CAGRCalculator.calculate(
            -100,
            -20,
            5
        )

        self.assertIsNone(value)

        self.assertEqual(
            flag,
            CAGRFlag.BOTH_NEGATIVE.value
        )

    # =====================================================
    # TEST 5
    # Zero Base
    # =====================================================

    def test_zero_base(self):

        value, flag = CAGRCalculator.calculate(
            0,
            200,
            5
        )

        self.assertIsNone(value)

        self.assertEqual(
            flag,
            CAGRFlag.ZERO_BASE.value
        )

    # =====================================================
    # TEST 6
    # Insufficient Years
    # =====================================================

    def test_insufficient(self):

        value, flag = CAGRCalculator.calculate(
            100,
            200,
            0
        )

        self.assertIsNone(value)

        self.assertEqual(
            flag,
            CAGRFlag.INSUFFICIENT.value
        )

    # =====================================================
    # TEST 7
    # Revenue CAGR
    # =====================================================

    def test_revenue_cagr(self):

        value, flag = CAGRCalculator.revenue_cagr(
            100,
            180,
            5
        )

        self.assertEqual(
            flag,
            CAGRFlag.NORMAL.value
        )

        self.assertIsNotNone(value)

    # =====================================================
    # TEST 8
    # PAT CAGR
    # =====================================================

    def test_pat_cagr(self):

        value, flag = CAGRCalculator.pat_cagr(
            100,
            300,
            5
        )

        self.assertEqual(
            flag,
            CAGRFlag.NORMAL.value
        )

        self.assertIsNotNone(value)

    # =====================================================
    # TEST 9
    # EPS CAGR
    # =====================================================

    def test_eps_cagr(self):

        value, flag = CAGRCalculator.eps_cagr(
            20,
            40,
            5
        )

        self.assertEqual(
            flag,
            CAGRFlag.NORMAL.value
        )

        self.assertIsNotNone(value)

    # =====================================================
    # TEST 10
    # Revenue CAGR from Series
    # =====================================================

    def test_revenue_cagr_5yr(self):

        values = [
            100,
            120,
            150,
            170,
            190,
            210
        ]

        value, flag = CAGRCalculator.revenue_cagr_5yr(
            values
        )

        self.assertEqual(
            flag,
            CAGRFlag.NORMAL.value
        )

        self.assertIsNotNone(value)


if __name__ == "__main__":

    unittest.main(verbosity=2)