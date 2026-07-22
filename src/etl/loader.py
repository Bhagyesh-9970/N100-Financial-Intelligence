"""
Automatic Excel Loader
Sprint 1 - Day 5
"""

from pathlib import Path
import pandas as pd


class ExcelLoader:
    """
    Automatically discovers and loads all Excel files
    inside data/raw/
    """

    def __init__(self, raw_data_path="data/raw"):
        self.raw_data_path = Path(raw_data_path)

    # =====================================================
    # DISCOVER EXCEL FILES
    # =====================================================

    def discover_excel_files(self):
        """
        Finds every .xlsx file recursively.
        """

        excel_files = list(self.raw_data_path.rglob("*.xlsx"))

        print("\n" + "=" * 60)
        print("DISCOVERED EXCEL FILES")
        print("=" * 60)

        for file in excel_files:
            print(file)

        return excel_files

    # =====================================================
    # LOAD ALL DATASETS
    # =====================================================

    def load_all(self):
        """
        Loads every Excel workbook.
        """

        datasets = {}

        excel_files = self.discover_excel_files()

        print("\n" + "=" * 60)
        print("LOADING DATASETS")
        print("=" * 60)

        for file in excel_files:

            dataset_name = file.stem.lower()

            try:

                # -------------------------------------------------
                # Read Excel
                # -------------------------------------------------

                df = pd.read_excel(
                    file,
                    skiprows=1
                )

                # -------------------------------------------------
                # Remove empty rows
                # -------------------------------------------------

                df = df.dropna(how="all")

                # -------------------------------------------------
                # Clean column names
                # -------------------------------------------------

                df.columns = (

                    df.columns
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .str.replace(" ", "_", regex=False)
                    .str.replace("%", "_pct", regex=False)
                    .str.replace("+", "", regex=False)
                    .str.replace("-", "_", regex=False)
                    .str.replace("/", "_", regex=False)
                    .str.replace("(", "", regex=False)
                    .str.replace(")", "", regex=False)
                    .str.replace(".", "", regex=False)

                )

                # -------------------------------------------------
                # Remove duplicate columns
                # -------------------------------------------------

                df = df.loc[:, ~df.columns.duplicated()]

                # -------------------------------------------------
                # Reset index
                # -------------------------------------------------

                df.reset_index(
                    drop=True,
                    inplace=True
                )

                datasets[dataset_name] = df

                print(
                    f"[OK] {dataset_name:<25}"
                    f"{len(df):>6} rows"
                )

            except Exception as e:

                print(f"[FAILED] {dataset_name}")
                print(e)

        print("\nTotal datasets loaded:", len(datasets))

        return datasets

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def summary(self, datasets):

        print("\n" + "=" * 60)
        print("DATASET SUMMARY")
        print("=" * 60)

        for name, df in datasets.items():

            print(
                f"{name:<25}"
                f"{df.shape[0]:>8} rows"
                f"{df.shape[1]:>6} cols"
            )

    # =====================================================
    # LIST FILES (Backward Compatibility)
    # =====================================================

    def list_files(self):
        """
        Compatibility method for older tests.
        """

        return self.discover_excel_files()