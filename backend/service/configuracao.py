"""
Constantes da Cifra VHX.

A chave não é digitada na tela: fica fixa aqui para o modo desafio
não revelar o segredo.
"""

# Palavra-chave da Vigenère. A cada 3 letras ela se inverte (SOL, LOS, SOL…).
CHAVE = "SOL"

TAMANHO_BLOCO = 3   # tamanho usado na montagem da chave e na inversão de blocos
