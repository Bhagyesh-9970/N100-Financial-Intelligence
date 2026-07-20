"""
N100 Financial Intelligence Platform
Complete ETL Pipeline
Sprint 1 Day 5
"""

from datetime import datetime

from src.etl.loader import ExcelLoader
from src.etl.data_cleaner import DataCleaner
from src.etl.validation_pipeline import ValidationPipeline
from src.etl.database_loader import DatabaseLoader


def main():

    start = datetime.now()

    print("\n" + "=" * 70)
    print("N100 FINANCIAL INTELLIGENCE PLATFORM")
    print("COMPLETE ETL PIPELINE")
    print("=" * 70)

    # -------------------------------------------------
    # STEP 1 : Load Excel Files
    # -------------------------------------------------

    print("\nSTEP 1 : Loading Excel Files")

    loader = ExcelLoader()

    datasets = loader.load_all()

    loader.summary(datasets)

    # -------------------------------------------------
    # STEP 2 : Clean Data
    # -------------------------------------------------

    print("\nSTEP 2 : Cleaning Data")

    cleaner = DataCleaner()

    cleaned = cleaner.clean_all(datasets)

    # -------------------------------------------------
    # STEP 3 : Validate
    # -------------------------------------------------

    print("\nSTEP 3 : Running Data Quality Checks")

    validator = ValidationPipeline()

    validated = validator.validate_all(cleaned)

    # -------------------------------------------------
    # STEP 4 : Load SQLite
    # -------------------------------------------------

    print("\nSTEP 4 : Loading Database")

    db = DatabaseLoader()

    db.load_all(validated)

    end = datetime.now()

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nStarted :", start)
    print("Finished:", end)

    print(
        "Duration:",
        end - start
    )


if __name__ == "__main__":
    main()