"""
Database Loader
N100 Financial Intelligence Platform

Sprint 1 - Database Integration
"""

from pathlib import Path
import sqlite3
import pandas as pd


class DatabaseLoader:
    """
    Loads validated pandas DataFrames into SQLite database tables.
    """

    def __init__(
        self,
        db_path="db/nifty100.db"
    ):

        self.db_path = Path(db_path)

        # Ensure database directory exists
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.audit = []

    # =====================================================
    # GET TABLE COLUMNS
    # =====================================================

    def get_table_columns(
        self,
        conn,
        table_name
    ):
        """
        Return actual columns from SQLite table.
        """

        cursor = conn.execute(
            f'PRAGMA table_info("{table_name}")'
        )

        return [
            row[1]
            for row in cursor.fetchall()
        ]

    # =====================================================
    # CHECK TABLE EXISTS
    # =====================================================

    def table_exists(
        self,
        conn,
        table_name
    ):
        """
        Check whether table exists in SQLite database.
        """

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

    # =====================================================
    # LOAD ALL DATASETS
    # =====================================================

    def load_all(
        self,
        datasets
    ):
        """
        Load all validated datasets into SQLite.

        Parameters
        ----------
        datasets : dict
            Dictionary containing:

            {
                "companies": dataframe,
                "profitandloss": dataframe,
                ...
            }
        """

        print("\n" + "=" * 60)
        print("DATABASE LOAD")
        print("=" * 60)

        conn = sqlite3.connect(
            self.db_path
        )

        try:

            # Enable foreign key constraints
            conn.execute(
                "PRAGMA foreign_keys = ON"
            )

            # Process every dataset
            for table_name, df in datasets.items():

                print(
                    f"\nLoading {table_name}..."
                )

                try:

                    # ---------------------------------
                    # CHECK TABLE EXISTS
                    # ---------------------------------

                    if not self.table_exists(
                        conn,
                        table_name
                    ):

                        print(
                            f"[SKIPPED] "
                            f"Table does not exist: "
                            f"{table_name}"
                        )

                        self.audit.append({

                            "table": table_name,
                            "status": "SKIPPED",
                            "rows": 0,
                            "error":
                                "Table does not exist"

                        })

                        continue

                    # ---------------------------------
                    # GET DATABASE COLUMNS
                    # ---------------------------------

                    db_columns = (
                        self.get_table_columns(
                            conn,
                            table_name
                        )
                    )

                    # ---------------------------------
                    # DISPLAY SCHEMA
                    # ---------------------------------

                    print(
                        "Database columns:"
                    )

                    print(
                        db_columns
                    )

                    print(
                        "CSV columns:"
                    )

                    print(
                        list(df.columns)
                    )

                    # ---------------------------------
                    # FIND COMMON COLUMNS
                    # ---------------------------------

                    valid_columns = [

                        column

                        for column in df.columns

                        if column in db_columns

                    ]

                    print(
                        "Matching columns:"
                    )

                    print(
                        valid_columns
                    )

                    # ---------------------------------
                    # PROTECT AGAINST EMPTY INSERT
                    # ---------------------------------

                    if not valid_columns:

                        print(
                            f"[SKIPPED] "
                            f"{table_name} "
                            f"- no matching columns"
                        )

                        self.audit.append({

                            "table": table_name,
                            "status": "SKIPPED",
                            "rows": 0,
                            "error":
                                "No matching columns"

                        })

                        continue

                    # ---------------------------------
                    # SELECT COMMON COLUMNS
                    # ---------------------------------

                    clean_df = df[
                        valid_columns
                    ].copy()

                    # ---------------------------------
                    # REMOVE COMPLETELY EMPTY ROWS
                    # ---------------------------------

                    clean_df = clean_df.dropna(
                        how="all"
                    )

                    # ---------------------------------
                    # PROTECT AGAINST EMPTY DATASET
                    # ---------------------------------

                    if clean_df.empty:

                        print(
                            f"[SKIPPED] "
                            f"{table_name} "
                            f"- empty dataset"
                        )

                        self.audit.append({

                            "table": table_name,
                            "status": "SKIPPED",
                            "rows": 0,
                            "error":
                                "Empty dataset"

                        })

                        continue

                    # ---------------------------------
                    # INSERT DATA
                    # ---------------------------------

                    clean_df.to_sql(

                        name=table_name,

                        con=conn,

                        if_exists="append",

                        index=False

                    )

                    # ---------------------------------
                    # AUDIT SUCCESS
                    # ---------------------------------

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

                except Exception as e:

                    print(
                        f"[FAILED] {table_name}"
                    )

                    print(
                        "Error:",
                        str(e)
                    )

                    self.audit.append({

                        "table": table_name,

                        "status": "FAILED",

                        "rows": 0,

                        "error": str(e)

                    })

                    # Stop and rollback
                    raise

            # -----------------------------------------
            # COMMIT
            # -----------------------------------------

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

        # ---------------------------------------------
        # EXPORT AUDIT
        # ---------------------------------------------

        self.export_audit()

    # =====================================================
    # EXPORT AUDIT
    # =====================================================

    def export_audit(
        self,
        output_path="output/load_audit.csv"
    ):
        """
        Export database loading audit.
        """

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        audit_df = pd.DataFrame(
            self.audit
        )

        audit_df.to_csv(

            output_path,

            index=False

        )

        print(
            f"\nLoad audit exported -> "
            f"{output_path}"
        )