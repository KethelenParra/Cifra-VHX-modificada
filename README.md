# Cifra VHX

Projeto acadêmico de criptografia simétrica usando uma modificação didática da Cifra de Vigenère.

## Tecnologias

### Backend
- Python
- FastAPI
- Uvicorn

### Frontend
- HTML
- CSS
- JavaScript puro

## Regra da VHX

A VHX deste projeto funciona assim:

1. Normaliza o texto para `A-Z`.
2. Divide o texto em blocos de 3.
3. Usa uma chave secreta de exatamente 3 letras.
4. Nos blocos 1, 3, 5... utiliza a chave normal.
5. Nos blocos 2, 4, 6... utiliza a chave invertida.
6. Aplica a fórmula da Vigenère:
   - Criptografia: `C = (P + K) mod 26`
   - Descriptografia: `P = (C - K) mod 26`
7. Depois da Vigenère, inverte as letras de cada bloco.
8. Junta os blocos e produz o texto cifrado.

Exemplo:

```text
Texto: ATAQUE
Chave: SOL

ATA | QUE
SOL | LOS

SHL | BIW

LHS | WIB

Resultado: LHSWIB
```

Descriptografia:

```text
LHS | WIB

SHL | BIW

SOL | LOS

ATA | QUE

Resultado: ATAQUE
```

## Modos do frontend

### 1. Modo Desafio

- O texto é digitado em campo oculto.
- A chave também fica oculta.
- Depois da criptografia, os campos são limpos.
- A tela mostra somente o texto criptografado.
- O programa mantém a chave apenas na memória da página para demonstrar a descriptografia.
- Ao clicar em `Descriptografar`, o texto original é revelado.

### 2. Modo Explicação

Mostra:

- normalização;
- divisão em blocos;
- chave normal e invertida;
- resultado da Vigenère;
- inversão dos blocos;
- texto final;
- caminho completo da descriptografia;
- explicação das diferenças entre Vigenère tradicional e VHX.

## Como executar

Abra um terminal dentro da pasta do projeto.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Depois abra:

```text
http://127.0.0.1:8000
```

A documentação automática da API fica em:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

- `GET /api/health`
- `GET /api/random-key`
- `POST /api/encrypt`
- `POST /api/decrypt`

Exemplo de requisição:

```json
{
  "text": "ATAQUE",
  "key": "SOL"
}
```

## Observação acadêmica

A VHX é uma cifra criada para demonstração e aprendizado. Ela não deve ser usada para proteger informações reais. Para sistemas reais, utilize algoritmos modernos e amplamente analisados, como AES.
