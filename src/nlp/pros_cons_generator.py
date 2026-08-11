from __future__ import annotations

from pathlib import Path
import pandas as pd


PRO_RULES = [
    ("ROE > 20% sustained for 3+ years", lambda row: (row.get("roe_series") or [0])[-1] > 20 and len([x for x in (row.get("roe_series") or []) if x > 20]) >= 3, "Consistently high return on equity above 20% demonstrates exceptional capital efficiency", 90),
    ("FCF positive for 5+ consecutive years", lambda row: len([x for x in (row.get("fcf_series") or []) if x > 0]) >= 5, "Strong free cash flow generation over 5 years signals healthy business fundamentals", 88),
    ("D/E = 0 in latest year", lambda row: (row.get("debt_to_equity_series") or [1])[-1] == 0, "Debt-free balance sheet provides financial flexibility and eliminates interest burden", 86),
    ("Revenue CAGR > 15% over 5 years", lambda row: (row.get("revenue_cagr_5yr") or 0) > 15, "Revenue growing at above 15% CAGR over 5 years reflects strong business momentum", 84),
    ("OPM > 25% in latest year", lambda row: (row.get("opm_series") or [0])[-1] > 25, "Operating profit margin above 25% indicates strong pricing power and cost discipline", 82),
    ("PAT CAGR > 20% over 5 years", lambda row: (row.get("pat_cagr_5yr") or 0) > 20, "Net profit compounding at above 20% over 5 years creates significant shareholder value", 80),
    ("ICR > 10 or Debt Free", lambda row: ((row.get("interest_coverage_series") or [0])[-1] > 10) or ((row.get("debt_to_equity_series") or [1])[-1] == 0), "Very high interest coverage ratio reflects negligible financial stress from debt servicing", 78),
    ("Dividend Yield > 2% with FCF positive", lambda row: ((row.get("dividend_yield_series") or [0])[-1] > 2) and ((row.get("fcf_series") or [0])[-1] > 0), "Consistent dividend yield above 2% backed by positive free cash flow", 76),
    ("EPS CAGR > 15% over 5 years", lambda row: (row.get("eps_cagr_5yr") or 0) > 15, "Earnings per share growing above 15% CAGR indicates strong earnings quality and compounding", 74),
    ("ROE improving for 3 consecutive years", lambda row: len([1 for i in range(1, len(row.get("roe_series") or [])) if (row.get("roe_series") or [0])[i] > (row.get("roe_series") or [0])[i-1]]) >= 3, "Return on equity improving for 3 consecutive years shows strengthening business quality", 72),
    ("Revenue CAGR > PAT CAGR", lambda row: (row.get("revenue_cagr_5yr") or 0) > (row.get("pat_cagr_5yr") or 0), "Revenue growing slower than profits shows improving operating leverage and scale benefits", 70),
    ("Assets growing with declining debt", lambda row: len([1 for i in range(1, len(row.get("asset_series") or [])) if (row.get("asset_series") or [0])[i] > (row.get("asset_series") or [0])[i-1]]) >= 2 and len([1 for i in range(1, len(row.get("debt_series") or [])) if (row.get("debt_series") or [0])[i] < (row.get("debt_series") or [0])[i-1]]) >= 2, "Growing asset base funded by internal accruals reflects self-sustaining growth", 68),
]

