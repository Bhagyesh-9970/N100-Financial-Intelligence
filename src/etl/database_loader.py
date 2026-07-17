"""
Production SQLite Database Loader
Sprint 1 Day 5 Part 4
"""

from pathlib import Path
import sqlite3
import logging
import pandas as pd


class DatabaseLoader:

    def __init__(self):

        self.db_path = Path("db/nifty100.db")

        self.audit = []

        logging.basicConfig(

            filename="logs/etl.log",

            level=logging.INFO,

            format="%(asctime)s %(levelname)s %(message)s"

        )

    # ----------------------------------------
    # Connect
    # ----------------------------------------

    def connect(self):

        return sqlite3.connect(self.db_path)

    # ----------------------------------------
    # Load All
    # ----------------------------------------

    def load_all(self, datasets):

        conn = self.connect()

        cursor = conn.cursor()

        try:

            cursor.execute("BEGIN TRANSACTION")

            print("\n" + "="*60)
            print("LOADING DATABASE")
            print("="*60)

            for table, dataframe in datasets.items():

                dataframe.to_sql(

                    table,

                    conn,

                    if_exists="replace",

                    index=False

                )

                rows = len(dataframe)

                self.audit.append({

                    "table": table,

                    "rows": rows,

                    "status": "SUCCESS"

                })

                logging.info(

                    f"{table} loaded ({rows} rows)"

                )

                print(

                    f"[OK] {table:<20}{rows:>8} rows"

                )

            conn.commit()

            print("\nDatabase Load Complete.")

        except Exception as e:

            conn.rollback()

            logging.error(str(e))

            print("\nROLLBACK EXECUTED")

            raise

        finally:

            conn.close()

    # ----------------------------------------
    # Export Audit
    # ----------------------------------------

    def export_audit(self):

        df = pd.DataFrame(self.audit)

        output = Path("output/load_audit.csv")

        output.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        df.to_csv(

            output,

            index=False

        )

        print(

            "\nAudit saved ->",

            output

        )