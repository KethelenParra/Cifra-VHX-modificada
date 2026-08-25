"""
Constantes da Cifra VHX.

A chave não é digitada na tela: fica fixa aqui para o modo desafio
não revelar o segredo. A matriz inversa foi calculada de forma que
M × M⁻¹ ≡ I (mod 26), permitindo desfazer a Hill.
"""

# Palavra-chave da Vigenère. A cada 3 letras ela se inverte (SOL, LOS, SOL…).
CHAVE = "SOL"

TAMANHO_BLOCO = 3   # tamanho usado na montagem da chave e na inversão
TAMANHO_PAR = 2     # a Hill trabalha com vetores de 2 letras
LETRA_X = "X"       # preenchimento quando o texto tem comprimento ímpar

# Novo par = matriz × par antigo, com aritmética módulo 26.
MATRIZ_HILL = (
    (3, 3),
    (2, 5),
)

# Matriz inversa de MATRIZ_HILL no anel Z/26Z.
MATRIZ_HILL_INVERSA = (
    (15, 17),
    (20, 9),
)
