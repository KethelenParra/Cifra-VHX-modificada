from backend.model.esquemas import ContaBloco
from .configuracao import CHAVE, TAMANHO_BLOCO


def montar_chave(tamanho, chave=CHAVE):
    # SOL, depois LOS, depois SOL... até cobrir o texto
    # DADOS (5 letras) vira SOLLO
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


def chave_em_grupos(chave_montada):
    return " | ".join(
        chave_montada[i:i + TAMANHO_BLOCO]
        for i in range(0, len(chave_montada), TAMANHO_BLOCO)
    )


def cortar_blocos(texto, tamanho=TAMANHO_BLOCO):
    return [texto[i:i + tamanho] for i in range(0, len(texto), tamanho)]


def inverter_blocos(texto):
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
