"""
Formatos de entrada e saída da API.
"""

from typing import List, Literal

from pydantic import BaseModel, Field


class PedidoCifra(BaseModel):
    """Corpo JSON de /encrypt e /decrypt - o que o usuário envia"""

    texto: str = Field(..., min_length=1)


class Passo(BaseModel):
    """Uma etapa resumida, exibida nos cartões do modo explicação."""

    titulo: str
    descricao: str
    valor: str


class ContaLetra(BaseModel):
    """Uma linha da tabela Vigenère: letra do texto + letra da chave."""

    letra: str
    valor: int
    letra_chave: str
    valor_chave: int
    operacao: str
    conta: str
    letra_resultado: str
    valor_resultado: int


class ContaBloco(BaseModel):
    """Um bloco de até 3 letras, antes e depois da inversão."""

    indice: int
    titulo: str
    bloco: str
    bloco_invertido: str
    resumo: str


class RespostaCifra(BaseModel):
    """Resposta completa usada pelo modo desafio e pelo modo explicação - resultado final mais o detalhamento pedagógico"""

    operacao: Literal["criptografar", "descriptografar"]
    texto_entrada: str
    texto_normalizado: str
    chave: str
    chave_invertida: str
    chave_montada: str
    depois_vigenere: str
    depois_blocos: str
    texto_saida: str
    alfabeto: str
    passos: List[Passo]
    letras_vigenere: List[ContaLetra]
    blocos: List[ContaBloco]
