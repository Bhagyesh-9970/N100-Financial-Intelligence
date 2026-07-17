"""
ETL Audit Manager
Sprint 1 Day 5
"""

from pathlib import Path
from datetime import datetime
import pandas as pd


class AuditManager:

    def __init__(self):

        self.records = []

    def start_table(self, table):

        return datetime.now()

    def finish_table(self,
                     table,
                     rows,
                     status,
                     start_time,
                     error=""):

        end_time = datetime.now()

        duration = round(
            (end_time - start_time).total_seconds(),
            3
        )

        self.records.append({

            "table": table,

            "rows_loaded": rows,

            "status": status,

            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),

            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),

            "duration_seconds": duration,

            "error": error

        })

    def export(self):

        output = Path("output/load_audit.csv")

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        pd.DataFrame(self.records).to_csv(
            output,
            index=False
        )

        print("\nLoad audit exported ->", output)