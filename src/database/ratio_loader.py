"""
N100 Financial Intelligence Platform
Sprint 2 - Day 12

Financial Ratio Database Loader
"""

import sqlite3
from pathlib import Path

import pandas as pd


class RatioLoader:
    """
    Loads calculated financial ratios
    into SQLite.
    """

    def __init__(
        self,
        database="data/database/nifty100.db"
    ):

        self.database = Path(database)

    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):

        return sqlite3.connect(
            self.database
        )

    # =====================================================
    # LOAD RATIOS
    # =====================================================

    def load(
        self,
        dataframe
    ):

        conn = self.connect()

        try:

            dataframe.to_sql(

                "financial_ratios",

                conn,

                if_exists="replace",

                index=False

            )

            conn.commit()

            print(
                "\nfinancial_ratios table loaded successfully."
            )

        finally:

            conn.close()

    # =====================================================
    # VERIFY
    # =====================================================

    def verify(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(

            """
            SELECT COUNT(*)
            FROM financial_ratios
            """
        )

        total = cursor.fetchone()[0]

        conn.close()

        print(
            f"\nRows loaded : {total}"
        )

        return total