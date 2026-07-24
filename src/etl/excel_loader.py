"""
N100 Financial Intelligence Platform
Excel Loader

Responsibilities:
- Discover Excel files recursively
- Automatically detect header rows
- Load Excel workbooks
- Normalize column names
- Remove title rows
- Remove empty rows and columns
- Apply dataset-specific transformations
- Return datasets as a dictionary
"""

from pathlib import Path
import pandas as pd


class ExcelLoader:

    def __init__(self, raw_data_path="data/raw"):
        self.raw_data_path = Path(raw_data_path)

    # =========================================================
    # DISCOVER EXCEL FILES
    # =========================================================

    def discover_excel_files(self):

        if not self.raw_data_path.exists():
            raise FileNotFoundError(
                f"Raw data directory does not exist: "
                f"{self.raw_data_path}"
            )

        excel_files = sorted(
            self.raw_data_path.rglob("*.xlsx")
        )

        print("\n" + "=" * 60)
        print("DISCOVERED EXCEL FILES")
        print("=" * 60)

        for file_path in excel_files:
            print(file_path)

        return excel_files

    # =========================================================
    # NORMALIZE ONE COLUMN NAME
    # =========================================================

    @staticmethod
    def normalize_column_name(column):

        # Safely handle NaN column names
        if pd.isna(column):
            return "unnamed"

        column = str(column)

        column = column.strip().lower()

        replacements = {
            " ": "_",
            "%": "_pct",
            "+": "",
            "-": "_",
            "/": "_",
            "(": "",
            ")": "",
            ".": "",
            ",": "",
            ":": "",
            "&": "and"
        }

        for old, new in replacements.items():
            column = column.replace(old, new)

        # Remove duplicate underscores
        while "__" in column:
            column = column.replace(
                "__",
                "_"
            )

        # Remove leading/trailing underscores
        column = column.strip("_")

        if column == "":
            column = "unnamed"

        return column

    # =========================================================
    # NORMALIZE ALL COLUMN NAMES
    # =========================================================

    @classmethod
    def normalize_columns(cls, df):

        normalized_columns = []

        used_columns = {}

        for column in df.columns:

            clean_column = cls.normalize_column_name(
                column
            )

            # Handle duplicate column names
            if clean_column in used_columns:

                used_columns[clean_column] += 1

                clean_column = (
                    f"{clean_column}_"
                    f"{used_columns[clean_column]}"
                )

            else:

                used_columns[clean_column] = 0

            normalized_columns.append(
                clean_column
            )

        df.columns = normalized_columns

        return df

    # =========================================================
    # DETECT HEADER ROW
    # =========================================================

    def detect_header_row(
        self,
        file_path,
        max_rows=30
    ):

        preview = pd.read_excel(
            file_path,
            header=None,
            nrows=max_rows
        )

        expected_headers = {

            "id",
            "company_id",
            "company_name",
            "year",
            "sector",
            "isin",
            "sales",
            "revenue",
            "date",
            "close",
            "market_cap",
            "net_profit_margin_pct",
            "operating_profit_margin_pct"

        }

        best_row = 0

        best_score = 0

        for index, row in preview.iterrows():

            score = 0

            for value in row:

                # Ignore empty cells safely
                if pd.isna(value):
                    continue

                value = str(value)

                value = value.strip().lower()

                value = value.replace(
                    " ",
                    "_"
                )

                if value in expected_headers:
                    score += 1

            if score > best_score:

                best_score = score

                best_row = index

        return best_row

    # =========================================================
    # LOAD ONE EXCEL FILE
    # =========================================================

    def load_file(self, file_path):

        file_path = Path(file_path)

        # -----------------------------------------------------
        # Detect header row
        # -----------------------------------------------------

        header_row = self.detect_header_row(
            file_path
        )

        print(
            f"\nLoading: {file_path.name}"
        )

        print(
            f"Detected header row: {header_row}"
        )

        # -----------------------------------------------------
        # Read Excel file
        # -----------------------------------------------------

        df = pd.read_excel(

            file_path,

            header=header_row

        )

        # -----------------------------------------------------
        # Normalize columns
        # -----------------------------------------------------

        df = self.normalize_columns(
            df
        )

        # -----------------------------------------------------
        # Remove empty rows
        # -----------------------------------------------------

        df = df.dropna(
            how="all"
        )

        # -----------------------------------------------------
        # Remove empty columns
        # -----------------------------------------------------

        df = df.dropna(
            axis=1,
            how="all"
        )

        # -----------------------------------------------------
        # Reset index
        # -----------------------------------------------------

        df.reset_index(
            drop=True,
            inplace=True
        )

        # =====================================================
        # DATASET-SPECIFIC CLEANING
        # =====================================================

        dataset_name = file_path.stem.lower()

        # -----------------------------------------------------
        # COMPANIES DATASET
        # -----------------------------------------------------

        if dataset_name == "companies":

            print(
                "Applying companies dataset transformation..."
            )

            # Current companies dataset contains:
            #
            # id
            # company_logo
            # company_name
            # chart_link
            # about_company
            # website
            # nse_profile
            # bse_profile
            # face_value
            # book_value
            # roce_percentage
            # roe_percentage

            # The financial datasets use company ticker
            # values such as ABB, ACC, TCS, etc.
            #
            # Therefore create company_id from company_name.

            if "company_id" not in df.columns:

                if "company_name" not in df.columns:

                    raise ValueError(
                        "Companies dataset must contain "
                        "'company_name' to generate "
                        "'company_id'."
                    )

                df["company_id"] = (

                    df["company_name"]

                    .astype(str)

                    .str.strip()

                    .str.upper()

                )

            # Remove invalid company IDs

            invalid_values = [

                "",
                "NAN",
                "NONE",
                "NULL",
                "NA"

            ]

            df = df[
                ~df["company_id"].isin(
                    invalid_values
                )
            ]

        # -----------------------------------------------------
        # DATASETS WITH COMPANY_ID
        # -----------------------------------------------------

        if "company_id" in df.columns:

            df["company_id"] = (

                df["company_id"]

                .astype(str)

                .str.strip()

                .str.upper()

            )

            invalid_values = [

                "",
                "NAN",
                "NONE",
                "NULL",
                "NA"

            ]

            df = df[
                ~df["company_id"].isin(
                    invalid_values
                )
            ]

        # -----------------------------------------------------
        # NUMERIC ID
        # -----------------------------------------------------

        if "id" in df.columns:

            df["id"] = pd.to_numeric(

                df["id"],

                errors="coerce"

            )

        # -----------------------------------------------------
        # Remove rows where every value is empty
        # -----------------------------------------------------

        df = df.dropna(
            how="all"
        )

        # -----------------------------------------------------
        # Reset index again
        # -----------------------------------------------------

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    # =========================================================
    # DATASET NAME
    # =========================================================

    @staticmethod
    def get_dataset_name(file_path):

        return Path(
            file_path
        ).stem.lower()

    # =========================================================
    # LOAD ALL FILES
    # =========================================================

    def load_all(self):

        datasets = {}

        excel_files = (
            self.discover_excel_files()
        )

        print("\n" + "=" * 60)
        print("LOADING DATASETS")
        print("=" * 60)

        for file_path in excel_files:

            dataset_name = (
                self.get_dataset_name(
                    file_path
                )
            )

            try:

                df = self.load_file(
                    file_path
                )

                datasets[
                    dataset_name
                ] = df

                print(

                    f"[OK] "

                    f"{dataset_name:<25}"

                    f"{len(df):>8} rows | "

                    f"{len(df.columns):>4} columns"

                )

                print(

                    "     Columns:",

                    list(df.columns)

                )

            except Exception as error:

                print(

                    f"[FAILED] "

                    f"{dataset_name}"

                )

                print(

                    f"Reason: {error}"

                )

                raise

        print("\n" + "=" * 60)
        print("DATA LOADING COMPLETE")
        print("=" * 60)

        print(

            f"Total datasets loaded: "

            f"{len(datasets)}"

        )

        return datasets

    # =========================================================
    # COMPATIBILITY METHOD
    # =========================================================

    def load_all_files(self):

        return self.load_all()

    # =========================================================
    # DATASET SUMMARY
    # =========================================================

    def summary(self, datasets):

        print("\n" + "=" * 60)
        print("DATASET SUMMARY")
        print("=" * 60)

        for name, df in datasets.items():

            print(

                f"{name:<25}"

                f"{df.shape[0]:>8} rows"

                f"{df.shape[1]:>6} columns"

            )

    # =========================================================
    # COLUMN SUMMARY
    # =========================================================

    def column_summary(self, datasets):

        print("\n" + "=" * 60)
        print("COLUMN SUMMARY")
        print("=" * 60)

        for name, df in datasets.items():

            print(f"\n{name}")

            print("-" * 40)

            for column in df.columns:

                print(
                    f"  - {column}"
                )


# =============================================================
# DIRECT EXECUTION
# =============================================================

if __name__ == "__main__":

    loader = ExcelLoader()

    datasets = loader.load_all_files()

    loader.summary(
        datasets
    )

    loader.column_summary(
        datasets
    )