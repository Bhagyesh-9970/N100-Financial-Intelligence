from fastapi import APIRouter

from src.analytics.clustering import build_company_clusters
from src.api.data_access import get_portfolio_stats

router = APIRouter(tags=["portfolio"])


@router.get("/portfolio/stats")
@router.get("/api/v1/portfolio/stats")
def portfolio_stats() -> dict:
    stats = get_portfolio_stats()
    return {"stats": stats.where(stats.notna(), None).to_dict(orient="records")}


@router.get("/portfolio/clusters")
@router.get("/api/v1/portfolio/clusters")
def portfolio_clusters() -> dict:
    return build_company_clusters()
