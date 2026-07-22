"""
N100 Financial Intelligence Platform
Sprint 2 - Day 10

CAGR Engine
"""

from enum import Enum


# =====================================================
# CAGR FLAGS
# =====================================================

class CAGRFlag(Enum):
    """
    Flags returned by the CAGR engine
    """

    NORMAL = "NORMAL"

    TURNAROUND = "TURNAROUND"

    DECLINE_TO_LOSS = "DECLINE_TO_LOSS"

    BOTH_NEGATIVE = "BOTH_NEGATIVE"

    ZERO_BASE = "ZERO_BASE"

    INSUFFICIENT = "INSUFFICIENT"


# =====================================================
# CAGR CALCULATOR
# =====================================================

class CAGRCalculator:
    """
    Compound Annual Growth Rate Engine
    """

    # =====================================================
    # GENERIC CAGR CALCULATION
    # =====================================================

    @staticmethod
    def calculate(
        start_value,
        end_value,
        years
    ):
        """
        CAGR Formula

        CAGR =
        ((End / Start)^(1/Years) - 1) * 100

        Returns
        -------
        tuple
            (cagr, flag)
        """

        # -----------------------------
        # Insufficient history
        # -----------------------------

        if years is None or years <= 0:

            return (
                None,
                CAGRFlag.INSUFFICIENT.value
            )

        # -----------------------------
        # Zero base
        # -----------------------------

        if start_value == 0:

            return (
                None,
                CAGRFlag.ZERO_BASE.value
            )

        # -----------------------------
        # Positive -> Positive
        # -----------------------------

        if start_value > 0 and end_value > 0:

            value = (
                (
                    end_value / start_value
                ) ** (1 / years) - 1
            ) * 100

            return (
                round(value, 2),
                CAGRFlag.NORMAL.value
            )

        # -----------------------------
        # Positive -> Negative
        # -----------------------------

        if start_value > 0 and end_value < 0:

            return (
                None,
                CAGRFlag.DECLINE_TO_LOSS.value
            )

        # -----------------------------
        # Negative -> Positive
        # -----------------------------

        if start_value < 0 and end_value > 0:

            return (
                None,
                CAGRFlag.TURNAROUND.value
            )

        # -----------------------------
        # Negative -> Negative
        # -----------------------------

        if start_value < 0 and end_value < 0:

            return (
                None,
                CAGRFlag.BOTH_NEGATIVE.value
            )

        return (
            None,
            CAGRFlag.INSUFFICIENT.value
        )

    # =====================================================
    # REVENUE CAGR
    # =====================================================

    @staticmethod
    def revenue_cagr(
        start_revenue,
        end_revenue,
        years
    ):

        return CAGRCalculator.calculate(
            start_revenue,
            end_revenue,
            years
        )

    # =====================================================
    # PAT CAGR
    # =====================================================

    @staticmethod
    def pat_cagr(
        start_profit,
        end_profit,
        years
    ):

        return CAGRCalculator.calculate(
            start_profit,
            end_profit,
            years
        )

    # =====================================================
    # EPS CAGR
    # =====================================================

    @staticmethod
    def eps_cagr(
        start_eps,
        end_eps,
        years
    ):

        return CAGRCalculator.calculate(
            start_eps,
            end_eps,
            years
        )

    # =====================================================
    # GENERIC CAGR FROM HISTORICAL SERIES
    # =====================================================

    @staticmethod
    def calculate_from_series(
        values,
        years
    ):
        """
        Parameters
        ----------
        values : list

            Historical values ordered
            from oldest to newest

        years : int

            CAGR period

        Returns
        -------
        (cagr, flag)
        """

        if values is None:

            return (
                None,
                CAGRFlag.INSUFFICIENT.value
            )

        if len(values) < years + 1:

            return (
                None,
                CAGRFlag.INSUFFICIENT.value
            )

        start = values[-(years + 1)]

        end = values[-1]

        return CAGRCalculator.calculate(
            start,
            end,
            years
        )

    # =====================================================
    # REVENUE CAGR WINDOWS
    # =====================================================

    @staticmethod
    def revenue_cagr_3yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            3
        )

    @staticmethod
    def revenue_cagr_5yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            5
        )

    @staticmethod
    def revenue_cagr_10yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            10
        )

    # =====================================================
    # PAT CAGR WINDOWS
    # =====================================================

    @staticmethod
    def pat_cagr_3yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            3
        )

    @staticmethod
    def pat_cagr_5yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            5
        )

    @staticmethod
    def pat_cagr_10yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            10
        )

    # =====================================================
    # EPS CAGR WINDOWS
    # =====================================================

    @staticmethod
    def eps_cagr_3yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            3
        )

    @staticmethod
    def eps_cagr_5yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            5
        )

    @staticmethod
    def eps_cagr_10yr(values):

        return CAGRCalculator.calculate_from_series(
            values,
            10
        )