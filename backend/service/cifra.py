"""
Orquestração da Cifra VHX.

Criptografia (nessa ordem):
    1. Normalizar para A–Z
    2. Montar a chave SOL / LOS
    3. Vigenère: C = (P + K) mod 26
    4. Inverter blocos de 3

Descriptografia: o caminho inverso (desinverter blocos, Vigenère inversa).
"""

from backend.model.esquemas import Passo, RespostaCifra
from .alfabeto import mapa_alfabeto, so_letras
from .blocos import chave_em_grupos, inverter_blocos, montar_chave
from .configuracao import CHAVE, TAMANHO_BLOCO
from .vigenere import criptografar_vigenere, descriptografar_vigenere


def _pegar_letras(texto: str, mensagem_erro: str) -> str:
    """Normaliza o texto e recusa entrada sem nenhuma letra A–Z."""
    limpo = so_letras(texto)
    if not limpo:
        raise ValueError(mensagem_erro)
    return limpo


def criptografar(texto: str) -> RespostaCifra:
    """Executa as etapas da VHX e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto precisa possuir pelo menos uma letra de A a Z.",
    )
    chave_montada = montar_chave(len(normalizado))
    depois_vigenere, letras = criptografar_vigenere(normalizado, chave_montada)
    saida, blocos = inverter_blocos(depois_vigenere)

    passos = [
        Passo(
            titulo="1. Normalização",
            descricao="Maiúsculas, sem acento, espaço ou número.",
            valor=normalizado,
        ),
        Passo(
            titulo="2. Montar a chave",
            descricao=f"Começa em {CHAVE} e alterna com {CHAVE[::-1]} a cada {TAMANHO_BLOCO} letras.",
            valor=f"{chave_montada}   ({chave_em_grupos(chave_montada)})",
        ),
        Passo(
            titulo="3. Vigenère",
            descricao="C = (P + K) mod 26",
            valor=depois_vigenere,
        ),
        Passo(
            titulo="4. Inverter blocos de 3",
            descricao="Parte o texto de 3 em 3 e vira cada pedaço ao contrário.",
            valor=" | ".join(bloco.bloco_invertido for bloco in blocos),
        ),
        Passo(
            titulo="5. Texto cifrado",
            descricao="Junta os blocos invertidos.",
            valor=saida,
        ),
    ]

    return RespostaCifra(
        operacao="criptografar",
        texto_entrada=texto,
        texto_normalizado=normalizado,
        chave=CHAVE,
        chave_invertida=CHAVE[::-1],
        chave_montada=chave_montada,
        depois_vigenere=depois_vigenere,
        depois_blocos=saida,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        passos=passos,
        letras_vigenere=letras,
        blocos=blocos,
    )


def descriptografar(texto: str) -> RespostaCifra:
    """Desfaz a VHX na ordem inversa e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto cifrado precisa possuir pelo menos uma letra.",
    )

    depois_desinverter, blocos = inverter_blocos(normalizado)
    chave_montada = montar_chave(len(depois_desinverter))
    saida, letras = descriptografar_vigenere(depois_desinverter, chave_montada)

    passos = [
        Passo(
            titulo="1. Texto cifrado",
            descricao="O que chegou para abrir.",
            valor=normalizado,
        ),
        Passo(
            titulo="2. Desinverter os blocos",
            descricao="De 3 em 3, vira de novo.",
            valor=" | ".join(bloco.bloco_invertido for bloco in blocos),
        ),
        Passo(
            titulo="3. Mesma chave",
            descricao=f"{CHAVE} / {CHAVE[::-1]} no tamanho do texto.",
            valor=f"{chave_montada}   ({chave_em_grupos(chave_montada)})",
        ),
        Passo(
            titulo="4. Vigenère ao contrário",
            descricao="P = (C - K) mod 26",
            valor=saida,
        ),
        Passo(
            titulo="5. Texto recuperado",
            descricao="Mensagem original.",
            valor=saida,
        ),
    ]

    return RespostaCifra(
        operacao="descriptografar",
        texto_entrada=texto,
        texto_normalizado=normalizado,
        chave=CHAVE,
        chave_invertida=CHAVE[::-1],
        chave_montada=chave_montada,
        depois_vigenere=depois_desinverter,
        depois_blocos=normalizado,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        passos=passos,
        letras_vigenere=letras,
        blocos=blocos,
    )
