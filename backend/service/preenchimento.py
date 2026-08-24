from .configuracao import LETRA_X, TAMANHO_PAR


def completar_com_x(texto):
    if len(texto) % TAMANHO_PAR == 0:
        return texto, False
    return texto + LETRA_X, True


def tirar_x(texto):
    if texto.endswith(LETRA_X) and len(texto) % TAMANHO_PAR == 0:
        return texto[:-1], True
    return texto, False
