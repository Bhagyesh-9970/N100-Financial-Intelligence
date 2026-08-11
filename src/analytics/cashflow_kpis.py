"""
N100 Financial Intelligence Platform
Sprint 2 - Day 11

Cash Flow KPI Engine
"""

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


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


def _cagr(values, years):
    if not values or len(values) < years + 1:
        return None
    try:
        start = values[-(years + 1)]
        end = values[-1]
    except Exception:
        return None
    if start in (0, None) or end in (0, None):
        return None
    try:
        result = ((end / start) ** (1 / years) - 1) * 100
    except Exception:
        return None
    if isinstance(result, complex):
        return None
    return round(float(result), 2)


def build_cashflow_intelligence(df, output_dir=None):
    output_dir = Path(output_dir or "output")
    output_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for company_id, company_df in df.groupby("company_id", sort=True):
        company_df = company_df.sort_values("year")
        latest = company_df.iloc[-1]
        cfo_values = company_df["cash_from_operating_activity"].astype(float).tolist()
        cfi_values = company_df["cash_from_investing_activity"].astype(float).tolist()
        cff_values = company_df["cash_from_financing_activity"].astype(float).tolist()
        pat_values = company_df["net_profit"].astype(float).tolist()

        cfo_quality_scores = [
            CashFlowKPIs.cfo_quality_score(cfo, pat)
            for cfo, pat in zip(cfo_values, pat_values)
        ]
        cfo_quality_score = round(
            sum(
                1 if score == "High Quality" else 0.5 if score == "Moderate" else 0
                for score in cfo_quality_scores
            ) / max(len(cfo_quality_scores), 1),
            2,
        )
        cfo_quality_label = (
            "High Quality"
            if cfo_quality_score > 0.8
            else "Moderate"
            if cfo_quality_score >= 0.5
            else "Accrual Risk"
        )

        capex_pct = None
        capex_label = None
        if not company_df.empty:
            capex_pct, capex_label = CashFlowKPIs.capex_intensity(
                latest.get("cash_from_investing_activity", 0),
                latest.get("sales", 0),
            )

        fcf_series = [
            CashFlowKPIs.free_cash_flow(cfo, cfi)
            for cfo, cfi in zip(cfo_values, cfi_values)
        ]
        fcf_cagr_5yr = _cagr(fcf_series, 5)
        fcf_conversion_pct = (
            CashFlowKPIs.fcf_conversion(
                fcf_series[-1],
                latest.get("operating_profit", 0),
            )
            if fcf_series
            else None
        )

        distress_flag = bool(
            latest.get("cash_from_operating_activity", 0) < 0
            and latest.get("cash_from_financing_activity", 0) > 0
        )
        deleveraging_flag = bool(
            latest.get("cash_from_financing_activity", 0) < 0
            and len(cff_values) > 1
            and cff_values[-1] < cff_values[-2]
        )
        capital_allocation_label = CashFlowKPIs.capital_allocation_pattern(
            latest.get("cash_from_operating_activity", 0),
            latest.get("cash_from_investing_activity", 0),
            latest.get("cash_from_financing_activity", 0),
            cfo_quality_label,
        )

        records.append({
            "company_id": company_id,
            "sector": latest.get("sector", ""),
            "cfo_quality_score": cfo_quality_score,
            "cfo_quality_label": cfo_quality_label,
            "capex_intensity_pct": capex_pct,
            "capex_label": capex_label,
            "fcf_cagr_5yr": fcf_cagr_5yr,
            "fcf_conversion_pct": fcf_conversion_pct,
            "distress_flag": distress_flag,
            "deleveraging_flag": deleveraging_flag,
            "capital_allocation_label": capital_allocation_label,
        })

    result = pd.DataFrame(records)
    output_path = output_dir / "cashflow_intelligence.xlsx"
    result.to_excel(output_path, index=False)

    distress_df = result[result["distress_flag"]].copy()
    distress_df.to_csv(output_dir / "distress_alerts.csv", index=False)
    return result