CON_RULES = [
    ("D/E > 2.0 for non-financial", lambda row: ((row.get("debt_to_equity_series") or [0])[-1] > 2.0) and (row.get("sector") != "Financials"), "Debt-to-equity ratio of X is elevated for a non-financial company and warrants monitoring", 84),
    ("FCF negative for 3 consecutive years", lambda row: sum(1 for x in (row.get("fcf_series") or []) if x < 0) >= 3, "Free cash flow negative for 3 consecutive years raises concern about cash generation quality", 82),
    ("OPM declining for 3 consecutive years", lambda row: len([1 for i in range(1, len(row.get("opm_series") or [])) if (row.get("opm_series") or [0])[i] < (row.get("opm_series") or [0])[i-1]]) >= 3, "Operating margins declining for 3 consecutive years suggest pricing or cost pressure", 80),
    ("Net profit negative in latest year", lambda row: (row.get("net_profit_series") or [0])[-1] < 0, "Company reported a net loss in the most recent financial year", 88),
    ("Revenue declining for 2+ years", lambda row: sum(1 for i in range(1, len(row.get("revenue_series") or [])) if (row.get("revenue_series") or [0])[i] < (row.get("revenue_series") or [0])[i-1]) >= 2, "Revenue contraction over 2 consecutive years indicates demand weakness or market share loss", 78),
    ("ICR < 1.5", lambda row: ((row.get("interest_coverage_series") or [0])[-1] < 1.5), "Interest coverage ratio below 1.5x indicates the company is at risk of not meeting its debt obligations", 82),
    ("Dividend payout > 100%", lambda row: (row.get("dividend_payout_series") or [0])[-1] > 100, "Dividend payout ratio above 100% means the company is paying dividends from reserves, which is unsustainable", 76),
    ("D/E rising for 3 consecutive years", lambda row: len([1 for i in range(1, len(row.get("debt_to_equity_series") or [])) if (row.get("debt_to_equity_series") or [0])[i] > (row.get("debt_to_equity_series") or [0])[i-1]]) >= 3, "Rising debt-to-equity ratio over 3 years suggests increasing financial leverage risk", 74),
    ("EPS declining for 3 consecutive years", lambda row: len([1 for i in range(1, len(row.get("eps_series") or [])) if (row.get("eps_series") or [0])[i] < (row.get("eps_series") or [0])[i-1]]) >= 3, "Earnings per share declining for 3 consecutive years reflects deteriorating profitability", 72),
    ("ROCE < 10%", lambda row: (row.get("roce_series") or [0])[-1] < 10, "Return on capital employed below 10% suggests the business is not generating sufficient returns on invested capital", 70),
    ("Net Debt > 3x EBITDA", lambda row: (row.get("net_debt_to_ebitda") or 0) > 3, "Net debt exceeding 3 times EBITDA is a high leverage ratio and limits financial flexibility", 68),
    ("Revenue CAGR < 5% over 5 years", lambda row: (row.get("revenue_cagr_5yr") or 0) < 5, "Revenue growing at below 5% over 5 years lags inflation and suggests limited business momentum", 66),
]


def _cagr(values, years):
    if not values or len(values) < years + 1:
        return None
    try:
        start = values[-(years + 1)]
        end = values[-1]
    except Exception:
        return None
    if start in (0, None) or end in (0, None):
        return None
    try:
        result = ((end / start) ** (1 / years) - 1) * 100
    except Exception:
        return None
    if isinstance(result, complex):
        return None
    return round(float(result), 2)


def _series_for(df, company_id, column):
    values = df.loc[df["company_id"] == company_id, column].dropna().tolist()
    return values


def _extract_numeric_series(values):
    if values is None:
        return []
    if isinstance(values, pd.DataFrame):
        return []
    if isinstance(values, (list, tuple, set)):
        flattened = []
        for item in values:
            if isinstance(item, (list, tuple, set)):
                flattened.extend(_extract_numeric_series(item))
            elif isinstance(item, pd.Series):
                flattened.extend(_extract_numeric_series(item.tolist()))
            else:
                flattened.append(float(item))
        return flattened
    if isinstance(values, pd.Series):
        flattened = []
        for v in values.dropna().tolist():
            if isinstance(v, (list, tuple, set)):
                flattened.extend(_extract_numeric_series(v))
            elif isinstance(v, pd.Series):
                flattened.extend(_extract_numeric_series(v.tolist()))
            else:
                flattened.append(float(v))
        return flattened
    if isinstance(values, pd.DataFrame):
        return []
    return [float(values)]


