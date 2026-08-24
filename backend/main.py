from __future__ import annotations

import random
import string
import unicodedata
from pathlib import Path
from typing import List, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


app = FastAPI(
    title="VHX Cipher API",
    description="API didática para criptografia e descriptografia da Cifra VHX.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


BLOCK_SIZE = 3
ALPHABET = string.ascii_uppercase


class CipherRequest(BaseModel):
    text: str = Field(..., min_length=1)
    key: str = Field(..., min_length=1)


class Step(BaseModel):
    title: str
    description: str
    value: str


class LetterCalc(BaseModel):
    input_letter: str
    input_value: int
    key_letter: str
    key_value: int
    operation: str
    formula: str
    result_letter: str
    result_value: int


class BlockCalc(BaseModel):
    index: int
    title: str
    input_block: str
    working_block: str
    key_used: str
    key_type: str
    after_vigenere: str
    after_reverse: str
    letters: List[LetterCalc]
    summary: str


class CipherResponse(BaseModel):
    operation: Literal["encrypt", "decrypt"]
    input_text: str
    normalized_text: str
    key: str
    reverse_key: str
    output_text: str
    alphabet: str
    steps: List[Step]
    blocks: List[BlockCalc]


class RandomKeyResponse(BaseModel):
    key: str


def letter_index(char: str) -> int:
    return ord(char) - ord("A")


def from_index(value: int) -> str:
    return chr((value % 26) + ord("A"))


def normalize_letters(value: str) -> str:
    """
    Remove acentos, espaços, pontuação e mantém apenas A-Z.
    Ex.: "Segurança da Informação!" -> "SEGURANCADAINFORMACAO"
    """
    decomposed = unicodedata.normalize("NFD", value.upper())
    without_accents = "".join(
        char for char in decomposed
        if unicodedata.category(char) != "Mn"
    )
    return "".join(char for char in without_accents if "A" <= char <= "Z")


def validate_key(key: str) -> str:
    normalized = normalize_letters(key)
    if len(normalized) != BLOCK_SIZE:
        raise HTTPException(
            status_code=400,
            detail="A chave deve possuir exatamente 3 letras de A a Z.",
        )
    return normalized


def split_blocks(text: str, size: int = BLOCK_SIZE) -> List[str]:
    return [text[i:i + size] for i in range(0, len(text), size)]


def key_for_block(key: str, block_index: int, block_length: int) -> str:
    """
    Blocos 1, 3, 5... usam chave normal.
    Blocos 2, 4, 6... usam chave invertida.
    Se o último bloco for menor, usa só o prefixo necessário.
    """
    oriented = key if block_index % 2 == 0 else key[::-1]
    return oriented[:block_length]


def encrypt_letter(plain: str, key_char: str) -> LetterCalc:
    p = letter_index(plain)
    k = letter_index(key_char)
    c = (p + k) % 26
    return LetterCalc(
        input_letter=plain,
        input_value=p,
        key_letter=key_char,
        key_value=k,
        operation="C = (P + K) mod 26",
        formula=f"({p} + {k}) mod 26 = {c}",
        result_letter=from_index(c),
        result_value=c,
    )


def decrypt_letter(cipher: str, key_char: str) -> LetterCalc:
    c = letter_index(cipher)
    k = letter_index(key_char)
    p = (c - k) % 26
    return LetterCalc(
        input_letter=cipher,
        input_value=c,
        key_letter=key_char,
        key_value=k,
        operation="P = (C - K) mod 26",
        formula=f"({c} - {k}) mod 26 = {p}",
        result_letter=from_index(p),
        result_value=p,
    )


def encrypt_vhx(text: str, key: str) -> CipherResponse:
    normalized_text = normalize_letters(text)
    normalized_key = validate_key(key)

    if not normalized_text:
        raise HTTPException(
            status_code=400,
            detail="O texto precisa possuir pelo menos uma letra de A a Z.",
        )

    original_blocks = split_blocks(normalized_text)
    vigenere_blocks = []
    inverted_blocks = []
    key_blocks = []
    blocks: List[BlockCalc] = []

    for index, block in enumerate(original_blocks):
        current_key = key_for_block(normalized_key, index, len(block))
        letters = [
            encrypt_letter(plain_char, key_char)
            for plain_char, key_char in zip(block, current_key)
        ]
        encrypted = "".join(item.result_letter for item in letters)
        inverted = encrypted[::-1]
        key_type = "normal" if index % 2 == 0 else "invertida"

        key_blocks.append(current_key)
        vigenere_blocks.append(encrypted)
        inverted_blocks.append(inverted)
        blocks.append(
            BlockCalc(
                index=index + 1,
                title=f"Bloco {index + 1}",
                input_block=block,
                working_block=block,
                key_used=current_key,
                key_type=key_type,
                after_vigenere=encrypted,
                after_reverse=inverted,
                letters=letters,
                summary=(
                    f"{block} com chave {current_key} ({key_type}) "
                    f"resulta em {encrypted}; invertendo o bloco: {inverted}."
                ),
            )
        )

    output = "".join(inverted_blocks)

    steps = [
        Step(
            title="1. Normalização",
            description=(
                "O texto é convertido para maiúsculas e são removidos "
                "acentos, espaços, números e pontuação."
            ),
            value=normalized_text,
        ),
        Step(
            title="2. Divisão em blocos",
            description=(
                "A VHX trabalha em blocos de 3 letras. "
                "O último bloco pode possuir 1 ou 2 letras."
            ),
            value=" | ".join(original_blocks),
        ),
        Step(
            title="3. Alternância da chave",
            description=(
                "Blocos ímpares usam a chave normal e blocos pares usam "
                "a chave invertida. Essa alternância é a primeira modificação "
                "em relação à Vigenère tradicional."
            ),
            value=" | ".join(key_blocks),
        ),
        Step(
            title="4. Cálculo da Vigenère",
            description=(
                "Cada letra vale de A=0 até Z=25. "
                "A fórmula da criptografia é C = (P + K) mod 26."
            ),
            value=" | ".join(vigenere_blocks),
        ),
        Step(
            title="5. Inversão dos blocos",
            description=(
                "Depois da Vigenère, cada bloco cifrado é invertido. "
                "Essa é a segunda modificação da VHX."
            ),
            value=" | ".join(inverted_blocks),
        ),
        Step(
            title="6. Texto cifrado",
            description="Os blocos invertidos são unidos para formar a saída final.",
            value=output,
        ),
    ]

    return CipherResponse(
        operation="encrypt",
        input_text=text,
        normalized_text=normalized_text,
        key=normalized_key,
        reverse_key=normalized_key[::-1],
        output_text=output,
        alphabet="  ".join(f"{letter}={index}" for index, letter in enumerate(ALPHABET)),
        steps=steps,
        blocks=blocks,
    )


def decrypt_vhx(text: str, key: str) -> CipherResponse:
    normalized_text = normalize_letters(text)
    normalized_key = validate_key(key)

    if not normalized_text:
        raise HTTPException(
            status_code=400,
            detail="O texto cifrado precisa possuir pelo menos uma letra.",
        )

    cipher_blocks = split_blocks(normalized_text)
    uninverted_blocks = []
    plain_blocks = []
    key_blocks = []
    blocks: List[BlockCalc] = []

    for index, block in enumerate(cipher_blocks):
        uninverted = block[::-1]
        current_key = key_for_block(normalized_key, index, len(block))
        letters = [
            decrypt_letter(cipher_char, key_char)
            for cipher_char, key_char in zip(uninverted, current_key)
        ]
        plain = "".join(item.result_letter for item in letters)
        key_type = "normal" if index % 2 == 0 else "invertida"

        uninverted_blocks.append(uninverted)
        key_blocks.append(current_key)
        plain_blocks.append(plain)
        blocks.append(
            BlockCalc(
                index=index + 1,
                title=f"Bloco {index + 1}",
                input_block=block,
                working_block=uninverted,
                key_used=current_key,
                key_type=key_type,
                after_vigenere=plain,
                after_reverse=uninverted,
                letters=letters,
                summary=(
                    f"{block} é desinvertido para {uninverted}; "
                    f"com chave {current_key} ({key_type}) recupera-se {plain}."
                ),
            )
        )

    output = "".join(plain_blocks)

    steps = [
        Step(
            title="1. Texto cifrado",
            description="Entrada recebida para descriptografia.",
            value=normalized_text,
        ),
        Step(
            title="2. Divisão em blocos",
            description="O texto cifrado é novamente dividido em blocos de 3.",
            value=" | ".join(cipher_blocks),
        ),
        Step(
            title="3. Desfazer a inversão",
            description=(
                "Como a última etapa da criptografia foi inverter cada bloco, "
                "essa precisa ser a primeira etapa da descriptografia."
            ),
            value=" | ".join(uninverted_blocks),
        ),
        Step(
            title="4. Recuperar as chaves",
            description=(
                "A chave volta a alternar entre a forma normal e a invertida, "
                "na mesma ordem da criptografia."
            ),
            value=" | ".join(key_blocks),
        ),
        Step(
            title="5. Cálculo da Vigenère inversa",
            description="Agora subtraímos a chave: P = (C - K) mod 26.",
            value=" | ".join(plain_blocks),
        ),
        Step(
            title="6. Texto recuperado",
            description="Os blocos descriptografados são unidos.",
            value=output,
        ),
    ]

    return CipherResponse(
        operation="decrypt",
        input_text=text,
        normalized_text=normalized_text,
        key=normalized_key,
        reverse_key=normalized_key[::-1],
        output_text=output,
        alphabet="  ".join(f"{letter}={index}" for index, letter in enumerate(ALPHABET)),
        steps=steps,
        blocks=blocks,
    )


@app.get("/api/health")
def health():
    return {"status": "ok", "cipher": "VHX"}


@app.get("/api/random-key", response_model=RandomKeyResponse)
def random_key():
    return RandomKeyResponse(
        key="".join(random.choice(string.ascii_uppercase) for _ in range(BLOCK_SIZE))
    )


@app.post("/api/encrypt", response_model=CipherResponse)
def encrypt(request: CipherRequest):
    return encrypt_vhx(request.text, request.key)


@app.post("/api/decrypt", response_model=CipherResponse)
def decrypt(request: CipherRequest):
    return decrypt_vhx(request.text, request.key)


# Serve o frontend pelo próprio FastAPI.
frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
