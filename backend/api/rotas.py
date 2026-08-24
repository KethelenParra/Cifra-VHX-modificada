from fastapi import APIRouter, HTTPException

from backend.model.esquemas import PedidoCifra, RespostaCifra
from backend.service.cifra import criptografar, descriptografar

rotas = APIRouter()


def _executar(funcao):
    try:
        return funcao()
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro


@rotas.get("/health")
def saude():
    return {"status": "ok", "cifra": "VHX"}


@rotas.post("/encrypt", response_model=RespostaCifra)
def rota_criptografar(pedido: PedidoCifra):
    return _executar(lambda: criptografar(pedido.texto))


@rotas.post("/decrypt", response_model=RespostaCifra)
def rota_descriptografar(pedido: PedidoCifra):
    return _executar(lambda: descriptografar(pedido.texto))
