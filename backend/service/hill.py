"""
Cifra de Hill em blocos de 2 letras.

Cada par vira um vetor coluna [p1, p2]. O novo par é:

    [ c1 ]       [ a  b ]   [ p1 ]
    [ c2 ]   =   [ c  d ] × [ p2 ]   (mod 26)

Na criptografia usa-se MATRIZ_HILL; na descriptografia, a inversa.
"""

from backend.model.esquemas import ContaParHill
from .alfabeto import indice, letra_do_indice
from .configuracao import MATRIZ_HILL, MATRIZ_HILL_INVERSA, TAMANHO_PAR


def texto_da_matriz(matriz) -> str:
    """Formato compacto para mostrar a matriz na tela: [ a b ; c d ]."""
    (a, b), (c, d) = matriz
    return f"[ {a} {b} ; {c} {d} ]"


def _multiplicar_par(par: str, matriz):
    """Multiplica um par de letras pela matriz 2×2 (mod 26)."""
    p1 = indice(par[0])
    p2 = indice(par[1])
    a, b = matriz[0]
    c, d = matriz[1]

    c1 = (a * p1 + b * p2) % 26
    c2 = (c * p1 + d * p2) % 26
    resultado = letra_do_indice(c1) + letra_do_indice(c2)

    conta1 = f"({a}*{p1} + {b}*{p2}) mod 26 = {c1}"
    conta2 = f"({c}*{p1} + {d}*{p2}) mod 26 = {c2}"
    return resultado, conta1, conta2


def aplicar_hill(texto: str, matriz):
    """Percorre o texto de 2 em 2 e aplica a matriz em cada par."""
    if len(texto) % TAMANHO_PAR != 0:
        raise ValueError("A cifra de Hill precisa de um número par de letras.")

    contas = []
    pedacos = []

    for i in range(0, len(texto), TAMANHO_PAR):
        par = texto[i:i + TAMANHO_PAR]
        resultado, conta1, conta2 = _multiplicar_par(par, matriz)
        pedacos.append(resultado)
        contas.append(
            ContaParHill(
                indice=i // TAMANHO_PAR + 1,
                par=par,
                letra_esq=par[0],
                valor_esq=indice(par[0]),
                letra_dir=par[1],
                valor_dir=indice(par[1]),
                conta_linha1=conta1,
                conta_linha2=conta2,
                par_resultado=resultado,
                letra_res_esq=resultado[0],
                letra_res_dir=resultado[1],
                resumo=f"{par} → {resultado}",
            )
        )

    return "".join(pedacos), contas


def hill_criptografar(texto: str):
    """Hill com a matriz direta [ 3 3 ; 2 5 ]."""
    return aplicar_hill(texto, MATRIZ_HILL)


def hill_descriptografar(texto: str):
    """Hill com a matriz inversa [ 15 17 ; 20 9 ]."""
    return aplicar_hill(texto, MATRIZ_HILL_INVERSA)
