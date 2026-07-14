"""
normaliser.py
-----------------------------------------
Data normalization utilities for the
N100 Financial Intelligence Platform.

Author: Bhagyesh Mali
Sprint: 1 Day 2
"""

import re
import pandas as pd


class DataNormalizer:
    """
    Collection of helper methods for cleaning
    and standardizing data before loading into SQLite.
    """

    @staticmethod
    def normalize_year(value):
        """
        Converts different year formats into integer.

        Examples:
        ---------
        FY24        -> 2024
        FY2023      -> 2023
        2024-25     -> 2024
        2024        -> 2024
        """

        if pd.isna(value):
            return None

        value = str(value).strip().upper()

        value = value.replace("FY", "")

        if "-" in value:
            value = value.split("-")[0]

        digits = re.findall(r"\d+", value)

        if not digits:
            return None

        year = digits[0]

        if len(year) == 2:
            year = "20" + year

        return int(year)

    @staticmethod
    def normalize_ticker(value):
        """
        Standardize stock ticker.

        Examples:
        tcs
        TCS
        TCS.NS

        ->
        TCS
        """

        if pd.isna(value):
            return None

        value = str(value).strip().upper()

        value = value.replace(".NS", "")
        value = value.replace(".BO", "")

        value = re.sub(r"[^A-Z0-9]", "", value)

        return value

    @staticmethod
    def normalize_company_name(value):
        """
        Clean company names.
        """

        if pd.isna(value):
            return None

        value = str(value)

        value = value.strip()

        value = re.sub(r"\s+", " ", value)

        return value

    @staticmethod
    def normalize_column_name(column):
        """
        Convert dataframe columns into snake_case.

        Example

        Net Profit %

        becomes

        net_profit
        """

        column = str(column)

        column = column.strip().lower()

        column = column.replace("%", "")

        column = column.replace("&", "and")

        column = re.sub(r"[^\w\s]", "", column)

        column = re.sub(r"\s+", "_", column)

        return column

    @staticmethod
    def normalize_numeric(value):
        """
        Convert numeric strings to float.

        Handles:

        1,23,456
        45%
        ₹123.45
        """

        if pd.isna(value):
            return None

        if isinstance(value, (int, float)):
            return float(value)

        value = str(value)

        value = value.replace(",", "")

        value = value.replace("%", "")

        value = value.replace("₹", "")

        value = value.strip()

        if value == "":
            return None

        try:
            return float(value)

        except ValueError:
            return None

    @staticmethod
    def normalize_missing(value):
        """
        Replace empty values with None.
        """

        if pd.isna(value):
            return None

        value = str(value).strip()

        if value == "":
            return None

        if value.upper() in [
            "NA",
            "N/A",
            "NULL",
            "-",
            "--"
        ]:
            return None

        return value

    @staticmethod
    def normalize_dataframe(df):
        """
        Normalize an entire dataframe.

        - Clean column names
        - Remove duplicate rows
        - Reset index
        """

        df = df.copy()

        df.columns = [
            DataNormalizer.normalize_column_name(col)
            for col in df.columns
        ]

        df.drop_duplicates(inplace=True)

        df.reset_index(drop=True, inplace=True)

        return df