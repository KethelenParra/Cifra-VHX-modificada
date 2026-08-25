"""
Alfabeto clássico da criptografia (26 letras).

A = 0, B = 1, …, Z = 25.
O texto do usuário é normalizado para esse alfabeto: maiúsculas,
sem acento, espaço, número ou pontuação.
"""

import string
import unicodedata

ALFABETO = string.ascii_uppercase


def indice(letra: str) -> int:
    """Converte uma letra A–Z no número correspondente (A → 0)."""
    return ord(letra) - ord("A")


def letra_do_indice(numero: int) -> str:
    """Converte um número (mod 26) de volta em letra A–Z."""
    return chr((numero % 26) + ord("A"))


def so_letras(texto: str) -> str:
    """
    Deixa apenas A–Z.

    Exemplo: "Dá dos!" → "DADOS"
    """
    separado = unicodedata.normalize("NFD", texto.upper())
    sem_acento = "".join(
        caractere for caractere in separado
        if unicodedata.category(caractere) != "Mn"
    )
    return "".join(caractere for caractere in sem_acento if "A" <= caractere <= "Z")


def mapa_alfabeto() -> str:
    """Texto pronto para a tela: A=0  B=1  …  Z=25."""
    return "  ".join(f"{letra}={i}" for i, letra in enumerate(ALFABETO))
