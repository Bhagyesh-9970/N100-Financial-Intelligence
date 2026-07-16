"""
=========================================================
Database Loader
Sprint 1 - Day 4
=========================================================
"""

from pathlib import Path
import sqlite3
import pandas as pd


class DatabaseLoader:

    def __init__(self):

        ROOT = Path(__file__).resolve().parents[2]

        self.db_path = ROOT / "db" / "nifty100.db"

        self.conn = sqlite3.connect(self.db_path)

        self.conn.execute("PRAGMA foreign_keys = ON")

    # --------------------------------------------------

    def load_table(self, dataframe, table_name):

        print(f"\nLoading {table_name}...")

        dataframe.to_sql(

            table_name,

            self.conn,

            if_exists="append",

            index=False

        )

        print(f"{len(dataframe)} rows inserted.")

    # --------------------------------------------------

    def commit(self):

        self.conn.commit()

    # --------------------------------------------------

    def rollback(self):

        self.conn.rollback()

    # --------------------------------------------------

    def close(self):

        self.conn.close()