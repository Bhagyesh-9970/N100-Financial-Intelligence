from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.database.db_manager import DatabaseManager

db = DatabaseManager()

db.connect()

db.create_database()

db.list_tables()

db.close()