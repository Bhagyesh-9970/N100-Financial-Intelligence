"""
Data Cleaning Pipeline
Sprint 1 - Day 5
"""

from pathlib import Path
import pandas as pd

from src.etl.normaliser import DataNormalizer


class DataCleaner:

    def __init__(self):

        self.normalizer = DataNormalizer()
        self.output_path = Path("data/interim/cleaned")

        self.output_path.mkdir(parents=True, exist_ok=True)

    def clean_dataframe(self, df):

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Standardize column names
        df.columns = [
            self.normalizer.normalize_column_name(col)
            for col in df.columns
        ]

        # Strip whitespace from column names
        df.columns = [
            col.strip()
            for col in df.columns
        ]

        # Strip whitespace from string values
        for col in df.columns:

            if df[col].dtype == object:

                df[col] = df[col].astype(str).str.strip()

        return df

    def clean_all(self, datasets):

        cleaned = {}

        print("\n" + "=" * 60)
        print("CLEANING DATASETS")
        print("=" * 60)

        for name, df in datasets.items():

            clean_df = self.clean_dataframe(df)

            cleaned[name] = clean_df

            output_file = self.output_path / f"{name}.csv"

            clean_df.to_csv(output_file, index=False)

            print(
                f"[OK] {name:<20}"
                f"{len(clean_df):>6} rows"
            )

        print("\nAll cleaned datasets saved.")

        return cleaned