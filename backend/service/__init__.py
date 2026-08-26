"""
Regras da Cifra VHX Dupla.

Cada módulo trata uma etapa:
- alfabeto: conversão letra ↔ número (A=0 … Z=25) e derivação da 2ª chave
- blocos: montagem das chaves alternadas (SOL/LOS e TPM/MPT) e inversão de 3 em 3
- vigenere: soma e subtração modular
- cifra: orquestra as duas Vigenères com a inversão no meio
"""
