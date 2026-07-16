"""
=========================================================
Validation Pipeline
N100 Financial Intelligence Platform

Sprint 1 - Day 3

Author : Bhagyesh Mali
=========================================================
"""

from src.etl.loader import ExcelLoader
from src.etl.validator import DataValidator


class ValidationPipeline:

    def __init__(self):

        self.loader = ExcelLoader("data/raw")
        self.validator = DataValidator()

    def run(self):

        print("\nLoading datasets...\n")

        datasets = self.loader.load_all_files()

        print("\nRunning Data Quality Checks...\n")

        # -------------------------
        # Companies
        # -------------------------

        if "companies" in datasets:

            companies = datasets["companies"]

            self.validator.validate_dataset_not_empty(
                companies,
                "companies"
            )

            self.validator.validate_primary_key(
                companies,
                "company_id",
                "companies"
            )

            self.validator.validate_duplicate_ticker(
                companies
            )

        # -------------------------
        # Profit & Loss
        # -------------------------

        if "profitandloss" in datasets:

            pnl = datasets["profitandloss"]

            self.validator.validate_company_year(
                pnl,
                "profitandloss"
            )

            self.validator.validate_positive_sales(
                pnl
            )

            self.validator.validate_opm(
                pnl
            )

            self.validator.validate_tax_rate(
                pnl
            )

            self.validator.validate_eps(
                pnl
            )

        # -------------------------
        # Balance Sheet
        # -------------------------

        if "balancesheet" in datasets:

            bs = datasets["balancesheet"]

            self.validator.validate_company_year(
                bs,
                "balancesheet"
            )

            self.validator.validate_balance_sheet(
                bs
            )

        # -------------------------
        # Cash Flow
        # -------------------------

        if "cashflow" in datasets:

            cf = datasets["cashflow"]

            self.validator.validate_company_year(
                cf,
                "cashflow"
            )

            self.validator.validate_net_cash(
                cf
            )

        # -------------------------
        # Analysis
        # -------------------------

        if "analysis" in datasets:

            self.validator.validate_dividend(
                datasets["analysis"]
            )

        # -------------------------
        # Documents
        # -------------------------

        if "documents" in datasets:

            self.validator.validate_url(
                datasets["documents"]
            )

        # -------------------------
        # Foreign Key Checks
        # -------------------------

        if "companies" in datasets:

            companies = datasets["companies"]

            for table in [
                "profitandloss",
                "balancesheet",
                "cashflow",
                "analysis",
                "financial_ratios"
            ]:

                if table in datasets:

                    self.validator.validate_foreign_key(

                        datasets[table],

                        companies,

                        "company_id",

                        table

                    )

        print("\nValidation Complete\n")

        self.validator.summary()

        self.validator.export_failures()

        return datasets