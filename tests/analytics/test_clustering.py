from src.analytics.clustering import build_company_clusters


def test_build_company_clusters_returns_artifacts():
    result = build_company_clusters(n_clusters=3)
    assert isinstance(result, dict)
    assert "clusters" in result
    assert "summary" in result
    assert "artifacts" in result
