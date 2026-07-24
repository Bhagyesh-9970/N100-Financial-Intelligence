"""
N100 Financial Intelligence Platform
Sprint 3 - Day 15

Screener Filter Engine

Responsibilities:
- Load screener_config.yaml
- Apply custom threshold filters
- Support 15 financial metrics
- Handle Financials-sector D/E exemption
- Handle Debt-Free ICR as infinity
- Calculate composite quality score
- Return sorted screener results
"""

from pathlib import Path

import yaml
import pandas as pd
import numpy as np


class ScreenerEngine:

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(
        self,
        config_path="config/screener_config.yaml"
    ):

        self.config_path = Path(config_path)

        if not self.config_path.exists():

            raise FileNotFoundError(
                f"Screener configuration not found: "
                f"{self.config_path}"
            )

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.config = yaml.safe_load(file)

        self.presets = self.config.get(
            "presets",
            {}
        )

    # =========================================================
    # COLUMN ALIASES
    # =========================================================

    COLUMN_ALIASES = {

        "roe": "return_on_equity_pct",

        "roce": "return_on_capital_employed_pct",

        "npm": "net_profit_margin_pct",

        "de": "debt_to_equity",

        "fcf": "free_cash_flow_cr",

        "revenue_cagr": "revenue_cagr_5yr_pct",

        "pat_cagr": "pat_cagr_5yr_pct",

        "eps_cagr": "eps_cagr_5yr_pct",

        "opm": "operating_profit_margin_pct",

        "pe": "pe_ratio",

        "pb": "pb_ratio",

        "dividend_yield": "dividend_yield_pct",

        "icr": "interest_coverage_ratio",

        "market_cap": "market_cap_cr",

        "net_profit": "net_profit",

        "asset_turnover": "asset_turnover",

        "sales": "sales"

    }

    # =========================================================
    # PREPARE DATAFRAME
    # =========================================================

    @staticmethod
    def prepare_dataframe(df):

        result = df.copy()

        # -----------------------------------------------------
        # Normalize column names
        # -----------------------------------------------------

        result.columns = (

            result.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)

        )

        # -----------------------------------------------------
        # Convert numeric columns
        # -----------------------------------------------------

        for column in result.columns:

            if column not in [

                "company_id",
                "company_name",
                "sector",
                "broad_sector",
                "year"

            ]:

                result[column] = pd.to_numeric(
                    result[column],
                    errors="coerce"
                )

        # -----------------------------------------------------
        # Debt-Free companies
        # -----------------------------------------------------

        if "interest_coverage_ratio" in result.columns:

            result["interest_coverage_ratio"] = (

                result["interest_coverage_ratio"]
                .replace(
                    [
                        "Debt Free",
                        "Debt-Free",
                        "debt free",
                        "debt-free"
                    ],
                    np.inf
                )

            )

        return result

    # =========================================================
    # APPLY SINGLE FILTER
    # =========================================================

    def apply_filter(
        self,
        df,
        metric,
        condition
    ):

        if metric not in df.columns:

            print(
                f"[WARNING] Metric not available: "
                f"{metric}"
            )

            return df

        result = df.copy()

        # -----------------------------------------------------
        # Financial sector D/E exemption
        # -----------------------------------------------------

        if metric == "debt_to_equity":

            sector_column = None

            if "broad_sector" in result.columns:

                sector_column = "broad_sector"

            elif "sector" in result.columns:

                sector_column = "sector"

            if sector_column:

                financial_mask = (

                    result[sector_column]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        "financial"
                    )

                )

            else:

                financial_mask = pd.Series(
                    False,
                    index=result.index
                )

        else:

            financial_mask = pd.Series(
                False,
                index=result.index
            )

        # -----------------------------------------------------
        # Minimum filter
        # -----------------------------------------------------

        if "min" in condition:

            threshold = condition["min"]

            mask = (

                result[metric] >= threshold

            )

        # -----------------------------------------------------
        # Maximum filter
        # -----------------------------------------------------

        elif "max" in condition:

            threshold = condition["max"]

            mask = (

                result[metric] <= threshold

            )

        # -----------------------------------------------------
        # Exact filter
        # -----------------------------------------------------

        elif "equal" in condition:

            threshold = condition["equal"]

            mask = (

                result[metric] == threshold

            )

        else:

            print(
                f"[WARNING] Invalid filter condition "
                f"for {metric}"
            )

            return result

        # -----------------------------------------------------
        # Apply Financials exemption
        # -----------------------------------------------------

        if metric == "debt_to_equity":

            mask = (

                mask
                | financial_mask

            )

        return result.loc[mask].copy()

    # =========================================================
    # APPLY FILTERS
    # =========================================================

    def apply_filters(
        self,
        df,
        filters
    ):

        result = self.prepare_dataframe(
            df
        )

        for metric, condition in filters.items():

            actual_column = (

                self.COLUMN_ALIASES
                .get(
                    metric,
                    metric
                )

            )

            result = self.apply_filter(

                result,
                actual_column,
                condition

            )

        return result

    # =========================================================
    # COMPOSITE QUALITY SCORE
    # =========================================================

    @staticmethod
    def winsorized_score(
        series,
        higher_is_better=True
    ):

        series = pd.to_numeric(
            series,
            errors="coerce"
        )

        if series.dropna().empty:

            return pd.Series(
                50,
                index=series.index
            )

        p10 = series.quantile(
            0.10
        )

        p90 = series.quantile(
            0.90
        )

        if p10 == p90:

            return pd.Series(
                50,
                index=series.index
            )

        clipped = series.clip(
            lower=p10,
            upper=p90
        )

        score = (

            (clipped - p10)
            /
            (p90 - p10)
            * 100

        )

        if not higher_is_better:

            score = 100 - score

        return score.fillna(
            50
        )

    # =========================================================
    # COMPOSITE SCORE
    # =========================================================

    def calculate_composite_score(
        self,
        df
    ):

        result = df.copy()

        # -----------------------------------------------------
        # Profitability - 35%
        # -----------------------------------------------------

        profitability = (

            self.winsorized_score(
                result.get(
                    "return_on_equity_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.15

            +

            self.winsorized_score(
                result.get(
                    "return_on_capital_employed_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.10

            +

            self.winsorized_score(
                result.get(
                    "net_profit_margin_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.10

        )

        # -----------------------------------------------------
        # Cash Quality - 30%
        # -----------------------------------------------------

        cash_quality = (

            self.winsorized_score(
                result.get(
                    "free_cash_flow_cagr_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.15

            +

            self.winsorized_score(
                result.get(
                    "cfo_pat_ratio",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.10

            +

            (

                pd.to_numeric(
                    result.get(
                        "free_cash_flow_cr",
                        pd.Series(
                            index=result.index,
                            dtype=float
                        )
                    ),
                    errors="coerce"
                ) > 0

            ).astype(int) * 100 * 0.05

        )

        # -----------------------------------------------------
        # Growth - 20%
        # -----------------------------------------------------

        growth = (

            self.winsorized_score(
                result.get(
                    "revenue_cagr_5yr_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.10

            +

            self.winsorized_score(
                result.get(
                    "pat_cagr_5yr_pct",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.10

        )

        # -----------------------------------------------------
        # Leverage - 15%
        # -----------------------------------------------------

        leverage = (

            self.winsorized_score(
                result.get(
                    "debt_to_equity",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                ),
                higher_is_better=False
            ) * 0.10

            +

            self.winsorized_score(
                result.get(
                    "interest_coverage_ratio",
                    pd.Series(
                        index=result.index,
                        dtype=float
                    )
                )
            ) * 0.05

        )

        result[
            "composite_quality_score"
        ] = (

            profitability
            +
            cash_quality
            +
            growth
            +
            leverage

        ).clip(
            lower=0,
            upper=100
        )

        return result

    # =========================================================
    # RUN CUSTOM SCREENER
    # =========================================================

    def screen(
        self,
        df,
        filters=None,
        preset=None
    ):

        if preset:

            if preset not in self.presets:

                raise ValueError(

                    f"Unknown preset: {preset}"

                )

            filters = self.presets[
                preset
            ].get(
                "filters",
                {}
            )

        if not filters:

            raise ValueError(
                "Either filters or preset "
                "must be provided"
            )

        result = self.apply_filters(
            df,
            filters
        )

        result = self.calculate_composite_score(
            result
        )

        result = result.sort_values(

            "composite_quality_score",

            ascending=False

        ).reset_index(
            drop=True
        )

        return result

    # =========================================================
    # RUN ALL PRESETS
    # =========================================================

    def run_all_presets(
        self,
        df
    ):

        results = {}

        for preset_name in self.presets:

            print(
                f"\nRunning preset: "
                f"{preset_name}"
            )

            results[preset_name] = (

                self.screen(
                    df,
                    preset=preset_name
                )

            )

            print(
                f"Results: "
                f"{len(results[preset_name])}"
            )

        return results