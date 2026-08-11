import re
from pathlib import Path
import pandas as pd

PATTERN = re.compile(r"(\d+)\s*Years?:?\s*([\d.]+)%")


def parse_analysis_text(value):
    if pd.isna(value):
        return None
    text = str(value).strip()
    match = PATTERN.search(text)
    if not match:
        return None
    period = int(match.group(1))
    value_pct = float(match.group(2))
    return period, value_pct


def parse_analysis_file(input_path=None, output_dir=None):
    input_path = Path(input_path or "data/raw/analysis/analysis.xlsx")
    output_dir = Path(output_dir or "output")
    output_dir.mkdir(parents=True, exist_ok=True)

    sheet = pd.read_excel(input_path, sheet_name="Analysis")
    first_row = sheet.iloc[0]
    if len(sheet.columns) > 0 and isinstance(first_row.iloc[0], str) and "company_id" in str(first_row.iloc[0]).lower():
        sheet = pd.read_excel(input_path, sheet_name="Analysis", header=1)
    else:
        sheet = pd.read_excel(input_path, sheet_name="Analysis", header=1)

    parsed_rows = []
    failure_rows = []

    column_map = {
        "compounded_sales_growth": "sales_growth",
        "compounded_profit_growth": "profit_growth",
        "stock_price_cagr": "stock_cagr",
        "roe": "roe",
    }

    for _, row in sheet.iterrows():
        company_id = row.get("company_id") if "company_id" in row.index else row.iloc[1] if len(row) > 1 else None
        for metric_name, metric_key in column_map.items():
            if metric_name not in sheet.columns:
                continue
            raw = row.get(metric_name)
            parsed = parse_analysis_text(raw)
            if parsed is None:
                failure_rows.append({
                    "company_id": company_id,
                    "metric_type": metric_name,
                    "raw_value": raw,
                })
                continue
            period_years, value_pct = parsed
            parsed_rows.append({
                "company_id": company_id,
                "metric_type": metric_name,
                "period_years": period_years,
                "value_pct": value_pct,
            })

    parsed_df = pd.DataFrame(parsed_rows)
    failures_df = pd.DataFrame(failure_rows)
    parsed_df.to_csv(output_dir / "analysis_parsed.csv", index=False)
    failures_df.to_csv(output_dir / "parse_failures.csv", index=False)
    return parsed_df, failures_df
