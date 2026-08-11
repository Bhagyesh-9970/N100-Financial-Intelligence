from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import companies, screener, sectors, peers, valuation, portfolio, documents, health

app = FastAPI(title="N100 Financial Intelligence API", version="0.1.0")
app.include_router(health.router)
app.include_router(companies.router)
app.include_router(screener.router)
app.include_router(sectors.router)
app.include_router(peers.router)
app.include_router(valuation.router)
app.include_router(portfolio.router)
app.include_router(documents.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

