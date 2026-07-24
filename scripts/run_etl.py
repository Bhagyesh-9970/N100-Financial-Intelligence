"""
N100 Financial Intelligence Platform
Complete ETL Pipeline
Sprint 1 Day 5
"""

import sys
from pathlib import Path
from datetime import datetime


# =========================================================
# ADD PROJECT ROOT TO PYTHON PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT)
    )


# =========================================================
# PROJECT IMPORTS
# =========================================================

from src.etl.loader import ExcelLoader
from src.etl.data_cleaner import DataCleaner
from src.etl.validation_pipeline import ValidationPipeline
from src.etl.database_loader import DatabaseLoader


# =========================================================
# MAIN ETL PIPELINE
# =========================================================

def main():

    start = datetime.now()

    print("\n" + "=" * 70)

    print(
        "N100 FINANCIAL INTELLIGENCE PLATFORM"
    )

    print(
        "COMPLETE ETL PIPELINE"
    )

    print("=" * 70)


    # -----------------------------------------------------
    # STEP 1 : LOAD EXCEL FILES
    # -----------------------------------------------------

    print(
        "\nSTEP 1 : Loading Excel Files"
    )

    loader = ExcelLoader()

    datasets = loader.load_all()

    loader.summary(
        datasets
    )


    # -----------------------------------------------------
    # STEP 2 : CLEAN DATA
    # -----------------------------------------------------

    print(
        "\nSTEP 2 : Cleaning Data"
    )

    cleaner = DataCleaner()

    cleaned = cleaner.clean_all(
        datasets
    )


    # -----------------------------------------------------
    # STEP 3 : VALIDATE DATA
    # -----------------------------------------------------

    print(
        "\nSTEP 3 : Running Data Quality Checks"
    )

    validator = ValidationPipeline()

    validated = validator.validate_all(
        cleaned
    )


    # -----------------------------------------------------
    # STEP 4 : LOAD SQLITE DATABASE
    # -----------------------------------------------------

    print(
        "\nSTEP 4 : Loading Database"
    )

    db = DatabaseLoader()

    db.load_all(
        validated
    )


    # -----------------------------------------------------
    # COMPLETION
    # -----------------------------------------------------

    end = datetime.now()

    print("\n" + "=" * 70)

    print(
        "PIPELINE COMPLETED SUCCESSFULLY"
    )

    print("=" * 70)

    print(
        "\nStarted :",
        start
    )

    print(
        "Finished:",
        end
    )

    print(
        "Duration:",
        end - start
    )


# =========================================================
# EXECUTION
# =========================================================

if __name__ == "__main__":

    main()