import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))
from src.etl.normaliser import DataNormalizer

print(DataNormalizer.normalize_year("FY24"))
print(DataNormalizer.normalize_year("2024-25"))

print(DataNormalizer.normalize_ticker(" tcs.ns "))

print(DataNormalizer.normalize_company_name("  Tata Consultancy Services   "))

print(DataNormalizer.normalize_column_name("Net Profit %"))

print(DataNormalizer.normalize_numeric("₹1,23,456"))

print(DataNormalizer.normalize_missing("NA"))