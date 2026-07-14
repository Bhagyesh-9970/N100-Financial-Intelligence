"""
=========================================================
Excel Loader
N100 Financial Intelligence Platform

Sprint 1 - Day 2

Author : Bhagyesh Mali
=========================================================
"""

from pathlib import Path
import pandas as pd

from src.etl.normaliser import DataNormalizer


class ExcelLoader:
    """
    Production-grade Excel Loader.

    Responsibilities
    ----------------
    1. Discover Excel files
    2. Validate file existence
    3. Validate extensions
    4. Read Excel
    5. Normalize dataframe
    6. Preview datasets
    7. Return cleaned DataFrames
    """

    def __init__(self, data_directory):
        self.data_directory = Path(data_directory)

    # =====================================================
    # FILE VALIDATION
    # =====================================================

    def file_exists(self, file_path):
        """Check if file exists."""
        return Path(file_path).exists()

    def validate_extension(self, file_path):
        """Allow only Excel files."""
        return Path(file_path).suffix.lower() in [
            ".xlsx",
            ".xls"
        ]

    # =====================================================
    # EXCEL READER
    # =====================================================

    def load_excel(self, file_path, sheet_name=0):
        """
        Read an Excel sheet.
        """

        file_path = Path(file_path)

        if not self.file_exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not self.validate_extension(file_path):
            raise ValueError(
                f"Invalid file extension: {file_path.suffix}"
            )

        dataframe = pd.read_excel(
            file_path,
            sheet_name=sheet_name
        )

        return dataframe

    # =====================================================
    # DATA CLEANING
    # =====================================================

    def clean_dataframe(self, dataframe):
        """
        Apply standard cleaning.
        """

        dataframe = DataNormalizer.normalize_dataframe(
            dataframe
        )

        dataframe.dropna(
            how="all",
            inplace=True
        )

        dataframe.reset_index(
            drop=True,
            inplace=True
        )

        return dataframe

    # =====================================================
    # COMPLETE PIPELINE
    # =====================================================

    def load_and_clean(self, file_path, sheet_name=0):
        """
        Read + Clean.
        """

        dataframe = self.load_excel(
            file_path,
            sheet_name
        )

        dataframe = self.clean_dataframe(
            dataframe
        )

        return dataframe

    # =====================================================
    # FILE DISCOVERY
    # =====================================================

    def discover_excel_files(self):
        """
        Discover every Excel file inside data directory.
        """

        excel_files = []

        for extension in ("*.xlsx", "*.xls"):

            excel_files.extend(
                self.data_directory.rglob(extension)
            )

        return sorted(excel_files)

    # =====================================================
    # LOAD SINGLE DATASET
    # =====================================================

    def load_dataset(self, filename, sheet_name=0):
        """
        Load one dataset by filename.

        Example:
        companies.xlsx
        """

        file_path = self.data_directory / filename

        dataframe = self.load_and_clean(
            file_path,
            sheet_name
        )

        return dataframe

    # =====================================================
    # LOAD ALL DATASETS
    # =====================================================

    def load_all_files(self):
        """
        Automatically load every Excel file.
        """

        datasets = {}

        excel_files = self.discover_excel_files()

        print()

        print("=" * 60)
        print("LOADING EXCEL FILES")
        print("=" * 60)

        for file in excel_files:

            try:

                dataframe = self.load_and_clean(file)

                datasets[file.stem] = dataframe

                print(
                    f"[SUCCESS] {file.name}"
                )

            except Exception as error:

                print(
                    f"[FAILED ] {file.name}"
                )

                print(error)

        print()

        return datasets

    # =====================================================
    # DATASET SUMMARY
    # =====================================================

    def dataset_summary(self, datasets):
        """
        Print dataset statistics.
        """

        print()

        print("=" * 60)
        print("DATASET SUMMARY")
        print("=" * 60)

        for name, dataframe in datasets.items():

            print()

            print(f"Dataset : {name}")

            print(
                f"Rows    : {len(dataframe)}"
            )

            print(
                f"Columns : {len(dataframe.columns)}"
            )

            print(
                f"Missing : {dataframe.isna().sum().sum()}"
            )

            print("-" * 60)

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview_dataset(
        self,
        datasets,
        dataset_name,
        rows=5
    ):
        """
        Preview dataset.
        """

        if dataset_name not in datasets:

            raise ValueError(
                f"{dataset_name} not loaded."
            )

        return datasets[dataset_name].head(rows)

    # =====================================================
    # LIST FILES
    # =====================================================

    def list_files(self):
        """
        Print discovered Excel files.
        """

        files = self.discover_excel_files()

        print()

        print("=" * 60)
        print("EXCEL FILES")
        print("=" * 60)

        for index, file in enumerate(files, start=1):

            print(
                f"{index}. {file.name}"
            )

        return files

    # =====================================================
    # GET ROW COUNTS
    # =====================================================

    def get_row_counts(self, datasets):
        """
        Return row count dictionary.
        """

        counts = {}

        for name, dataframe in datasets.items():

            counts[name] = len(dataframe)

        return counts

    # =====================================================
    # GET COLUMN COUNTS
    # =====================================================

    def get_column_counts(self, datasets):
        """
        Return column count dictionary.
        """

        counts = {}

        for name, dataframe in datasets.items():

            counts[name] = len(dataframe.columns)

        return counts

    # =====================================================
    # EXPORT SUMMARY
    # =====================================================

    def export_summary(
        self,
        datasets,
        output_path="output/load_summary.csv"
    ):
        """
        Export dataset statistics.
        """

        summary = []

        for name, dataframe in datasets.items():

            summary.append({

                "dataset": name,

                "rows": len(dataframe),

                "columns": len(dataframe.columns),

                "missing_values": dataframe.isna().sum().sum()

            })

        summary_df = pd.DataFrame(summary)

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        summary_df.to_csv(
            output_path,
            index=False
        )

        print()

        print(
            f"Summary exported -> {output_path}"
        )

        return summary_df