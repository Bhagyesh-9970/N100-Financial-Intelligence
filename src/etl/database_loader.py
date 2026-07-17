from pathlib import Path
import sqlite3
import logging

from src.etl.audit import AuditManager


class DatabaseLoader:

    def __init__(self):

        self.db = Path("db/nifty100.db")

        self.audit = AuditManager()

        Path("logs").mkdir(exist_ok=True)

        logging.basicConfig(

            filename="logs/etl.log",

            level=logging.INFO,

            format="%(asctime)s %(levelname)s %(message)s"

        )

    def connect(self):

        return sqlite3.connect(self.db)

    def load_all(self, datasets):

        conn = self.connect()

        try:

            conn.execute("BEGIN")

            print("\n" + "="*60)
            print("DATABASE LOAD")
            print("="*60)

            for table, df in datasets.items():

                start = self.audit.start_table(table)

                try:

                    conn.execute(f"DELETE FROM {table}")

                except:

                    pass

                df.to_sql(

                    table,

                    conn,

                    if_exists="append",

                    index=False,

                    chunksize=1000,

                    method="multi"

                )

                rows = len(df)

                logging.info(
                    f"{table} : {rows} rows loaded"
                )

                self.audit.finish_table(

                    table,

                    rows,

                    "SUCCESS",

                    start

                )

                print(
                    f"[OK] {table:<22}{rows:>8} rows"
                )

            conn.commit()

            print("\nDatabase Commit Successful")

        except Exception as e:

            conn.rollback()

            logging.exception(e)

            print("\nROLLBACK EXECUTED")

            raise

        finally:

            conn.close()

            self.audit.export()