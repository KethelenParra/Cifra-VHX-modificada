from typing import List, Literal

from pydantic import BaseModel, Field


class PedidoCifra(BaseModel):
    texto: str = Field(..., min_length=1)


class Passo(BaseModel):
    titulo: str
    descricao: str
    valor: str


class ContaLetra(BaseModel):
    letra: str
    valor: int
    letra_chave: str
    valor_chave: int
    operacao: str
    conta: str
    letra_resultado: str
    valor_resultado: int


class ContaBloco(BaseModel):
    indice: int
    titulo: str
    bloco: str
    bloco_invertido: str
    resumo: str


class ContaParHill(BaseModel):
    indice: int
    par: str
    letra_esq: str
    valor_esq: int
    letra_dir: str
    valor_dir: int
    conta_linha1: str
    conta_linha2: str
    par_resultado: str
    letra_res_esq: str
    letra_res_dir: str
    resumo: str


class RespostaCifra(BaseModel):
    operacao: Literal["criptografar", "descriptografar"]
    texto_entrada: str
    texto_normalizado: str
    chave: str
    chave_invertida: str
    chave_montada: str
    depois_vigenere: str
    depois_blocos: str
    texto_com_x: str
    usou_x: bool
    texto_saida: str
    alfabeto: str
    matriz_hill: str
    passos: List[Passo]
    letras_vigenere: List[ContaLetra]
    blocos: List[ContaBloco]
    pares_hill: List[ContaParHill]
