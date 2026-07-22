"""
Sprint 2 - Day 13
Ratio Edge Case Validation
"""

from pathlib import Path
import logging

import pandas as pd


# =====================================================
# PATHS
# =====================================================

ROOT = Path(__file__).resolve().parents[1]

RATIOS_PATH = (
    ROOT
    / "data"
    / "interim"
    / "validated"
    / "financial_ratios.csv"
)

COMPANIES_PATH = (
    ROOT
    / "data"
    / "interim"
    / "validated"
    / "companies.csv"
)

OUTPUT_PATH = ROOT / "output"

LOG_PATH = OUTPUT_PATH / "ratio_edge_cases.log"


OUTPUT_PATH.mkdir(
    parents=True,
    exist_ok=True
)


# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# COLUMN NORMALIZATION
# =====================================================

def normalize_columns(df):

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("%", "pct")
        .str.replace("-", "_")
    )

    return df


# =====================================================
# LOAD DATA
# =====================================================

def load_data():

    ratios = pd.read_csv(RATIOS_PATH)

    companies = pd.read_csv(COMPANIES_PATH)

    ratios = normalize_columns(ratios)

    companies = normalize_columns(companies)

    return ratios, companies


# =====================================================
# IDENTIFY COMPANY KEY
# =====================================================

def prepare_company_key(ratios, companies):

    print("\nRatio columns:")
    print(ratios.columns.tolist())

    print("\nCompany columns:")
    print(companies.columns.tolist())

    # -----------------------------------------
    # Ratio file
    # -----------------------------------------

    if "company_id" not in ratios.columns:

        raise KeyError(
            "financial_ratios.csv does not contain company_id"
        )

    # -----------------------------------------
    # Companies file
    # -----------------------------------------

    possible_company_keys = [
        "company_id",
        "id",
        "ticker",
        "symbol",
        "code"
    ]

    company_key = None

    for key in possible_company_keys:

        if key in companies.columns:

            company_key = key

            break

    if company_key is None:

        raise KeyError(
            "No usable company identifier found in companies.csv"
        )

    # -----------------------------------------
    # Rename company key
    # -----------------------------------------

    if company_key != "company_id":

        companies = companies.rename(
            columns={
                company_key: "company_id"
            }
        )

    # -----------------------------------------
    # Convert keys to strings
    # -----------------------------------------

    ratios["company_id"] = (
        ratios["company_id"]
        .astype(str)
        .str.strip()
    )

    companies["company_id"] = (
        companies["company_id"]
        .astype(str)
        .str.strip()
    )

    return ratios, companies


# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)
    print("RATIO EDGE CASE VALIDATION")
    print("=" * 60)

    ratios, companies = load_data()

    print(
        "Ratio rows:",
        len(ratios)
    )

    print(
        "Company rows:",
        len(companies)
    )

    # -----------------------------------------
    # Prepare company identifier
    # -----------------------------------------

    ratios, companies = prepare_company_key(
        ratios,
        companies
    )

    # -----------------------------------------
    # Select available company columns
    # -----------------------------------------

    company_columns = [
        "company_id"
    ]

    optional_columns = [
        "company_name",
        "broad_sector",
        "roe_percentage",
        "roce_percentage"
    ]

    for column in optional_columns:

        if column in companies.columns:

            company_columns.append(column)

    # -----------------------------------------
    # Remove duplicate company records
    # -----------------------------------------

    companies = (
        companies[company_columns]
        .drop_duplicates(
            subset=["company_id"]
        )
    )

    # -----------------------------------------
    # Merge
    # -----------------------------------------

    df = ratios.merge(
        companies,
        on="company_id",
        how="left",
        suffixes=("", "_source")
    )

    print(
        "\nMerged rows:",
        len(df)
    )

    # =================================================
    # ROCE CHECK
    # =================================================

    print("\nChecking ROCE anomalies...")

    calculated_roce_column = None

    possible_roce_columns = [
        "return_on_capital_employed_pct",
        "roce_pct",
        "roce"
    ]

    for column in possible_roce_columns:

        if column in df.columns:

            calculated_roce_column = column

            break

    if (
        calculated_roce_column
        and "roce_percentage" in df.columns
    ):

        df["roce_difference"] = (
            pd.to_numeric(
                df[calculated_roce_column],
                errors="coerce"
            )
            -
            pd.to_numeric(
                df["roce_percentage"],
                errors="coerce"
            )
        ).abs()

        roce_anomalies = df[
            df["roce_difference"] > 5
        ]

        for _, row in roce_anomalies.iterrows():

            logger.warning(
                "ROCE ANOMALY | "
                f"Company={row.get('company_id')} | "
                f"Year={row.get('year')} | "
                f"Calculated={row.get(calculated_roce_column)} | "
                f"Source={row.get('roce_percentage')} | "
                f"Difference={row.get('roce_difference'):.2f} | "
                "Category=Needs Review"
            )

        print(
            "ROCE anomalies:",
            len(roce_anomalies)
        )

    else:

        print(
            "ROCE source/calculated column unavailable."
        )

    # =================================================
    # ROE CHECK
    # =================================================

    print("\nChecking ROE anomalies...")

    calculated_roe_column = None

    possible_roe_columns = [
        "return_on_equity_pct",
        "roe_pct",
        "roe"
    ]

    for column in possible_roe_columns:

        if column in df.columns:

            calculated_roe_column = column

            break

    if (
        calculated_roe_column
        and "roe_percentage" in df.columns
    ):

        df["roe_difference"] = (
            pd.to_numeric(
                df[calculated_roe_column],
                errors="coerce"
            )
            -
            pd.to_numeric(
                df["roe_percentage"],
                errors="coerce"
            )
        ).abs()

        roe_anomalies = df[
            df["roe_difference"] > 5
        ]

        for _, row in roe_anomalies.iterrows():

            logger.warning(
                "ROE ANOMALY | "
                f"Company={row.get('company_id')} | "
                f"Year={row.get('year')} | "
                f"Calculated={row.get(calculated_roe_column)} | "
                f"Source={row.get('roe_percentage')} | "
                f"Difference={row.get('roe_difference'):.2f} | "
                "Category=Needs Review"
            )

        print(
            "ROE anomalies:",
            len(roe_anomalies)
        )

    else:

        print(
            "ROE source/calculated column unavailable."
        )

    # =================================================
    # FINANCIAL SECTOR CHECK
    # =================================================

    print(
        "\nChecking financial sector carve-out..."
    )

    if "broad_sector" in df.columns:

        financial_companies = df[
            df["broad_sector"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("financials")
        ]

        print(
            "Financial sector rows:",
            len(financial_companies)
        )

        if "high_leverage_flag" in financial_companies.columns:

            incorrect_flags = financial_companies[
                financial_companies[
                    "high_leverage_flag"
                ].fillna(False)
                == True
            ]

            print(
                "Incorrect financial-sector "
                "leverage flags:",
                len(incorrect_flags)
            )

            for _, row in incorrect_flags.iterrows():

                logger.error(
                    "FINANCIAL SECTOR LEVERAGE ERROR | "
                    f"Company={row.get('company_id')} | "
                    f"Year={row.get('year')} | "
                    "Category=Formula Discrepancy"
                )

        else:

            print(
                "high_leverage_flag column not available."
            )

    else:

        print(
            "broad_sector column not available."
        )

    # =================================================
    # COMPLETION
    # =================================================

    print("\n" + "=" * 60)

    print(
        "Edge-case validation completed."
    )

    print(
        f"Log saved to:\n{LOG_PATH}"
    )

    print("=" * 60)


if __name__ == "__main__":

    main()