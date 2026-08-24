import string
import unicodedata

ALFABETO = string.ascii_uppercase


def indice(letra):
    return ord(letra) - ord("A")


def letra_do_indice(numero):
    return chr((numero % 26) + ord("A"))


def so_letras(texto):
    # tira acento, espaço e pontuação; deixa só A-Z
    separado = unicodedata.normalize("NFD", texto.upper())
    sem_acento = "".join(
        caractere for caractere in separado
        if unicodedata.category(caractere) != "Mn"
    )
    return "".join(caractere for caractere in sem_acento if "A" <= caractere <= "Z")


def mapa_alfabeto():
    return "  ".join(f"{letra}={i}" for i, letra in enumerate(ALFABETO))