def generate_pros_cons(company_df, company_id=None, company_name=None, sector=None, output_dir=None):
    output_dir = Path(output_dir or "output")
    output_dir.mkdir(parents=True, exist_ok=True)

    if company_df is None or company_df.empty:
        return []

    if company_id is None:
        company_id = company_df["company_id"].iloc[0]

    if company_name is None:
        company_name = company_df.get("company_name", pd.Series([company_id])).iloc[0] if "company_name" in company_df.columns else company_id

    if sector is None:
        sector = company_df.get("sector", pd.Series([None])).iloc[0] if "sector" in company_df.columns else None

    revenue_series = _extract_numeric_series(company_df.get("sales", pd.Series([0])) if "sales" in company_df.columns else 0)
    net_profit_series = _extract_numeric_series(company_df.get("net_profit", pd.Series([0])) if "net_profit" in company_df.columns else 0)
    opm_series = _extract_numeric_series(company_df.get("opm_percentage", pd.Series([0])) if "opm_percentage" in company_df.columns else 0)
    roe_series = _extract_numeric_series(company_df.get("roe_pct", pd.Series([0])) if "roe_pct" in company_df.columns else 0)
    debt_to_equity_series = _extract_numeric_series(company_df.get("debt_to_equity", pd.Series([0])) if "debt_to_equity" in company_df.columns else 0)
    interest_coverage_series = _extract_numeric_series(company_df.get("interest_coverage", pd.Series([0])) if "interest_coverage" in company_df.columns else 0)
    fcf_series = _extract_numeric_series(company_df.get("free_cash_flow_cr", pd.Series([0])) if "free_cash_flow_cr" in company_df.columns else 0)
    dividend_payout_series = _extract_numeric_series(company_df.get("dividend_payout", pd.Series([0])) if "dividend_payout" in company_df.columns else 0)
    dividend_yield_series = _extract_numeric_series(company_df.get("dividend_yield_pct", pd.Series([0])) if "dividend_yield_pct" in company_df.columns else 0)
    eps_series = _extract_numeric_series(company_df.get("eps", pd.Series([0])) if "eps" in company_df.columns else 0)
    roce_series = _extract_numeric_series(company_df.get("roce_pct", pd.Series([0])) if "roce_pct" in company_df.columns else 0)
    asset_series = _extract_numeric_series(company_df.get("total_assets", pd.Series([0])) if "total_assets" in company_df.columns else 0)
    debt_series = _extract_numeric_series(company_df.get("borrowings", pd.Series([0])) if "borrowings" in company_df.columns else 0)

    row = {
        "company_id": company_id,
        "company_name": company_name,
        "sector": sector,
        "sales": revenue_series,
        "net_profit_series": net_profit_series,
        "opm_series": opm_series,
        "roe_series": roe_series,
        "debt_to_equity_series": debt_to_equity_series,
        "interest_coverage_series": interest_coverage_series,
        "fcf_series": fcf_series,
        "dividend_payout_series": dividend_payout_series,
        "dividend_yield_series": dividend_yield_series,
        "eps_series": eps_series,
        "roce_series": roce_series,
        "asset_series": asset_series,
        "debt_series": debt_series,
        "revenue_series": revenue_series,
        "revenue_cagr_5yr": _cagr(revenue_series, 5),
        "pat_cagr_5yr": _cagr(net_profit_series, 5),
        "eps_cagr_5yr": _cagr(eps_series, 5),
        "net_debt_to_ebitda": None,
    }

    rows = []
    for rule_id, predicate, text, confidence in PRO_RULES:
        if predicate(row):
            rows.append({"company_id": company_id, "type": "pro", "rule_id": rule_id, "text": text, "confidence_pct": confidence})
    for rule_id, predicate, text, confidence in CON_RULES:
        if predicate(row):
            rows.append({"company_id": company_id, "type": "con", "rule_id": rule_id, "text": text, "confidence_pct": confidence})

    rows = [r for r in rows if r["confidence_pct"] > 60]
    if not rows:
        rows.append({"company_id": company_id, "type": "pro", "rule_id": "default", "text": "Operational performance remains stable across the latest period", "confidence_pct": 60})
        rows.append({"company_id": company_id, "type": "con", "rule_id": "default", "text": "Additional monitoring may be warranted due to limited signal clarity", "confidence_pct": 60})

    output_df = pd.DataFrame(rows)
    output_df.to_csv(output_dir / "pros_cons_generated.csv", index=False)
    return rows


def generate_all_pros_cons(companies_df, financial_df, output_dir=None):
    output_dir = Path(output_dir or "output")
    output_dir.mkdir(parents=True, exist_ok=True)
    all_rows = []
    company_ids = []
    for company_id in companies_df["company_id"].tolist():
        if pd.notna(company_id):
            company_ids.append(str(company_id))
    for company_id in sorted(set(company_ids)):
        company_rows = financial_df[financial_df["company_id"].astype(str) == company_id]
        if company_rows.empty:
            continue
        company_rows = company_rows.sort_values("year")
        rows = generate_pros_cons(company_rows, company_id=company_id, company_name=company_rows.iloc[0].get("company_name", company_id), sector=company_rows.iloc[0].get("sector"), output_dir=output_dir)
        all_rows.extend(rows)
    out = pd.DataFrame(all_rows)
    out.to_csv(output_dir / "pros_cons_generated.csv", index=False)
    return out
