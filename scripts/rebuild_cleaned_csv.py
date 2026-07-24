"""
N100 Financial Intelligence Platform

Rebuild cleaned CSV files from raw Excel files.

Purpose:
- Read Excel files using header row 0
- Normalize column names
- Remove empty rows and columns
- Save corrected CSV files
- Prevent corrupted headers such as:
  ['1', 'abb', 'dec_2012', ...]
"""

from pathlib import Path
import re
import pandas as pd


# =============================================================
# PATHS
# =============================================================

RAW_DIR = Path("data/raw")

CLEANED_DIR = Path(
    "data/interim/cleaned"
)


# =============================================================
# COLUMN NORMALIZATION
# =============================================================

def normalize_column_name(column):

    column = str(column).strip().lower()

    # Percentage symbols

    column = column.replace(
        "%",
        "pct"
    )

    # Ampersand

    column = column.replace(
        "&",
        "and"
    )

    # Spaces

    column = re.sub(
        r"\s+",
        "_",
        column
    )

    # Special characters

    column = re.sub(
        r"[^a-zA-Z0-9_]",
        "",
        column
    )

    # Duplicate underscores

    column = re.sub(
        r"_+",
        "_",
        column
    )

    return column.strip("_")


def normalize_columns(df):

    df.columns = [

        normalize_column_name(

            column

        )

        for column in df.columns

    ]

    return df


# =============================================================
# LOAD ONE EXCEL FILE
# =============================================================

def load_excel(file_path):

    print(

        f"Loading: {file_path}"

    )

    # IMPORTANT:
    # Header is row 0 in your Excel files

    df = pd.read_excel(

        file_path,

        header=0

    )

    # Normalize columns

    df = normalize_columns(

        df

    )

    # Remove empty rows

    df = df.dropna(

        how="all"

    )

    # Remove empty columns

    df = df.dropna(

        axis=1,

        how="all"

    )

    # Remove duplicate columns

    df = df.loc[

        :,

        ~df.columns.duplicated()

    ]

    # Reset index

    df = df.reset_index(

        drop=True

    )

    return df


# =============================================================
# MAIN
# =============================================================

def main():

    print("\n")

    print("=" * 60)

    print(

        "REBUILDING CLEANED CSV FILES"

    )

    print("=" * 60)

    # Create output directory

    CLEANED_DIR.mkdir(

        parents=True,

        exist_ok=True

    )

    # Discover Excel files

    excel_files = sorted(

        RAW_DIR.rglob(

            "*.xlsx"

        )

    )

    if not excel_files:

        print(

            "ERROR: No Excel files found."

        )

        return

    print(

        f"Found {len(excel_files)} Excel files"

    )

    print()

    # Process each file

    for file_path in excel_files:

        # Load

        df = load_excel(

            file_path

        )

        # Dataset name

        dataset_name = (

            file_path.stem.lower()

        )

        # Output path

        output_path = (

            CLEANED_DIR

            /

            f"{dataset_name}.csv"

        )

        # Save

        df.to_csv(

            output_path,

            index=False

        )

        print(

            f"[OK] "

            f"{dataset_name:<25}"

            f"{len(df):>8} rows | "

            f"{len(df.columns):>4} columns"

        )

        print(

            f"     Saved -> {output_path}"

        )

        print()

    print("=" * 60)

    print(

        "CLEANING COMPLETED SUCCESSFULLY"

    )

    print("=" * 60)


# =============================================================
# EXECUTION
# =============================================================

if __name__ == "__main__":

    main()