from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))

from src.database.db_manager import DatabaseManager
from src.database.data_loader import DatabaseLoader
from src.etl.loader import ExcelLoader

db = DatabaseManager()

db.connect()

loader = ExcelLoader("data/raw")

datasets = loader.load_all_files()

database = DatabaseLoader()

for table, dataframe in datasets.items():

    try:

        database.load_table(dataframe, table)

    except Exception as e:

        print(table, e)

database.commit()

database.close()

db.close()

print("\nDatabase Load Completed")