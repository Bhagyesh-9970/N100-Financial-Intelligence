

from pathlib import Path
import pandas as pd


class DataValidator:
    """
    Base validation framework for the ETL pipeline.
    """

    def __init__(self):
        self.failures = []

    # =====================================================
    # LOG FAILURE
    # =====================================================

    def log_failure(
        self,
        rule,
        severity,
        table,
        company,
        year,
        message
    ):
        """
        Store validation failure.
        """

        self.failures.append({

            "rule": rule,
            "severity": severity,
            "table": table,
            "company": company,
            "year": year,
            "message": message

        })

    # =====================================================
    # GET FAILURES
    # =====================================================

    def get_failures(self):
        """
        Return all validation failures.
        """
        return pd.DataFrame(self.failures)

    # =====================================================
    # EXPORT FAILURES
    # =====================================================

    def export_failures(
        self,
        output_path="output/validation_failures.csv"
    ):
        """
        Export validation failures.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df = self.get_failures()

        df.to_csv(
            output_path,
            index=False
        )

        print(
            f"\nValidation report saved to: {output_path}"
        )

        return df

    # =====================================================
    # VALIDATION SUMMARY
    # =====================================================

    def summary(self):
        """
        Print validation summary.
        """

        df = self.get_failures()

        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)

        if df.empty:
            print("No validation failures found.")
            return

        print(f"Total Failures : {len(df)}")

        print("\nBy Severity:")

        print(
            df["severity"].value_counts()
        )

        print("\nBy Rule:")

        print(
            df["rule"].value_counts()
        )

    # =====================================================
    # CLEAR FAILURES
    # =====================================================

    def clear(self):
        """
        Clear validation results.
        """
        self.failures = []
        # =====================================================
    # DQ-01 : PRIMARY KEY UNIQUENESS
    # =====================================================

    def validate_primary_key(self, dataframe, column_name, table_name):
        """
        Validate uniqueness of a primary key column.
        """

        duplicates = dataframe[dataframe.duplicated(subset=[column_name], keep=False)]

        for _, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-01",
                severity="CRITICAL",
                table=table_name,
                company=row.get("company_name", "Unknown"),
                year=row.get("year", ""),
                message=f"Duplicate Primary Key: {column_name}"
            )

    # =====================================================
    # DQ-02 : COMPANY_ID + YEAR UNIQUENESS
    # =====================================================

    def validate_company_year(self, dataframe, table_name):
        """
        Validate uniqueness of (company_id, year).
        """

        duplicates = dataframe[
            dataframe.duplicated(
                subset=["company_id", "year"],
                keep=False
            )
        ]

        for _, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-02",
                severity="CRITICAL",
                table=table_name,
                company=row.get("company_name", "Unknown"),
                year=row.get("year", ""),
                message="Duplicate (company_id, year)"
            )

    # =====================================================
    # DQ-03 : FOREIGN KEY INTEGRITY
    # =====================================================

    def validate_foreign_key(
        self,
        child_dataframe,
        parent_dataframe,
        foreign_key,
        table_name
    ):
        """
        Check FK integrity.
        """

        valid_keys = set(parent_dataframe[foreign_key])

        invalid = child_dataframe[
            ~child_dataframe[foreign_key].isin(valid_keys)
        ]

        for _, row in invalid.iterrows():

            self.log_failure(
                rule="DQ-03",
                severity="CRITICAL",
                table=table_name,
                company=row.get("company_name", "Unknown"),
                year=row.get("year", ""),
                message=f"Invalid FK : {foreign_key}"
            )

    # =====================================================
    # DQ-04 : BALANCE SHEET EQUATION
    # Assets = Liabilities + Equity
    # =====================================================

    def validate_balance_sheet(
        self,
        dataframe,
        tolerance=0.01
    ):
        """
        Validate accounting equation.
        """

        for _, row in dataframe.iterrows():

            assets = row.get("total_assets", 0)
            liabilities = row.get("total_liabilities", 0)
            equity = row.get("total_equity", 0)

            if assets == 0:
                continue

            difference = abs(
                assets - (liabilities + equity)
            )

            if difference > assets * tolerance:

                self.log_failure(
                    rule="DQ-04",
                    severity="WARNING",
                    table="balancesheet",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="Assets != Liabilities + Equity"
                )

    # =====================================================
    # DQ-05 : OPERATING PROFIT MARGIN
    # =====================================================

    def validate_opm(self, dataframe):
        """
        Cross-check OPM.
        """

        for _, row in dataframe.iterrows():

            sales = row.get("sales", 0)
            operating_profit = row.get("operating_profit", 0)
            opm = row.get("opm", 0)

            if sales == 0:
                continue

            calculated = (operating_profit / sales) * 100

            if abs(calculated - opm) > 1:

                self.log_failure(
                    rule="DQ-05",
                    severity="WARNING",
                    table="profitandloss",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="OPM mismatch"
                )

    # =====================================================
    # DQ-06 : POSITIVE SALES
    # =====================================================

    def validate_positive_sales(self, dataframe):
        """
        Sales should never be negative.
        """

        invalid = dataframe[
            dataframe["sales"] < 0
        ]

        for _, row in invalid.iterrows():

            self.log_failure(
                rule="DQ-06",
                severity="CRITICAL",
                table="profitandloss",
                company=row.get("company_name", "Unknown"),
                year=row.get("year", ""),
                message="Negative Sales"
            )
        # =====================================================
    # DQ-07 : NET CASH VALIDATION
    # =====================================================

    def validate_net_cash(self, dataframe):

        for _, row in dataframe.iterrows():

            operating = row.get("cash_from_operating_activity", 0)
            investing = row.get("cash_from_investing_activity", 0)
            financing = row.get("cash_from_financing_activity", 0)
            net_cash = row.get("net_cash_flow", 0)

            calculated = operating + investing + financing

            if abs(calculated - net_cash) > 1:

                self.log_failure(
                    rule="DQ-07",
                    severity="WARNING",
                    table="cashflow",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="Net cash flow mismatch"
                )

    # =====================================================
    # DQ-08 : TAX RATE VALIDATION
    # =====================================================

    def validate_tax_rate(self, dataframe):

        for _, row in dataframe.iterrows():

            tax_rate = row.get("tax_rate", 0)

            if tax_rate < 0 or tax_rate > 100:

                self.log_failure(
                    rule="DQ-08",
                    severity="WARNING",
                    table="profitandloss",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="Invalid tax rate"
                )

    # =====================================================
    # DQ-09 : DIVIDEND PAYOUT LIMIT
    # =====================================================

    def validate_dividend(self, dataframe):

        for _, row in dataframe.iterrows():

            dividend = row.get("dividend", 0)
            profit = row.get("net_profit", 0)

            if dividend > profit and profit > 0:

                self.log_failure(
                    rule="DQ-09",
                    severity="WARNING",
                    table="analysis",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="Dividend exceeds profit"
                )

    # =====================================================
    # DQ-10 : URL VALIDATION
    # =====================================================

    def validate_url(self, dataframe, column="url"):

        for _, row in dataframe.iterrows():

            url = str(row.get(column, ""))

            if url and not url.startswith(("http://", "https://")):

                self.log_failure(
                    rule="DQ-10",
                    severity="INFO",
                    table="documents",
                    company=row.get("company_name", "Unknown"),
                    year="",
                    message="Invalid URL"
                )

    # =====================================================
    # DQ-11 : EPS SIGN CHECK
    # =====================================================

    def validate_eps(self, dataframe):

        for _, row in dataframe.iterrows():

            eps = row.get("eps", 0)
            profit = row.get("net_profit", 0)

            if (eps < 0 and profit > 0) or (eps > 0 and profit < 0):

                self.log_failure(
                    rule="DQ-11",
                    severity="WARNING",
                    table="financial_ratios",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message="EPS sign inconsistent with profit"
                )

    # =====================================================
    # DQ-12 : DUPLICATE TICKER
    # =====================================================

    def validate_duplicate_ticker(self, dataframe):

        duplicates = dataframe[
            dataframe.duplicated(
                subset=["ticker"],
                keep=False
            )
        ]

        for _, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-12",
                severity="CRITICAL",
                table="companies",
                company=row.get("company_name", "Unknown"),
                year="",
                message="Duplicate ticker"
            )

    # =====================================================
    # DQ-13 : YEAR COVERAGE
    # =====================================================

    def validate_year_coverage(self, dataframe):

        counts = dataframe.groupby("company_id")["year"].count()

        for company, total in counts.items():

            if total < 5:

                self.log_failure(
                    rule="DQ-13",
                    severity="WARNING",
                    table="financials",
                    company=company,
                    year="",
                    message="Less than 5 years of data"
                )

    # =====================================================
    # DQ-14 : MANDATORY NULL CHECK
    # =====================================================

    def validate_nulls(self, dataframe, columns):

        for column in columns:

            invalid = dataframe[
                dataframe[column].isna()
            ]

            for _, row in invalid.iterrows():

                self.log_failure(
                    rule="DQ-14",
                    severity="CRITICAL",
                    table="unknown",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message=f"Missing {column}"
                )

    # =====================================================
    # DQ-15 : DATA TYPE VALIDATION
    # =====================================================

    def validate_numeric(self, dataframe, columns):

        for column in columns:

            invalid = pd.to_numeric(
                dataframe[column],
                errors="coerce"
            ).isna()

            for _, row in dataframe[invalid].iterrows():

                self.log_failure(
                    rule="DQ-15",
                    severity="WARNING",
                    table="unknown",
                    company=row.get("company_name", "Unknown"),
                    year=row.get("year", ""),
                    message=f"{column} is not numeric"
                )

    # =====================================================
    # DQ-16 : DATASET COVERAGE
    # =====================================================

    def validate_dataset_not_empty(
        self,
        dataframe,
        table_name
    ):

        if dataframe.empty:

            self.log_failure(
                rule="DQ-16",
                severity="CRITICAL",
                table=table_name,
                company="",
                year="",
                message="Dataset is empty"
            )