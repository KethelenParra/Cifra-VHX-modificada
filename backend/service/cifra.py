"""
Orquestração da Cifra VHX.

Criptografia (nessa ordem):
    1. Normalizar para A–Z
    2. Montar a chave SOL / LOS
    3. Vigenère: C = (P + K) mod 26
    4. Inverter blocos de 3
    5. Completar com X se o tamanho for ímpar
    6. Hill nos pares

Descriptografia: o caminho inverso (Hill inversa, tirar X,
desinverter blocos, Vigenère inversa).
"""

from backend.model.esquemas import Passo, RespostaCifra
from .alfabeto import mapa_alfabeto, so_letras
from .blocos import chave_em_grupos, inverter_blocos, montar_chave
from .configuracao import CHAVE, LETRA_X, MATRIZ_HILL, MATRIZ_HILL_INVERSA, TAMANHO_BLOCO
from .hill import hill_criptografar, hill_descriptografar, texto_da_matriz
from .preenchimento import completar_com_x, tirar_x
from .vigenere import criptografar_vigenere, descriptografar_vigenere


def _pegar_letras(texto: str, mensagem_erro: str) -> str:
    """Normaliza o texto e recusa entrada sem nenhuma letra A–Z."""
    limpo = so_letras(texto)
    if not limpo:
        raise ValueError(mensagem_erro)
    return limpo


def criptografar(texto: str) -> RespostaCifra:
    """Executa as seis etapas da VHX e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto precisa possuir pelo menos uma letra de A a Z.",
    )
    chave_montada = montar_chave(len(normalizado))
    depois_vigenere, letras = criptografar_vigenere(normalizado, chave_montada)
    depois_blocos, blocos = inverter_blocos(depois_vigenere)
    texto_com_x, usou_x = completar_com_x(depois_blocos)
    saida, pares = hill_criptografar(texto_com_x)

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
            titulo="5. Completar com X",
            descricao=f"Se sobrar letra ímpar, entra um {LETRA_X} para a Hill trabalhar em pares.",
            valor=texto_com_x if usou_x else "Não precisou de X.",
        ),
        Passo(
            titulo="6. Hill",
            descricao=f"Cada par vezes a matriz {texto_da_matriz(MATRIZ_HILL)} (mod 26).",
            valor=" | ".join(par.par_resultado for par in pares),
        ),
        Passo(
            titulo="7. Texto cifrado",
            descricao="Junta os pares.",
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
        depois_blocos=depois_blocos,
        texto_com_x=texto_com_x,
        usou_x=usou_x,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        matriz_hill=texto_da_matriz(MATRIZ_HILL),
        passos=passos,
        letras_vigenere=letras,
        blocos=blocos,
        pares_hill=pares,
    )


def descriptografar(texto: str) -> RespostaCifra:
    """Desfaz a VHX na ordem inversa e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto cifrado precisa possuir pelo menos uma letra.",
    )
    if len(normalizado) % 2 != 0:
        raise ValueError(
            "O texto cifrado tem de ter quantidade par de letras (Hill trabalha em pares)."
        )

    depois_hill, pares = hill_descriptografar(normalizado)
    sem_x, usou_x = tirar_x(depois_hill)
    depois_desinverter, blocos = inverter_blocos(sem_x)
    chave_montada = montar_chave(len(depois_desinverter))
    saida, letras = descriptografar_vigenere(depois_desinverter, chave_montada)

    passos = [
        Passo(
            titulo="1. Texto cifrado",
            descricao="O que chegou para abrir.",
            valor=normalizado,
        ),
        Passo(
            titulo="2. Hill ao contrário",
            descricao=f"Par vezes a matriz {texto_da_matriz(MATRIZ_HILL_INVERSA)} (mod 26).",
            valor=" | ".join(par.par_resultado for par in pares),
        ),
        Passo(
            titulo="3. Tirar o X",
            descricao=f"Se o último caractere for {LETRA_X} de preenchimento, sai fora.",
            valor=sem_x if usou_x else "Não tinha X extra.",
        ),
        Passo(
            titulo="4. Desinverter os blocos",
            descricao="De 3 em 3, vira de novo.",
            valor=" | ".join(bloco.bloco_invertido for bloco in blocos),
        ),
        Passo(
            titulo="5. Mesma chave",
            descricao=f"{CHAVE} / {CHAVE[::-1]} no tamanho do texto.",
            valor=f"{chave_montada}   ({chave_em_grupos(chave_montada)})",
        ),
        Passo(
            titulo="6. Vigenère ao contrário",
            descricao="P = (C - K) mod 26",
            valor=saida,
        ),
        Passo(
            titulo="7. Texto recuperado",
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
        depois_blocos=sem_x,
        texto_com_x=depois_hill,
        usou_x=usou_x,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        matriz_hill=texto_da_matriz(MATRIZ_HILL_INVERSA),
        passos=passos,
        letras_vigenere=letras,
        blocos=blocos,
        pares_hill=pares,
    )
