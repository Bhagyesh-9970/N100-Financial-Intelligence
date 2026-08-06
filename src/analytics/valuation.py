from pathlib import Path

import pandas as pd

from src.dashboard.utils.db import get_companies


def build_valuation_summary():
    df = get_companies().copy()

    if df.empty:
        return pd.DataFrame()

    if "fcf" not in df.columns:
        df["fcf"] = pd.NA
    if "market_cap" not in df.columns:
        df["market_cap"] = pd.NA
    if "pe_ratio" not in df.columns:
        df["pe_ratio"] = pd.NA
    if "pb_ratio" not in df.columns:
        df["pb_ratio"] = pd.NA
    if "ev_ebitda" not in df.columns:
        df["ev_ebitda"] = pd.NA

    df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce")
    df["fcf"] = pd.to_numeric(df["fcf"], errors="coerce")
    df["pe_ratio"] = pd.to_numeric(df["pe_ratio"], errors="coerce")
    df["pb_ratio"] = pd.to_numeric(df["pb_ratio"], errors="coerce")
    df["ev_ebitda"] = pd.to_numeric(df["ev_ebitda"], errors="coerce")

    df["fcf_yield_pct"] = (df["fcf"] / df["market_cap"] * 100).replace([float("inf"), -float("inf")], pd.NA)

    sector_pe = df.groupby("sector")["pe_ratio"].median().dropna()
    sector_pe = sector_pe.reindex(df["sector"].fillna("Unknown").astype(str))

    df["sector_median_pe"] = sector_pe.values
    df["pe_vs_sector_median_pct"] = ((df["pe_ratio"] / df["sector_median_pe"]) * 100).replace([float("inf"), -float("inf")], pd.NA)

    df["flag"] = "Fair"
    df.loc[df["pe_ratio"].fillna(0) > df["sector_median_pe"].fillna(999) * 1.5, "flag"] = "Caution"
    df.loc[df["pe_ratio"].fillna(0) < df["sector_median_pe"].fillna(0) * 0.7, "flag"] = "Discount"

    summary = df[[
        "company_id",
        "company_name",
        "sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "sector_median_pe",
        "pe_vs_sector_median_pct",
        "flag",
    ]].rename(columns={
        "pe_ratio": "P/E",
        "pb_ratio": "P/B",
        "ev_ebitda": "EV/EBITDA",
        "fcf_yield_pct": "FCF_yield_pct",
        "sector_median_pe": "5yr_median_PE",
        "pe_vs_sector_median_pct": "PE_vs_sector_median_pct",
        "flag": "flag",
    })

    output_dir = Path(__file__).resolve().parents[1] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_path = output_dir / "valuation_summary.xlsx"
    flags_path = output_dir / "valuation_flags.csv"

    try:
        summary.to_excel(summary_path, index=False)
    except Exception:
        summary.to_csv(summary_path.with_suffix(".csv"), index=False)

    flags = summary[summary["flag"].isin(["Caution", "Discount"])]
    flags.to_csv(flags_path, index=False)

    return summary


if __name__ == "__main__":
    build_valuation_summary()