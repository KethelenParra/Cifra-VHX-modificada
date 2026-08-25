"""
Preenchimento para a cifra de Hill.

A Hill precisa de um número par de letras. Se o texto tiver
comprimento ímpar, acrescenta-se X no final. Na descriptografia,
esse X extra é removido quando estiver na última posição.
"""

from .configuracao import LETRA_X, TAMANHO_PAR


def completar_com_x(texto: str):
    """
    Garante comprimento par.

    Devolve (texto, True) se o X foi acrescentado; (texto, False) caso contrário.
    """
    if len(texto) % TAMANHO_PAR == 0:
        return texto, False
    return texto + LETRA_X, True


def tirar_x(texto: str):
    """
    Remove o X de preenchimento, se ele estiver no fim e o tamanho for par.

    Devolve (texto, True) se removeu; (texto, False) se não havia X extra.
    """
    if texto.endswith(LETRA_X) and len(texto) % TAMANHO_PAR == 0:
        return texto[:-1], True
    return texto, False
