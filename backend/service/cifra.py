"""
Orquestração da Cifra Criptografada.

Criptografia (nessa ordem):
    1. Normalizar para A–Z
    2. Montar a 1ª chave SOL / LOS
    3. Vigenère 1: C = (P + K) mod 26
    4. Inverter blocos de 3
    5. Montar a 2ª chave TPM / MPT (derivada: cada letra de SOL avança 1)
    6. Vigenère 2: C = (P + K) mod 26

Descriptografia: o caminho inverso (Vigenère 2 inversa, desinverter blocos,
Vigenère 1 inversa). Quem aplicar só uma Vigenère clássica não recupera
a palavra original. As tabelas de contas vão logo abaixo do passo
correspondente, para a apresentação seguir a ordem da cifra.
"""

from backend.model.esquemas import Passo, RespostaCifra
from .alfabeto import mapa_alfabeto, so_letras
from .blocos import chave_em_grupos, inverter_blocos, montar_chave
from .configuracao import CHAVE, CHAVE_2, TAMANHO_BLOCO
from .vigenere import criptografar_vigenere, descriptografar_vigenere


def _pegar_letras(texto: str, mensagem_erro: str) -> str:
    """Normaliza o texto e recusa entrada sem nenhuma letra A–Z."""
    limpo = so_letras(texto)
    if not limpo:
        raise ValueError(mensagem_erro)
    return limpo


def criptografar(texto: str) -> RespostaCifra:
    """Executa as etapas da Cifra Criptografada e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto precisa possuir pelo menos uma letra de A a Z.",
    )
    chave_montada = montar_chave(len(normalizado), CHAVE)
    depois_vigenere, letras = criptografar_vigenere(normalizado, chave_montada)
    depois_blocos, blocos = inverter_blocos(depois_vigenere)
    chave_montada_2 = montar_chave(len(depois_blocos), CHAVE_2)
    saida, letras_2 = criptografar_vigenere(depois_blocos, chave_montada_2)

    passos = [
        Passo(
            titulo="1. Normalização",
            descricao="Maiúsculas, sem acento, espaço ou número.",
            valor=normalizado,
        ),
        Passo(
            titulo="2. Montar a 1ª chave",
            descricao=f"Começa em {CHAVE} e alterna com {CHAVE[::-1]} a cada {TAMANHO_BLOCO} letras.",
            valor=f"{chave_montada}   ({chave_em_grupos(chave_montada)})",
        ),
        Passo(
            titulo="3. Vigenère 1",
            descricao="C = (P + K) mod 26, com a chave SOL / LOS.",
            valor=depois_vigenere,
            tabela="vigenere_1",
        ),
        Passo(
            titulo="4. Inverter blocos de 3",
            descricao="Parte o texto de 3 em 3 e vira cada pedaço ao contrário.",
            valor=" | ".join(bloco.bloco_invertido for bloco in blocos),
            tabela="blocos",
        ),
        Passo(
            titulo="5. Montar a 2ª chave",
            descricao=f"Deriva de {CHAVE} avançando 1 posição → {CHAVE_2}, e alterna com {CHAVE_2[::-1]}.",
            valor=f"{chave_montada_2}   ({chave_em_grupos(chave_montada_2)})",
        ),
        Passo(
            titulo="6. Vigenère 2",
            descricao="C = (P + K) mod 26, com a chave TPM / MPT.",
            valor=saida,
            tabela="vigenere_2",
        ),
        Passo(
            titulo="7. Texto cifrado",
            descricao="Resultado depois das duas Vigenères e da inversão.",
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
        chave_2=CHAVE_2,
        chave_2_invertida=CHAVE_2[::-1],
        chave_montada_2=chave_montada_2,
        depois_vigenere=depois_vigenere,
        depois_blocos=depois_blocos,
        depois_vigenere_2=saida,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        passos=passos,
        letras_vigenere=letras,
        letras_vigenere_2=letras_2,
        blocos=blocos,
    )


def descriptografar(texto: str) -> RespostaCifra:
    """Desfaz a Cifra Criptografada na ordem inversa e monta a resposta pedagógica."""
    normalizado = _pegar_letras(
        texto,
        "O texto cifrado precisa possuir pelo menos uma letra.",
    )

    chave_montada_2 = montar_chave(len(normalizado), CHAVE_2)
    depois_vigenere_2, letras_2 = descriptografar_vigenere(normalizado, chave_montada_2)
    depois_blocos, blocos = inverter_blocos(depois_vigenere_2)
    chave_montada = montar_chave(len(depois_blocos), CHAVE)
    saida, letras = descriptografar_vigenere(depois_blocos, chave_montada)

    passos = [
        Passo(
            titulo="1. Texto cifrado",
            descricao="O que chegou para abrir.",
            valor=normalizado,
        ),
        Passo(
            titulo="2. 2ª chave (derivada)",
            descricao=f"{CHAVE_2} / {CHAVE_2[::-1]} no tamanho do texto.",
            valor=f"{chave_montada_2}   ({chave_em_grupos(chave_montada_2)})",
        ),
        Passo(
            titulo="3. Vigenère 2 ao contrário",
            descricao="P = (C - K) mod 26, com TPM / MPT.",
            valor=depois_vigenere_2,
            tabela="vigenere_2",
        ),
        Passo(
            titulo="4. Desinverter os blocos",
            descricao="De 3 em 3, vira de novo.",
            valor=" | ".join(bloco.bloco_invertido for bloco in blocos),
            tabela="blocos",
        ),
        Passo(
            titulo="5. 1ª chave",
            descricao=f"{CHAVE} / {CHAVE[::-1]} no tamanho do texto.",
            valor=f"{chave_montada}   ({chave_em_grupos(chave_montada)})",
        ),
        Passo(
            titulo="6. Vigenère 1 ao contrário",
            descricao="P = (C - K) mod 26, com SOL / LOS.",
            valor=saida,
            tabela="vigenere_1",
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
        chave_2=CHAVE_2,
        chave_2_invertida=CHAVE_2[::-1],
        chave_montada_2=chave_montada_2,
        depois_vigenere=saida,
        depois_blocos=depois_blocos,
        depois_vigenere_2=depois_vigenere_2,
        texto_saida=saida,
        alfabeto=mapa_alfabeto(),
        passos=passos,
        letras_vigenere=letras,
        letras_vigenere_2=letras_2,
        blocos=blocos,
    )
