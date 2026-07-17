from src.etl.loader import ExcelLoader
from src.etl.data_cleaner import DataCleaner

loader = ExcelLoader()

datasets = loader.load_all()

cleaner = DataCleaner()

cleaned = cleaner.clean_all(datasets)

print("\nCleaning completed successfully.")