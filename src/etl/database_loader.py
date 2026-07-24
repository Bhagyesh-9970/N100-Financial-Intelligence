"""
N100 Financial Intelligence Platform
Database Loader
Sprint 1 - Database Layer

Responsibilities:
    1. Create SQLite database schema
    2. Load validated DataFrames into SQLite
    3. Respect foreign-key dependencies
    4. Convert data types safely
    5. Prevent duplicate primary-key insertion
    6. Handle invalid foreign keys safely
    7. Export load audit report
"""

from pathlib import Path
from datetime import datetime
import sqlite3

import pandas as pd


class DatabaseLoader:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        db_path="db/nifty100.db",
        audit_path="output/load_audit.csv"
    ):

        self.db_path = Path(db_path)

        self.audit_path = Path(audit_path)

        # Create parent directories
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.audit_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.audit = []

    # =========================================================
    # DATABASE CONNECTION
    # =========================================================

    def connect(self):

        conn = sqlite3.connect(

            str(self.db_path)

        )

        conn.execute(

            "PRAGMA foreign_keys = ON"

        )

        return conn

    # =========================================================
    # CREATE DATABASE SCHEMA
    # =========================================================

    def create_schema(self):

        print("\n" + "=" * 60)
        print("CREATING DATABASE SCHEMA")
        print("=" * 60)

        conn = self.connect()

        try:

            cursor = conn.cursor()

            # -------------------------------------------------
            # COMPANIES
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT UNIQUE NOT NULL,

                    company_name TEXT,

                    isin TEXT,

                    sector TEXT,

                    broad_sector TEXT,

                    industry TEXT

                )
                """
            )

            # -------------------------------------------------
            # PROFIT AND LOSS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS profitandloss (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT NOT NULL,

                    year TEXT,

                    sales REAL,

                    expenses REAL,

                    operating_profit REAL,

                    opm_percentage REAL,

                    other_income REAL,

                    interest REAL,

                    depreciation REAL,

                    profit_before_tax REAL,

                    tax_percentage REAL,

                    net_profit REAL,

                    eps REAL,

                    dividend_payout REAL,

                    FOREIGN KEY (

                        company_id

                    )

                    REFERENCES companies(company_id)

                )
                """
            )

            # -------------------------------------------------
            # BALANCE SHEET
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS balancesheet (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT NOT NULL,

                    year TEXT,

                    equity_capital REAL,

                    reserves REAL,

                    borrowings REAL,

                    other_liabilities REAL,

                    total_liabilities REAL,

                    fixed_assets REAL,

                    cwip REAL,

                    investments REAL,

                    other_asset REAL,

                    total_assets REAL,

                    FOREIGN KEY (

                        company_id

                    )

                    REFERENCES companies(company_id)

                )
                """
            )

            # -------------------------------------------------
            # CASH FLOW
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cashflow (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT NOT NULL,

                    year TEXT,

                    operating_activity REAL,

                    investing_activity REAL,

                    financing_activity REAL,

                    net_cash_flow REAL,

                    FOREIGN KEY (

                        company_id

                    )

                    REFERENCES companies(company_id)

                )
                """
            )

            # -------------------------------------------------
            # FINANCIAL RATIOS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS financial_ratios (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT NOT NULL,

                    year TEXT,

                    net_profit_margin_pct REAL,

                    operating_profit_margin_pct REAL,

                    return_on_equity_pct REAL,

                    debt_to_equity REAL,

                    interest_coverage REAL,

                    asset_turnover REAL,

                    free_cash_flow_cr REAL,

                    capex_cr REAL,

                    earnings_per_share REAL,

                    book_value_per_share REAL,

                    dividend_payout_ratio_pct REAL,

                    total_debt_cr REAL,

                    cash_from_operations_cr REAL,

                    FOREIGN KEY (

                        company_id

                    )

                    REFERENCES companies(company_id)

                )
                """
            )

            # -------------------------------------------------
            # DOCUMENTS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    document_type TEXT,

                    document_date TEXT,

                    document_url TEXT

                )
                """
            )

            # -------------------------------------------------
            # ANALYSIS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    analysis_type TEXT,

                    analysis_text TEXT,

                    analyst TEXT,

                    analysis_date TEXT

                )
                """
            )

            # -------------------------------------------------
            # PROS AND CONS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prosandcons (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    pros TEXT,

                    cons TEXT

                )
                """
            )

            # -------------------------------------------------
            # MARKET CAP
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS market_cap (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    year TEXT,

                    market_cap REAL,

                    market_cap_category TEXT,

                    rank INTEGER,

                    price REAL,

                    shares_outstanding REAL,

                    market_cap_cr REAL

                )
                """
            )

            # -------------------------------------------------
            # PEER GROUPS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS peer_groups (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    peer_group_name TEXT,

                    benchmark_company TEXT

                )
                """
            )

            # -------------------------------------------------
            # SECTORS
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sectors (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    sector TEXT,

                    broad_sector TEXT,

                    industry TEXT,

                    sub_industry TEXT

                )
                """
            )

            # -------------------------------------------------
            # STOCK PRICES
            # -------------------------------------------------

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stock_prices (

                    id INTEGER PRIMARY KEY,

                    company_id TEXT,

                    date TEXT,

                    open REAL,

                    high REAL,

                    low REAL,

                    close REAL,

                    volume REAL,

                    adjusted_close REAL

                )
                """
            )

            conn.commit()

            print(
                "[OK] Database schema created"
            )

        finally:

            conn.close()

    # =========================================================
    # CHECK TABLE EXISTS
    # =========================================================

    @staticmethod
    def table_exists(

        conn,

        table_name

    ):

        result = conn.execute(

            """
            SELECT name

            FROM sqlite_master

            WHERE type = 'table'

            AND name = ?

            """,

            (table_name,)

        ).fetchone()

        return result is not None

    # =========================================================
    # GET TABLE COLUMNS
    # =========================================================

    @staticmethod
    def get_table_columns(

        conn,

        table_name

    ):

        rows = conn.execute(

            f'PRAGMA table_info("{table_name}")'

        ).fetchall()

        return [

            row[1]

            for row in rows

        ]

    # =========================================================
    # GET FULL SCHEMA
    # =========================================================

    @staticmethod
    def get_table_schema(

        conn,

        table_name

    ):

        return conn.execute(

            f'PRAGMA table_info("{table_name}")'

        ).fetchall()

    # =========================================================
    # NORMALIZE COMPANY IDS
    # =========================================================

    @staticmethod
    def normalize_company_id(value):

        if pd.isna(value):

            return None

        value = str(value).strip().upper()

        if value in [

            "",

            "NAN",

            "NONE",

            "NULL"

        ]:

            return None

        return value

    # =========================================================
    # CONVERT INTEGER
    # =========================================================

    @staticmethod
    def convert_integer(value):

        if pd.isna(value):

            return None

        if isinstance(value, str):

            value = value.strip()

            if value == "":

                return None

        try:

            return int(

                float(value)

            )

        except (

            ValueError,

            TypeError

        ):

            return None

    # =========================================================
    # CONVERT REAL
    # =========================================================

    @staticmethod
    def convert_real(value):

        if pd.isna(value):

            return None

        if isinstance(value, str):

            value = value.strip()

            if value == "":

                return None

            # Remove common formatting
            value = (

                value
                .replace(",", "")
                .replace("₹", "")
                .replace("%", "")
            )

        try:

            return float(value)

        except (

            ValueError,

            TypeError

        ):

            return None

    # =========================================================
    # CONVERT TEXT
    # =========================================================

    @staticmethod
    def convert_text(value):

        if pd.isna(value):

            return None

        value = str(value).strip()

        if value.lower() in [

            "",

            "nan",

            "none",

            "null"

        ]:

            return None

        return value

    # =========================================================
    # CLEAN DATAFRAME TYPES
    # =========================================================

    def convert_dataframe_types(

        self,

        conn,

        table_name,

        df

    ):

        schema = self.get_table_schema(

            conn,

            table_name

        )

        for row in schema:

            column_name = row[1]

            column_type = (

                row[2] or ""

            ).upper()

            if column_name not in df.columns:

                continue

            # INTEGER
            if "INT" in column_type:

                df[column_name] = (

                    df[column_name]

                    .apply(

                        self.convert_integer

                    )

                )

            # REAL / NUMERIC
            elif any(

                data_type in column_type

                for data_type in [

                    "REAL",

                    "FLOAT",

                    "DOUBLE",

                    "NUMERIC",

                    "DECIMAL"

                ]

            ):

                df[column_name] = (

                    df[column_name]

                    .apply(

                        self.convert_real

                    )

                )

            # TEXT
            elif "TEXT" in column_type:

                df[column_name] = (

                    df[column_name]

                    .apply(

                        self.convert_text

                    )

                )

        return df

    # =========================================================
    # GET VALID COMPANY IDS
    # =========================================================

    @staticmethod
    def get_valid_company_ids(conn):

        rows = conn.execute(

            """
            SELECT company_id

            FROM companies

            WHERE company_id IS NOT NULL

            """

        ).fetchall()

        return set(

            row[0]

            for row in rows

        )

    # =========================================================
    # LOAD ONE TABLE
    # =========================================================

    def load_table(

        self,

        conn,

        table_name,

        df

    ):

        print(

            f"\nLoading {table_name}..."

        )

        # -----------------------------------------------------
        # CHECK TABLE
        # -----------------------------------------------------

        if not self.table_exists(

            conn,

            table_name

        ):

            print(

                f"[SKIPPED] Table does not exist: "

                f"{table_name}"

            )

            self.audit.append({

                "table": table_name,

                "status": "SKIPPED",

                "rows": 0,

                "error": "Table does not exist"

            })

            return

        # -----------------------------------------------------
        # COPY DATAFRAME
        # -----------------------------------------------------

        clean_df = df.copy()

        # -----------------------------------------------------
        # SPECIAL FIX FOR COMPANIES
        # -----------------------------------------------------

        if table_name == "companies":

            # Remove completely empty columns
            clean_df = clean_df.dropna(

                axis=1,

                how="all"

            )

        # -----------------------------------------------------
        # GET DATABASE COLUMNS
        # -----------------------------------------------------

        db_columns = self.get_table_columns(

            conn,

            table_name

        )

        print(

            "Database columns:"

        )

        print(

            db_columns

        )

        print(

            "Dataset columns:"

        )

        print(

            list(clean_df.columns)

        )

        # -----------------------------------------------------
        # MATCH COLUMNS
        # -----------------------------------------------------

        valid_columns = [

            column

            for column in clean_df.columns

            if column in db_columns

        ]

        print(

            "Matching columns:"

        )

        print(

            valid_columns

        )

        if not valid_columns:

            print(

                f"[SKIPPED] {table_name} "

                f"- no matching columns"

            )

            self.audit.append({

                "table": table_name,

                "status": "SKIPPED",

                "rows": 0,

                "error": "No matching columns"

            })

            return

        clean_df = clean_df[

            valid_columns

        ].copy()

        # -----------------------------------------------------
        # REMOVE EMPTY ROWS
        # -----------------------------------------------------

        clean_df = clean_df.dropna(

            how="all"

        )

        # -----------------------------------------------------
        # NORMALIZE COMPANY ID
        # -----------------------------------------------------

        if "company_id" in clean_df.columns:

            clean_df["company_id"] = (

                clean_df["company_id"]

                .apply(

                    self.normalize_company_id

                )

            )

        # -----------------------------------------------------
        # REMOVE NULL COMPANY IDS
        # -----------------------------------------------------

        if (

            "company_id"

            in clean_df.columns

            and table_name != "companies"

        ):

            clean_df = clean_df[

                clean_df["company_id"]

                .notna()

            ]

        # -----------------------------------------------------
        # CONVERT DATA TYPES
        # -----------------------------------------------------

        clean_df = (

            self.convert_dataframe_types(

                conn,

                table_name,

                clean_df

            )

        )

        # -----------------------------------------------------
        # FOREIGN KEY FILTERING
        # -----------------------------------------------------

        if (

            "company_id"

            in clean_df.columns

            and table_name != "companies"

        ):

            valid_company_ids = (

                self.get_valid_company_ids(

                    conn

                )

            )

            if valid_company_ids:

                before_count = len(

                    clean_df

                )

                clean_df = clean_df[

                    clean_df["company_id"]

                    .isin(

                        valid_company_ids

                    )

                ]

                removed_count = (

                    before_count
                    - len(clean_df)

                )

                if removed_count > 0:

                    print(

                        f"[WARNING] Removed "

                        f"{removed_count} rows "

                        f"with invalid "

                        f"company_id"

                    )

        # -----------------------------------------------------
        # REMOVE DUPLICATE PRIMARY KEYS
        # -----------------------------------------------------

        if "id" in clean_df.columns:

            clean_df = clean_df.drop_duplicates(

                subset=["id"]

            )

        # -----------------------------------------------------
        # HANDLE EXISTING IDS
        # -----------------------------------------------------

        if "id" in clean_df.columns:

            existing_ids = set(

                row[0]

                for row in conn.execute(

                    f'SELECT id FROM "{table_name}"'

                ).fetchall()

            )

            if existing_ids:

                clean_df = clean_df[

                    ~clean_df["id"]

                    .isin(

                        existing_ids

                    )

                ]

        # -----------------------------------------------------
        # EMPTY CHECK
        # -----------------------------------------------------

        if clean_df.empty:

            print(

                f"[SKIPPED] {table_name} "

                f"- no rows to insert"

            )

            self.audit.append({

                "table": table_name,

                "status": "SKIPPED",

                "rows": 0,

                "error": "No rows to insert"

            })

            return

        # -----------------------------------------------------
        # FINAL NaN CLEANUP
        # -----------------------------------------------------

        clean_df = clean_df.where(

            pd.notna(clean_df),

            None

        )

        # -----------------------------------------------------
        # INSERT
        # -----------------------------------------------------

        try:

            clean_df.to_sql(

                name=table_name,

                con=conn,

                if_exists="append",

                index=False

            )

        except Exception as error:

            print(

                f"\n[FAILED] {table_name}"

            )

            print(

                "Columns:"

            )

            print(

                list(clean_df.columns)

            )

            print(

                "Data types:"

            )

            print(

                clean_df.dtypes

            )

            print(

                "Sample data:"

            )

            print(

                clean_df.head()

            )

            raise error

        # -----------------------------------------------------
        # AUDIT
        # -----------------------------------------------------

        self.audit.append({

            "table": table_name,

            "status": "SUCCESS",

            "rows": len(clean_df),

            "error": ""

        })

        print(

            f"[OK] {table_name} "

            f"({len(clean_df)} rows)"

        )

    # =========================================================
    # LOAD ALL DATASETS
    # =========================================================

    def load_all(

        self,

        datasets

    ):

        print("\n" + "=" * 60)
        print("DATABASE LOAD")
        print("=" * 60)

        # -----------------------------------------------------
        # CREATE SCHEMA
        # -----------------------------------------------------

        self.create_schema()

        conn = self.connect()

        try:

            # -------------------------------------------------
            # IMPORTANT LOAD ORDER
            # -------------------------------------------------

            load_order = [

                "companies",

                "sectors",

                "peer_groups",

                "profitandloss",

                "balancesheet",

                "cashflow",

                "financial_ratios",

                "market_cap",

                "stock_prices",

                "documents",

                "analysis",

                "prosandcons"

            ]

            # -------------------------------------------------
            # LOAD IN ORDER
            # -------------------------------------------------

            for table_name in load_order:

                if table_name not in datasets:

                    continue

                self.load_table(

                    conn,

                    table_name,

                    datasets[table_name]

                )

            conn.commit()

            print(

                "\nDATABASE LOAD COMPLETED"

            )

        except Exception:

            conn.rollback()

            print(

                "\nROLLBACK EXECUTED"

            )

            raise

        finally:

            conn.close()

        self.export_audit()

    # =========================================================
    # EXPORT AUDIT
    # =========================================================

    def export_audit(self):

        if not self.audit:

            return

        audit_df = pd.DataFrame(

            self.audit

        )

        audit_df.insert(

            0,

            "timestamp",

            datetime.now().isoformat()

        )

        audit_df.to_csv(

            self.audit_path,

            index=False

        )

        print(

            "\nLoad audit exported -> "

            f"{self.audit_path}"

        )

    # =========================================================
    # VERIFY DATABASE
    # =========================================================

    def verify_database(self):

        conn = self.connect()

        try:

            tables = conn.execute(

                """
                SELECT name

                FROM sqlite_master

                WHERE type = 'table'

                ORDER BY name

                """

            ).fetchall()

            result = {}

            for row in tables:

                table_name = row[0]

                count = conn.execute(

                    f'SELECT COUNT(*) FROM "{table_name}"'

                ).fetchone()[0]

                result[table_name] = count

            return result

        finally:

            conn.close()


# =============================================================
# DIRECT EXECUTION
# =============================================================

if __name__ == "__main__":

    db = DatabaseLoader()

    db.create_schema()

    print(

        db.verify_database()

    )