"""
N100 Financial Intelligence Platform
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from dataclasses import dataclass


@dataclass
class CashFlowKPIs:
    """
    Cash Flow KPI Library
    """

    # =====================================================
    # FREE CASH FLOW
    # =====================================================

    @staticmethod
    def free_cash_flow(
        operating_activity,
        investing_activity
    ):
        """
        Free Cash Flow

        Formula:
        CFO + CFI

        (Investing cash flow is usually negative.)
        """

        return (
            (operating_activity or 0)
            +
            (investing_activity or 0)
        )

    # =====================================================
    # CFO QUALITY SCORE
    # =====================================================

    @staticmethod
    def cfo_quality_score(
        cfo,
        pat
    ):
        """
        CFO / PAT
        """

        if pat is None or pat == 0:
            return None

        score = cfo / pat

        if score > 1.0:
            return "High Quality"

        if score >= 0.5:
            return "Moderate"

        return "Accrual Risk"

    # =====================================================
    # CAPEX INTENSITY
    # =====================================================

    @staticmethod
    def capex_intensity(
        investing_activity,
        sales
    ):
        """
        |Investing Cash Flow|
        /
        Sales
        """

        if sales is None or sales == 0:
            return None, None

        pct = abs(
            investing_activity
        ) / sales * 100

        if pct < 3:

            label = "Asset Light"

        elif pct <= 8:

            label = "Moderate"

        else:

            label = "Capital Intensive"

        return round(pct, 2), label

    # =====================================================
    # FCF CONVERSION
    # =====================================================

    @staticmethod
    def fcf_conversion(
        free_cash_flow,
        operating_profit
    ):
        """
        FCF /
        Operating Profit
        """

        if operating_profit is None or operating_profit == 0:
            return None

        return round(
            free_cash_flow / operating_profit * 100,
            2
        )

    # =====================================================
    # SIGN HELPER
    # =====================================================

    @staticmethod
    def sign(value):

        if value > 0:
            return "+"

        if value < 0:
            return "-"

        return "0"

    # =====================================================
    # CAPITAL ALLOCATION PATTERN
    # =====================================================

    @staticmethod
    def capital_allocation_pattern(
        cfo,
        cfi,
        cff,
        quality="Moderate"
    ):
        """
        Determine capital allocation pattern.
        """

        s1 = CashFlowKPIs.sign(cfo)
        s2 = CashFlowKPIs.sign(cfi)
        s3 = CashFlowKPIs.sign(cff)

        pattern = (s1, s2, s3)

        if pattern == ("+", "-", "-"):

            if quality == "High Quality":
                return "Shareholder Returns"

            return "Reinvestor"

        if pattern == ("+", "+", "-"):
            return "Liquidating Assets"

        if pattern == ("-", "+", "+"):
            return "Distress Signal"

        if pattern == ("-", "-", "+"):
            return "Growth Funded by Debt"

        if pattern == ("+", "+", "+"):
            return "Cash Accumulator"

        if pattern == ("-", "-", "-"):
            return "Pre-Revenue"

        if pattern == ("+", "-", "+"):
            return "Mixed"

        return "Unknown"