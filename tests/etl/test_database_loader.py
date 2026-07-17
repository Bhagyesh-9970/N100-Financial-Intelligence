from src.etl.loader import ExcelLoader
from src.etl.data_cleaner import DataCleaner
from src.etl.validation_pipeline import ValidationPipeline
from src.etl.database_loader import DatabaseLoader

loader = ExcelLoader()

datasets = loader.load_all()

cleaner = DataCleaner()

cleaned = cleaner.clean_all(datasets)

validator = ValidationPipeline()

validated = validator.validate_all(cleaned)

database = DatabaseLoader()

database.load_all(validated)

database.export_audit()

print("\nDatabase Pipeline Finished Successfully.")