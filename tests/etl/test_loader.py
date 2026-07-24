"""
ETL Loader Tests
Sprint 1 - Day 5
"""

import unittest

from src.etl.excel_loader import ExcelLoader


class TestExcelLoader(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.loader = ExcelLoader(
            raw_data_path="data/raw"
        )

        cls.datasets = cls.loader.load_all_files()

    # =========================================================
    # TEST FILE DISCOVERY
    # =========================================================

    def test_excel_files_discovered(self):

        files = self.loader.discover_excel_files()

        self.assertGreater(
            len(files),
            0
        )

    # =========================================================
    # TEST DATASETS LOADED
    # =========================================================

    def test_datasets_loaded(self):

        self.assertGreater(
            len(self.datasets),
            0
        )

    # =========================================================
    # TEST REQUIRED DATASETS
    # =========================================================

    def test_required_datasets_exist(self):

        required_datasets = [

            "companies",
            "sectors",
            "peer_groups",
            "market_cap",
            "profitandloss",
            "balancesheet",
            "cashflow",
            "financial_ratios",
            "stock_prices",
            "documents",
            "analysis",
            "prosandcons"

        ]

        for dataset in required_datasets:

            self.assertIn(
                dataset,
                self.datasets
            )

    # =========================================================
    # TEST DATAFRAME TYPE
    # =========================================================

    def test_datasets_are_dataframes(self):

        import pandas as pd

        for name, df in self.datasets.items():

            self.assertIsInstance(
                df,
                pd.DataFrame
            )

    # =========================================================
    # TEST NO EMPTY DATASETS
    # =========================================================

    def test_datasets_are_not_empty(self):

        for name, df in self.datasets.items():

            self.assertGreater(
                len(df),
                0,
                msg=f"{name} dataset is empty"
            )

    # =========================================================
    # TEST COLUMN NORMALIZATION
    # =========================================================

    def test_columns_are_normalized(self):

        for name, df in self.datasets.items():

            for column in df.columns:

                self.assertEqual(
                    column,
                    column.lower()
                )

                self.assertNotIn(
                    " ",
                    column
                )


# =============================================================
# DIRECT EXECUTION
# =============================================================

if __name__ == "__main__":

    unittest.main()