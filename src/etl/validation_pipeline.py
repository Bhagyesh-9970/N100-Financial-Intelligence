from pathlib import Path

from src.etl.validator import DataValidator


class ValidationPipeline:

    def __init__(self):

        self.validator = DataValidator()

        self.output_path = Path("data/interim/validated")
        self.output_path.mkdir(parents=True, exist_ok=True)

    def validate_all(self, datasets):

        self.validator.clear()

        validated = {}

        print("\n" + "=" * 60)
        print("VALIDATING DATASETS")
        print("=" * 60)

        # -----------------------------
        # Companies
        # -----------------------------
        if "companies" in datasets:

            df = datasets["companies"]

            self.validator.validate_dataset_not_empty(df, "companies")

            if "company_id" in df.columns:
                self.validator.validate_primary_key(
                    df,
                    "company_id",
                    "companies"
                )

            if "ticker" in df.columns:
                self.validator.validate_duplicate_ticker(df)

            validated["companies"] = df

        # -----------------------------
        # Profit & Loss
        # -----------------------------
        if "profitandloss" in datasets:

            df = datasets["profitandloss"]

            self.validator.validate_dataset_not_empty(
                df,
                "profitandloss"
            )

            if {"company_id", "year"}.issubset(df.columns):
                self.validator.validate_company_year(
                    df,
                    "profitandloss"
                )

            if "sales" in df.columns:
                self.validator.validate_positive_sales(df)

            if {"sales", "operating_profit", "opm"}.issubset(df.columns):
                self.validator.validate_opm(df)

            if "tax_rate" in df.columns:
                self.validator.validate_tax_rate(df)

            validated["profitandloss"] = df

        # -----------------------------
        # Balance Sheet
        # -----------------------------
        if "balancesheet" in datasets:

            df = datasets["balancesheet"]

            self.validator.validate_dataset_not_empty(
                df,
                "balancesheet"
            )

            if {
                "total_assets",
                "total_liabilities",
                "total_equity"
            }.issubset(df.columns):

                self.validator.validate_balance_sheet(df)

            validated["balancesheet"] = df

        # -----------------------------
        # Cash Flow
        # -----------------------------
        if "cashflow" in datasets:

            df = datasets["cashflow"]

            self.validator.validate_dataset_not_empty(
                df,
                "cashflow"
            )

            if {
                "cash_from_operating_activity",
                "cash_from_investing_activity",
                "cash_from_financing_activity",
                "net_cash_flow"
            }.issubset(df.columns):

                self.validator.validate_net_cash(df)

            validated["cashflow"] = df

        # -----------------------------
        # Financial Ratios
        # -----------------------------
        if "financial_ratios" in datasets:

            df = datasets["financial_ratios"]

            self.validator.validate_dataset_not_empty(
                df,
                "financial_ratios"
            )

            if {"eps", "net_profit"}.issubset(df.columns):
                self.validator.validate_eps(df)

            validated["financial_ratios"] = df

        # -----------------------------
        # Documents
        # -----------------------------
        if "documents" in datasets:

            df = datasets["documents"]

            self.validator.validate_dataset_not_empty(
                df,
                "documents"
            )

            if "url" in df.columns:
                self.validator.validate_url(df)

            validated["documents"] = df

        # -----------------------------
        # Analysis
        # -----------------------------
        if "analysis" in datasets:

            df = datasets["analysis"]

            self.validator.validate_dataset_not_empty(
                df,
                "analysis"
            )

            if {"dividend", "net_profit"}.issubset(df.columns):
                self.validator.validate_dividend(df)

            validated["analysis"] = df

        # -----------------------------
        # Remaining datasets
        # -----------------------------
        for table in [
            "prosandcons",
            "market_cap",
            "peer_groups",
            "sectors",
            "stock_prices"
        ]:

            if table in datasets:

                self.validator.validate_dataset_not_empty(
                    datasets[table],
                    table
                )

                validated[table] = datasets[table]

        self.validator.export_failures()

        self.validator.summary()

        for name, df in validated.items():

            df.to_csv(
                self.output_path / f"{name}.csv",
                index=False
            )

        return validated