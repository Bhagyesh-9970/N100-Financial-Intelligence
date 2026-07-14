"""
config.py
----------

Central configuration for the project.

All project paths are managed here.

Never hardcode paths anywhere else.

Project:
N100 Financial Intelligence Platform
"""

from pathlib import Path

# ===========================================================
# Project Root
# ===========================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

# ===========================================================
# Data
# ===========================================================

DATA_DIR = ROOT_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

INTERIM_DATA_DIR = DATA_DIR / "interim"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

EXTERNAL_DATA_DIR = DATA_DIR / "external"

# ===========================================================
# Database
# ===========================================================

DB_DIR = ROOT_DIR / "db"

DATABASE_PATH = DB_DIR / "nifty100.db"

SCHEMA_FILE = DB_DIR / "schema.sql"

# ===========================================================
# Output
# ===========================================================

OUTPUT_DIR = ROOT_DIR / "output"

AUDIT_DIR = OUTPUT_DIR / "audit"

VALIDATION_DIR = OUTPUT_DIR / "validation"

REPORT_DIR = OUTPUT_DIR / "reports"

EXPORT_DIR = OUTPUT_DIR / "exports"

# ===========================================================
# Logs
# ===========================================================

LOG_DIR = ROOT_DIR / "logs"

# ===========================================================
# Documentation
# ===========================================================

DOCS_DIR = ROOT_DIR / "docs"

# ===========================================================
# Source
# ===========================================================

SRC_DIR = ROOT_DIR / "src"

ETL_DIR = SRC_DIR / "etl"

# ===========================================================
# Tests
# ===========================================================

TEST_DIR = ROOT_DIR / "tests"

# ===========================================================
# Notebooks
# ===========================================================

NOTEBOOK_DIR = ROOT_DIR / "notebooks"

# ===========================================================
# Environment
# ===========================================================

ENV_FILE = ROOT_DIR / ".env"

# ===========================================================
# Helper Function
# ===========================================================

def create_project_directories() -> None:
    """
    Create all required directories if they don't exist.
    """

    directories = [
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        EXTERNAL_DATA_DIR,
        DB_DIR,
        OUTPUT_DIR,
        AUDIT_DIR,
        VALIDATION_DIR,
        REPORT_DIR,
        EXPORT_DIR,
        LOG_DIR,
        DOCS_DIR,
        NOTEBOOK_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)