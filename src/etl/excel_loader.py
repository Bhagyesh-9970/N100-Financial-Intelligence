"""
N100 Financial Intelligence Platform
Sprint 1 - Day 5

Automatic Excel Loader

Responsibilities:
- Discover all Excel files inside data/raw/
- Load Excel workbooks
- Skip title rows
- Normalize column names
- Remove empty rows
- Return datasets as a dictionary
- Provide load_all_files() for ETL test compatibility
"""

from pathlib import Path
import pandas as pd


class ExcelLoader:
    """
    Automatically discovers and loads all Excel files
    inside the data/raw/ directory recursively.
    """

    def __init__(self, raw_data_path="data/raw"):
        self.raw_data_path = Path(raw_data_path)

    # =========================================================
    # DISCOVER EXCEL FILES
    # =========================================================

    def discover_excel_files(self):
        """
        Recursively find all .xlsx files inside raw_data_path.

        Returns:
            list[Path]
        """

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

        if not excel_files:
            print("No Excel files found.")

        for file_path in excel_files:
            print(file_path)

        return excel_files

    # =========================================================
    # NORMALIZE COLUMN NAMES
    # =========================================================

    @staticmethod
    def normalize_columns(df):
        """
        Normalize column names.

        Example:

        Company ID
            ->
        company_id

        OPM %
            ->
        opm_pct
        """

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
            .str.replace("%", "pct", regex=False)
            .str.replace("+", "", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("/", "_", regex=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
            .str.replace(".", "", regex=False)
        )

        return df

    # =========================================================
    # LOAD ONE EXCEL FILE
    # =========================================================

    def load_file(self, file_path):
        """
        Load and clean a single Excel file.

        The N100 Excel files contain a title row before
        the actual header row, therefore skiprows=1.

        Args:
            file_path: Path to Excel file

        Returns:
            pandas.DataFrame
        """

        file_path = Path(file_path)

        # -----------------------------------------------------
        # Read Excel
        # -----------------------------------------------------

        df = pd.read_excel(
            file_path,
            skiprows=1
        )

        # -----------------------------------------------------
        # Normalize column names
        # -----------------------------------------------------

        df = self.normalize_columns(df)

        # -----------------------------------------------------
        # Remove completely empty rows
        # -----------------------------------------------------

        df = df.dropna(
            how="all"
        )

        # -----------------------------------------------------
        # Remove completely empty columns
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

        return df

    # =========================================================
    # DATASET NAME
    # =========================================================

    @staticmethod
    def get_dataset_name(file_path):
        """
        Convert filename into dataset name.

        Example:

        profitandloss.xlsx
            ->
        profitandloss
        """

        return Path(file_path).stem.lower()

    # =========================================================
    # LOAD ALL EXCEL FILES
    # =========================================================

    def load_all(self):
        """
        Discover and load all Excel files.

        Returns:
            dict[str, pandas.DataFrame]
        """

        datasets = {}

        excel_files = self.discover_excel_files()

        print("\n" + "=" * 60)
        print("LOADING DATASETS")
        print("=" * 60)

        for file_path in excel_files:

            dataset_name = self.get_dataset_name(
                file_path
            )

            try:

                df = self.load_file(
                    file_path
                )

                datasets[dataset_name] = df

                print(
                    f"[OK] "
                    f"{dataset_name:<25}"
                    f"{len(df):>8} rows | "
                    f"{len(df.columns):>4} columns"
                )

            except Exception as error:

                print(
                    f"[FAILED] {dataset_name}"
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
        """
        Compatibility method required by the
        ETL test suite.

        This method delegates to load_all().
        """

        return self.load_all()

    # =========================================================
    # DATASET SUMMARY
    # =========================================================

    def summary(self, datasets):
        """
        Display a summary of loaded datasets.

        Args:
            datasets: Dictionary returned by load_all()
        """

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
        """
        Display columns for every dataset.
        """

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

    loader = ExcelLoader(
        raw_data_path="data/raw"
    )

    datasets = loader.load_all_files()

    loader.summary(
        datasets
    )

    loader.column_summary(
        datasets
    )