from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
except ModuleNotFoundError:  # pragma: no cover - fallback for environments without scikit-learn
    KMeans = None
    StandardScaler = None

from src.dashboard.utils.db import get_companies

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


def build_company_clusters(n_clusters: int = 5, output_dir: Path | None = None) -> dict[str, Any]:
    """Cluster companies using a small financial feature set and export the artifacts."""
    df = get_companies().copy()
    if df.empty:
        return {"clusters": [], "summary": [], "artifacts": []}

    feature_cols = [
        "return_on_equity_pct",
        "revenue_cagr_5yr",
        "net_profit_margin_pct",
        "debt_to_equity",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf",
    ]
    features = df[feature_cols].apply(pd.to_numeric, errors="coerce")
    features = features.dropna(how="all")
    if features.empty:
        return {"clusters": [], "summary": [], "artifacts": []}

    if StandardScaler is None or KMeans is None:
        clustered = df.loc[features.index].copy()
        clustered["cluster"] = 0
        summary = (
            clustered.groupby("cluster")
            .agg(
                companies=("company_name", "count"),
                avg_roe=("return_on_equity_pct", "mean"),
                avg_cagr=("revenue_cagr_5yr", "mean"),
                avg_margin=("net_profit_margin_pct", "mean"),
            )
            .reset_index()
        )
        out_dir = output_dir or OUTPUT_DIR
        out_dir.mkdir(exist_ok=True)
        cluster_path = out_dir / "company_clusters.csv"
        clustered.to_csv(cluster_path, index=False)
        stats_path = out_dir / "cluster_profile_summary.csv"
        summary.to_csv(stats_path, index=False)
        return {"clusters": clustered.to_dict(orient="records"), "summary": summary.to_dict(orient="records"), "artifacts": [str(cluster_path), str(stats_path)]}

    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)

    model = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    labels = model.fit_predict(scaled)

    clustered = df.loc[features.index].copy()
    clustered["cluster"] = labels

    summary = (
        clustered.groupby("cluster")
        .agg(
            companies=("company_name", "count"),
            avg_roe=("return_on_equity_pct", "mean"),
            avg_cagr=("revenue_cagr_5yr", "mean"),
            avg_margin=("net_profit_margin_pct", "mean"),
        )
        .reset_index()
    )

    out_dir = output_dir or OUTPUT_DIR
    out_dir.mkdir(exist_ok=True)
    cluster_path = out_dir / "company_clusters.csv"
    clustered.to_csv(cluster_path, index=False)

    plt.figure(figsize=(8, 4))
    plt.plot(range(1, 6), [0.0] * 4, color="lightgray")
    plt.close()

    stats_path = out_dir / "cluster_profile_summary.csv"
    summary.to_csv(stats_path, index=False)

    return {
        "clusters": clustered.to_dict(orient="records"),
        "summary": summary.to_dict(orient="records"),
        "artifacts": [str(cluster_path), str(stats_path)],
    }
