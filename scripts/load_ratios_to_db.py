"""
Sprint 2 - Load Financial Ratios into SQLite
"""

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    ROOT
    / "data"
    / "interim"
    / "validated"
    / "financial_ratios.csv"
)

DB_PATH = (
    ROOT
    / "db"
    / "nifty100.db"
)


def main():

    print("=" * 60)
    print("LOADING FINANCIAL RATIOS INTO SQLITE")
    print("=" * 60)

    # -----------------------------------------
    # Load CSV
    # -----------------------------------------

    df = pd.read_csv(CSV_PATH)

    print("CSV rows:", len(df))

    # -----------------------------------------
    # Remove duplicate technical columns
    # -----------------------------------------

    technical_columns = [
        "id",
        "id_bs",
        "id_cf",
        "id_company"
    ]

    df = df.drop(
        columns=[
            column
            for column in technical_columns
            if column in df.columns
        ],
        errors="ignore"
    )

    # -----------------------------------------
    # Connect database
    # -----------------------------------------

    conn = sqlite3.connect(DB_PATH)

    try:

        # -----------------------------------------
        # Replace ratio table
        # -----------------------------------------

        df.to_sql(
            "financial_ratios",
            conn,
            if_exists="replace",
            index=False
        )

        conn.commit()

        print("\nFinancial ratios loaded successfully.")

        # -----------------------------------------
        # Verify row count
        # -----------------------------------------

        count = conn.execute(
            "SELECT COUNT(*) FROM financial_ratios"
        ).fetchone()[0]

        print("Database rows:", count)

        # -----------------------------------------
        # Verify columns
        # -----------------------------------------

        columns = conn.execute(
            "PRAGMA table_info(financial_ratios)"
        ).fetchall()

        print("\nDatabase columns:")

        for column in columns:

            print(
                f"- {column[1]}"
            )

    except Exception as error:

        conn.rollback()

        print("\nROLLBACK EXECUTED")

        raise error

    finally:

        conn.close()


if __name__ == "__main__":

    main()