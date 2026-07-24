"""
N100 Financial Intelligence Platform
Excel Data Loader

Responsibilities
-----------------
1. Discover Excel files
2. Detect header rows
3. Load Excel datasets
4. Normalize column names
5. Normalize company identifiers
6. Transform companies master dataset
7. Clean missing values and text
8. Return all datasets as pandas DataFrames
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


class ExcelLoader:
    """
    Loads all Excel datasets from the project raw data directory.
    """

    # ---------------------------------------------------------
    # INITIALIZATION
    # ---------------------------------------------------------

    def __init__(
        self,
        raw_dir: str = "data/raw"
    ) -> None:

        self.raw_dir = Path(raw_dir)

        self.dataset_files = {

            "analysis":
                self.raw_dir
                / "analysis"
                / "analysis.xlsx",

            "prosandcons":
                self.raw_dir
                / "analysis"
                / "prosandcons.xlsx",

            "documents":
                self.raw_dir
                / "documents"
                / "documents.xlsx",

            "balancesheet":
                self.raw_dir
                / "financials"
                / "balancesheet.xlsx",

            "cashflow":
                self.raw_dir
                / "financials"
                / "cashflow.xlsx",

            "financial_ratios":
                self.raw_dir
                / "financials"
                / "financial_ratios.xlsx",

            "profitandloss":
                self.raw_dir
                / "financials"
                / "profitandloss.xlsx",

            "companies":
                self.raw_dir
                / "master"
                / "companies.xlsx",

            "market_cap":
                self.raw_dir
                / "master"
                / "market_cap.xlsx",

            "peer_groups":
                self.raw_dir
                / "master"
                / "peer_groups.xlsx",

            "sectors":
                self.raw_dir
                / "master"
                / "sectors.xlsx",

            "stock_prices":
                self.raw_dir
                / "stock_prices"
                / "stock_prices.xlsx",
        }

    # =========================================================
    # TEXT NORMALIZATION
    # =========================================================

    @staticmethod
    def clean_text(value) -> str:

        if pd.isna(value):

            return ""

        value = str(value)

        value = value.replace(
            "\n",
            " "
        )

        value = value.replace(
            "\r",
            " "
        )

        value = value.replace(
            "\t",
            " "
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()

    # =========================================================
    # COLUMN NORMALIZATION
    # =========================================================

    @staticmethod
    def normalize_column_name(
        column
    ) -> str:

        column = ExcelLoader.clean_text(
            column
        )

        column = column.lower()

        column = re.sub(
            r"[^a-z0-9]+",
            "_",
            column
        )

        column = re.sub(
            r"_+",
            "_",
            column
        )

        column = column.strip(
            "_"
        )

        return column

    # =========================================================
    # DATASET NAME NORMALIZATION
    # =========================================================

    @staticmethod
    def normalize_dataset_name(
        file_name: str
    ) -> str:

        file_name = file_name.lower()

        file_name = file_name.replace(
            ".xlsx",
            ""
        )

        file_name = re.sub(
            r"[^a-z0-9]+",
            "_",
            file_name
        )

        return file_name.strip(
            "_"
        )

    # =========================================================
    # COMPANY ID NORMALIZATION
    # =========================================================

    @staticmethod
    def normalize_company_id(
        value
    ) -> Optional[str]:

        if pd.isna(value):

            return None

        value = str(value)

        value = value.replace(
            "\n",
            " "
        )

        value = value.replace(
            "\r",
            " "
        )

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        value = value.strip()

        if not value:

            return None

        if value.lower() in {
            "nan",
            "none",
            "null",
            "na",
            "n/a"
        }:

            return None

        return value.upper()

    # =========================================================
    # CLEAN DATAFRAME
    # =========================================================

    def clean_dataframe(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        df = df.copy()

        # ---------------------------------------------
        # Normalize column names
        # ---------------------------------------------

        df.columns = [

            self.normalize_column_name(
                column
            )

            for column in df.columns

        ]

        # ---------------------------------------------
        # Remove duplicate columns
        # ---------------------------------------------

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]

        # ---------------------------------------------
        # Clean object columns only
        # ---------------------------------------------

        for column in df.columns:

            if df[column].dtype == "object":

                df[column] = df[column].apply(
                    self.clean_text
                )

        # ---------------------------------------------
        # Convert empty strings to None
        # ---------------------------------------------

        df = df.replace(
            {
                "": None,
                "nan": None,
                "NaN": None,
                "NULL": None,
                "null": None,
                "N/A": None,
                "n/a": None
            }
        )

        return df

    # =========================================================
    # HEADER DETECTION
    # =========================================================

    def detect_header_row(
        self,
        file_path: Path,
        max_rows: int = 15
    ) -> int:

        preview = pd.read_excel(
            file_path,
            header=None,
            nrows=max_rows
        )

        best_row = 0

        best_score = -1

        for row_index in range(
            len(preview)
        ):

            row = preview.iloc[
                row_index
            ]

            values = []

            for value in row:

                if pd.isna(value):

                    continue

                value = self.clean_text(
                    value
                )

                if value:

                    values.append(
                        value
                    )

            if not values:

                continue

            score = 0

            # -----------------------------------------
            # Strong header keywords
            # -----------------------------------------

            header_keywords = {

                "id",
                "company_id",
                "company_name",
                "year",
                "date",
                "sales",
                "expenses",
                "profit",
                "net_profit",
                "sector",
                "open",
                "close",
                "volume",
                "pros",
                "cons",
                "website"

            }

            for value in values:

                normalized = self.normalize_column_name(
                    value
                )

                if normalized in header_keywords:

                    score += 10

            # -----------------------------------------
            # General header-like values
            # -----------------------------------------

            for value in values:

                normalized = self.normalize_column_name(
                    value
                )

                if (

                    normalized.isidentifier()

                    and len(normalized) <= 60

                ):

                    score += 1

            # -----------------------------------------
            # Ignore title rows
            # -----------------------------------------

            if len(values) == 1:

                score -= 5

            if score > best_score:

                best_score = score

                best_row = row_index

        return best_row

    # =========================================================
    # FILE LOADING
    # =========================================================

    def load_file(
        self,
        file_path: Path,
        dataset_name: Optional[str] = None
    ) -> pd.DataFrame:

        if not file_path.exists():

            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if dataset_name is None:

            dataset_name = self.normalize_dataset_name(
                file_path.name
            )

        header_row = self.detect_header_row(
            file_path
        )

        print(
            f"Loading: {file_path.name}"
        )

        print(
            f"Detected header row: {header_row}"
        )

        df = pd.read_excel(

            file_path,

            header=header_row

        )

        df = self.clean_dataframe(
            df
        )

        # =====================================================
        # DATASET-SPECIFIC TRANSFORMATIONS
        # =====================================================

        # -----------------------------------------------------
        # COMPANIES MASTER DATASET
        # -----------------------------------------------------

        if dataset_name == "companies":

            print(
                "Applying companies dataset transformation..."
            )

            # -------------------------------------------------
            # CRITICAL:
            #
            # companies.xlsx has:
            #
            # id              company_name
            # ABB             Abbott India Ltd
            # ADANIENT        Adani Enterprises Ltd
            #
            # Therefore:
            #
            # company_id = original id
            #
            # NOT company_name
            # -------------------------------------------------

            if "id" not in df.columns:

                raise ValueError(
                    "Companies dataset must contain 'id' column"
                )

            df["company_id"] = (

                df["id"]

                .apply(
                    self.normalize_company_id
                )

            )

            # Clean company name

            if "company_name" in df.columns:

                df["company_name"] = (

                    df["company_name"]

                    .apply(
                        self.clean_text
                    )

                )

            # Remove invalid company IDs

            df = df[
                df["company_id"].notna()
            ]

            df = df[
                df["company_id"] != ""
            ]

            # Remove duplicates

            df = df.drop_duplicates(

                subset=[
                    "company_id"
                ],

                keep="first"

            )

        # -----------------------------------------------------
        # ALL OTHER DATASETS
        # -----------------------------------------------------

        else:

            if "company_id" in df.columns:

                df["company_id"] = (

                    df["company_id"]

                    .apply(
                        self.normalize_company_id
                    )

                )

        # =====================================================
        # DATASET-SPECIFIC CLEANING
        # =====================================================

        # -----------------------------------------------------
        # YEAR
        # -----------------------------------------------------

        if "year" in df.columns:

            df["year"] = (

                df["year"]

                .apply(
                    self.clean_text
                )

            )

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------

        if "date" in df.columns:

            df["date"] = pd.to_datetime(

                df["date"],

                errors="coerce"

            )

            df["date"] = (

                df["date"]

                .dt.strftime(
                    "%Y-%m-%d"
                )

            )

        # -----------------------------------------------------
        # NUMERIC COLUMNS
        # -----------------------------------------------------

        numeric_columns = [

            "face_value",
            "book_value",
            "roce_percentage",
            "roe_percentage",

            "sales",
            "expenses",
            "operating_profit",
            "opm_percentage",
            "other_income",
            "interest",
            "depreciation",
            "profit_before_tax",
            "tax_percentage",
            "net_profit",
            "eps",
            "dividend_payout",

            "equity_capital",
            "reserves",
            "borrowings",
            "other_liabilities",
            "total_liabilities",
            "fixed_assets",
            "cwip",
            "investments",
            "other_asset",
            "total_assets",

            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow",

            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "capex_cr",
            "earnings_per_share",
            "book_value_per_share",
            "dividend_payout_ratio_pct",
            "total_debt_cr",
            "cash_from_operations_cr",

            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct",

            "index_weight_pct",

            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "volume",
            "adjusted_close",

            "compounded_sales_growth",
            "compounded_profit_growth",
            "stock_price_cagr",
            "roe"

        ]

        for column in numeric_columns:

            if column in df.columns:

                df[column] = pd.to_numeric(

                    df[column],

                    errors="coerce"

                )

        # =====================================================
        # REMOVE COMPLETELY EMPTY ROWS
        # =====================================================

        df = df.dropna(
            how="all"
        )

        # =====================================================
        # RESET INDEX
        # =====================================================

        df = df.reset_index(
            drop=True
        )

        print(

            f"[OK] "

            f"{dataset_name:<25}"

            f"{len(df):>6} rows | "

            f"{len(df.columns):>4} columns"

        )

        print(
            "     Columns:",
            list(df.columns)
        )

        return df

    # =========================================================
    # DISCOVER FILES
    # =========================================================

    def discover_files(self):

        print(
            "\n"
            + "=" * 60
        )

        print(
            "DISCOVERED EXCEL FILES"
        )

        print(
            "=" * 60
        )

        discovered = {}

        for dataset_name, file_path in (

            self.dataset_files.items()

        ):

            if file_path.exists():

                discovered[
                    dataset_name
                ] = file_path

                print(
                    file_path
                )

            else:

                print(
                    f"[MISSING] {file_path}"
                )

        return discovered

    # =========================================================
    # LOAD ALL DATASETS
    # =========================================================

    def load_all(
        self
    ) -> Dict[str, pd.DataFrame]:

        print(
            "\n"
            + "=" * 60
        )

        print(
            "LOADING DATASETS"
        )

        print(
            "=" * 60
        )

        files = self.discover_files()

        datasets = {}

        for dataset_name, file_path in files.items():

            try:

                df = self.load_file(

                    file_path,

                    dataset_name

                )

                datasets[
                    dataset_name
                ] = df

            except Exception as error:

                print(
                    f"[FAILED] {dataset_name}"
                )

                print(
                    f"Reason: {error}"
                )

                raise

        print(
            "\n"
            + "=" * 60
        )

        print(
            "DATA LOADING COMPLETE"
        )

        print(
            "=" * 60
        )

        print(
            f"Total datasets loaded: "
            f"{len(datasets)}"
        )

        return datasets


# =============================================================
# TEST EXECUTION
# =============================================================

if __name__ == "__main__":

    loader = ExcelLoader()

    data = loader.load_all()

    print(
        "\n"
        + "=" * 60
    )

    print(
        "DATASET SUMMARY"
    )

    print(
        "=" * 60
    )

    for name, df in data.items():

        print(

            f"{name:<25}"

            f"{len(df):>6} rows "

            f"{len(df.columns):>5} columns"

        )