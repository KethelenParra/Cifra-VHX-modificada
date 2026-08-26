"""
Constantes da Cifra Criptografada.

A chave não é digitada na tela: fica fixa aqui para o modo desafio
não revelar o segredo.

Há duas Vigenères com regras diferentes:
- 1ª chave: SOL, alternando com LOS a cada 3 letras
- 2ª chave: derivada da primeira, avançando cada letra 1 posição (SOL → TPM),
  alternando com MPT
"""

from .alfabeto import avancar_letras

# Palavra-chave da 1ª Vigenère. A cada 3 letras ela se inverte (SOL, LOS, SOL…).
CHAVE = "SOL"

TAMANHO_BLOCO = 3   # tamanho usado na montagem da chave e na inversão de blocos

# Quantas posições cada letra da 1ª chave avança para formar a 2ª (S→T, O→P, L→M).
DESLOCAMENTO_SEGUNDA_CHAVE = 1

# Palavra-chave da 2ª Vigenère. Alterna com a invertida (TPM, MPT, TPM…).
CHAVE_2 = avancar_letras(CHAVE, DESLOCAMENTO_SEGUNDA_CHAVE)
