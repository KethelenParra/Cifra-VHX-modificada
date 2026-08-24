from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.rotas import rotas

app = FastAPI(
    title="Cifra VHX",
    description="Vigenère + inversão de blocos + Hill",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(rotas, prefix="/api")

pasta_frontend = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(pasta_frontend), html=True), name="frontend")
