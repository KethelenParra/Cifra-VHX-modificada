"""
Rotas HTTP da Cifra VHX.

O frontend envia o texto; a chave SOL permanece só no backend.
Erros de validação da cifra viram HTTP 400.
"""

from fastapi import APIRouter, HTTPException

from backend.model.esquemas import PedidoCifra, RespostaCifra
from backend.service.cifra import criptografar, descriptografar

rotas = APIRouter()


def _executar(funcao):
    """Chama a cifra e traduz ValueError em resposta HTTP 400."""
    try:
        return funcao()
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro


@rotas.get("/health")
def saude():
    """Confirma que a API está no ar (útil para teste rápido)."""
    return {"status": "ok", "cifra": "VHX"}


@rotas.post("/encrypt", response_model=RespostaCifra)
def rota_criptografar(pedido: PedidoCifra):
    """Criptografa o texto e devolve o resultado com todos os passos."""
    return _executar(lambda: criptografar(pedido.texto))


@rotas.post("/decrypt", response_model=RespostaCifra)
def rota_descriptografar(pedido: PedidoCifra):
    """Descriptografa o texto cifrado, na ordem inversa das etapas."""
    return _executar(lambda: descriptografar(pedido.texto))
