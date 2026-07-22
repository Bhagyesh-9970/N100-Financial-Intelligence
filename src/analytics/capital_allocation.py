"""
N100 Financial Intelligence Platform
Sprint 2 - Day 11

Capital Allocation Engine
"""

from pathlib import Path
import pandas as pd

from src.analytics.cashflow_kpis import CashFlowKPIs


class CapitalAllocationEngine:
    """
    Generates capital allocation patterns
    for every company-year.
    """

    def __init__(self):

        self.output_dir = Path("output")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # =====================================================
    # PROCESS DATASET
    # =====================================================

    def process(self, dataframe):
        """
        Generate capital allocation labels.
        """

        records = []

        for _, row in dataframe.iterrows():

            cfo = row.get(
                "cash_from_operating_activity",
                0
            )

            cfi = row.get(
                "cash_from_investing_activity",
                0
            )

            cff = row.get(
                "cash_from_financing_activity",
                0
            )

            pat = row.get(
                "net_profit",
                0
            )

            quality = CashFlowKPIs.cfo_quality_score(
                cfo,
                pat
            )

            pattern = CashFlowKPIs.capital_allocation_pattern(
                cfo,
                cfi,
                cff,
                quality if quality else "Moderate"
            )

            records.append({

                "company_id":
                    row.get("company_id"),

                "year":
                    row.get("year"),

                "cfo_sign":
                    CashFlowKPIs.sign(cfo),

                "cfi_sign":
                    CashFlowKPIs.sign(cfi),

                "cff_sign":
                    CashFlowKPIs.sign(cff),

                "quality":
                    quality,

                "pattern_label":
                    pattern

            })

        result = pd.DataFrame(records)

        output_file = (
            self.output_dir /
            "capital_allocation.csv"
        )

        result.to_csv(
            output_file,
            index=False
        )

        print(
            f"\nCapital Allocation Report saved to:\n{output_file}"
        )

        return result