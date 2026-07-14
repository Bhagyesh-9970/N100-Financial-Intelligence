from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from src.etl.loader import ExcelLoader


loader = ExcelLoader("data/raw")

loader.list_files()

datasets = loader.load_all_files()

loader.dataset_summary(datasets)

print(loader.get_row_counts(datasets))

print(loader.get_column_counts(datasets))

loader.export_summary(datasets)

# Preview one dataset
if datasets:
    first_dataset = list(datasets.keys())[0]
    print(loader.preview_dataset(datasets, first_dataset))