"""
=========================================================
Database Manager
N100 Financial Intelligence Platform

Sprint 1 - Day 4

Author : Bhagyesh Mali
=========================================================
"""

import sqlite3
from pathlib import Path


class DatabaseManager:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.database_path = self.project_root / "db" / "nifty100.db"

        self.schema_path = self.project_root / "db" / "schema.sql"

        self.connection = None

    # ----------------------------------------------------

    def connect(self):

        self.connection = sqlite3.connect(self.database_path)

        self.connection.execute("PRAGMA foreign_keys = ON")

        print(f"\nConnected to database:\n{self.database_path}")

        return self.connection

    # ----------------------------------------------------

    def create_database(self):

        if self.connection is None:
            self.connect()

        with open(self.schema_path, "r", encoding="utf-8") as file:
            schema = file.read()

        self.connection.executescript(schema)

        self.connection.commit()

        print("\nDatabase schema created successfully.")

    # ----------------------------------------------------

    def list_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
        """)

        tables = cursor.fetchall()

        print("\nDATABASE TABLES")

        print("=" * 40)

        for table in tables:
            print(table[0])

    # ----------------------------------------------------

    def close(self):

        if self.connection:

            self.connection.close()

            print("\nDatabase connection closed.")