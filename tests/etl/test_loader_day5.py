from src.etl.loader import ExcelLoader


loader = ExcelLoader()

datasets = loader.load_all()

loader.summary(datasets)