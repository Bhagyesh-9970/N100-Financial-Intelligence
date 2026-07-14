"""
exceptions.py
--------------

Custom exception classes used by the ETL pipeline.

Project:
N100 Financial Intelligence Platform
"""


class ETLError(Exception):
    """
    Base ETL Exception.
    """

    pass


class FileLoadError(ETLError):
    """
    Raised when a source file cannot be loaded.
    """

    pass


class UnsupportedFileTypeError(ETLError):
    """
    Raised when the file extension is unsupported.
    """

    pass


class MissingColumnError(ETLError):
    """
    Raised when required columns are missing.
    """

    pass


class InvalidYearError(ETLError):
    """
    Raised when financial year is invalid.
    """

    pass


class InvalidTickerError(ETLError):
    """
    Raised when stock ticker format is invalid.
    """

    pass


class DataValidationError(ETLError):
    """
    Raised when data quality checks fail.
    """

    pass


class DatabaseConnectionError(ETLError):
    """
    Raised when SQLite connection fails.
    """

    pass


class DatabaseLoadError(ETLError):
    """
    Raised during database insertion failures.
    """

    pass


class DuplicateRecordError(ETLError):
    """
    Raised when duplicate records are detected.
    """

    pass