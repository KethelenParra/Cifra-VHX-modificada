from backend.model.esquemas import ContaLetra
from .alfabeto import indice, letra_do_indice


def criptografar_letra(letra, letra_chave):
    p = indice(letra)
    k = indice(letra_chave)
    c = (p + k) % 26
    return ContaLetra(
        letra=letra,
        valor=p,
        letra_chave=letra_chave,
        valor_chave=k,
        operacao="C = (P + K) mod 26",
        conta=f"({p} + {k}) mod 26 = {c}",
        letra_resultado=letra_do_indice(c),
        valor_resultado=c,
    )


def descriptografar_letra(letra, letra_chave):
    c = indice(letra)
    k = indice(letra_chave)
    p = (c - k) % 26
    return ContaLetra(
        letra=letra,
        valor=c,
        letra_chave=letra_chave,
        valor_chave=k,
        operacao="P = (C - K) mod 26",
        conta=f"({c} - {k}) mod 26 = {p}",
        letra_resultado=letra_do_indice(p),
        valor_resultado=p,
    )


def criptografar_vigenere(texto, chave_montada):
    contas = [
        criptografar_letra(letra, k)
        for letra, k in zip(texto, chave_montada)
    ]
    saida = "".join(item.letra_resultado for item in contas)
    return saida, contas


def descriptografar_vigenere(texto, chave_montada):
    contas = [
        descriptografar_letra(letra, k)
        for letra, k in zip(texto, chave_montada)
    ]
    saida = "".join(item.letra_resultado for item in contas)
    return saida, contas
