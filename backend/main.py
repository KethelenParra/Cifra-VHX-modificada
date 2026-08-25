"""
Ponto de entrada da aplicação.

Sobe a API FastAPI, libera CORS para o frontend local e serve os
arquivos estáticos da pasta frontend na raiz do site.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.rotas import rotas

app = FastAPI(
    title="Cifra VHX",
    description="Vigenère + inversão de blocos",
    version="2.0.0",
)

# Em trabalho acadêmico local, qualquer origem pode chamar a API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints JSON ficam em /api (health, encrypt, decrypt).
app.include_router(rotas, prefix="/api")

# O restante das URLs entrega o site (HTML, CSS e JavaScript).
pasta_frontend = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(pasta_frontend), html=True), name="frontend")
