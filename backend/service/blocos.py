"""
Montagem da chave alternada e inversão dos blocos.

A mesma montagem serve para as duas chaves da VHX Dupla:
SOL se repete invertida (SOL / LOS) e TPM se repete invertida (TPM / MPT),
até cobrir a mensagem.

No meio das duas Vigenères, o texto é cortado de 3 em 3 e cada pedaço
é escrito ao contrário. A mesma inversão desfaz o efeito, porque
inverter duas vezes devolve o bloco original.
"""

from backend.model.esquemas import ContaBloco
from .configuracao import CHAVE, TAMANHO_BLOCO


def montar_chave(tamanho: int, chave: str = CHAVE) -> str:
    """
    Repete a chave e a chave invertida até atingir o tamanho do texto.

    Exemplo com SOL e 5 letras (DADOS): SOL + LO → SOLLO
    Exemplo com TPM e 6 letras (ATAQUE): TPM + MPT → TPMMPT
    """
    normal = chave
    invertida = chave[::-1]
    pedacos = []
    falta = tamanho
    usa_normal = True

    while falta > 0:
        fonte = normal if usa_normal else invertida
        pega = min(TAMANHO_BLOCO, falta)
        pedacos.append(fonte[:pega])
        falta -= pega
        usa_normal = not usa_normal

    return "".join(pedacos)


def chave_em_grupos(chave_montada: str) -> str:
    """Separa a chave montada de 3 em 3 para facilitar a leitura na tela."""
    return " | ".join(
        chave_montada[i:i + TAMANHO_BLOCO]
        for i in range(0, len(chave_montada), TAMANHO_BLOCO)
    )


def cortar_blocos(texto: str, tamanho: int = TAMANHO_BLOCO) -> list:
    """Parte o texto em fatias de no máximo `tamanho` letras."""
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]


def inverter_blocos(texto: str):
    """
    Inverte cada bloco de 3 (o último pode ser menor).

    Exemplo: VOOZG → VOO | ZG → OOV | GZ
    Devolve o texto juntado e a lista de contas para o modo explicação.
    """
    contas = []
    invertidos = []

    for i, bloco in enumerate(cortar_blocos(texto), start=1):
        invertido = bloco[::-1]
        invertidos.append(invertido)
        contas.append(
            ContaBloco(
                indice=i,
                titulo=f"Bloco {i}",
                bloco=bloco,
                bloco_invertido=invertido,
                resumo=f"{bloco} → {invertido}",
            )
        )

    return "".join(invertidos), contas
