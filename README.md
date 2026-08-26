# Cifra VHX Dupla

Projeto acadêmico de criptografia simétrica: duas Vigenères com chaves
diferentes e inversão de blocos no meio.

## Tecnologias

- Backend: Python, FastAPI, Uvicorn
- Frontend: HTML, CSS e JavaScript puro, em módulos

## Arquitetura

```text
vhx_project/
  backend/
    main.py           # sobe a API e o site
    api/              # rotas HTTP
    model/            # formatos de entrada e saída
    service/          # regra da cifra (Vigenère, blocos, derivação da 2ª chave)
  frontend/
    index.html
    css/
    js/
```

As chaves **não são digitadas na tela**. Ficam fixas no backend:

- 1ª chave: `SOL` (alterna com `LOS`)
- 2ª chave: `TPM`, derivada da primeira avançando cada letra 1 posição
  (`S→T`, `O→P`, `L→M`), e alterna com `MPT`

## Fluxo da criptografia

```text
TEXTO
 ↓
Vigenère 1
 ↓
Inverter blocos
 ↓
Vigenère 2
 ↓
TEXTO CIFRADO
```

1. Normaliza o texto para `A-Z`.
2. Monta a 1ª chave no tamanho da mensagem: `SOL`, depois `LOS`, depois `SOL`...
3. Aplica Vigenère 1: `C = (P + K) mod 26`.
4. Divide em blocos de 3 e inverte cada bloco.
5. Monta a 2ª chave: `TPM`, depois `MPT`, depois `TPM`...
6. Aplica Vigenère 2: de novo `C = (P + K) mod 26`.

A VHX Dupla combina duas famílias clássicas: a Vigenère é uma
**substituição** (troca o valor de cada letra) e a inversão de blocos é
uma **transposição** (muda a ordem das letras, sem mudar o valor delas).
Como as duas Vigenères usam chaves diferentes, quem aplicar só a Vigenère
clássica não recupera a palavra original.

Exemplo com `ATAQUE`:

```text
ATAQUE
1ª chave     SOLLOS
Vigenère 1 → SHLBIW
blocos       SHL | BIW
inversão     LHS | WIB
2ª chave     TPMMPT
Vigenère 2 → EWEIXU

Resultado: EWEIXU
```

A descriptografia faz o caminho inverso: Vigenère 2 inversa com `TPM / MPT`,
desfaz a inversão dos blocos e aplica a Vigenère 1 inversa com `SOL / LOS`
(`P = (C - K) mod 26`).

## Modos do frontend

### Modo desafio

Mostra só o texto secreto e o resultado. Não revela as chaves nem as etapas.

### Modo explicação

Mostra as chaves `SOL` e `TPM`, a montagem `SOL / LOS` e `TPM / MPT`, as
contas das duas Vigenères letra a letra e a inversão de cada bloco de 3.

## Como executar

Na pasta do projeto:

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

Abra:

```text
http://127.0.0.1:8000
```

A documentação da API fica em `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /api/health`
- `POST /api/encrypt`
- `POST /api/decrypt`

Exemplo:

```json
{
  "texto": "ATAQUE"
}
```

## Observação acadêmica

A VHX Dupla é uma cifra de demonstração. Não use para proteger dados reais; em sistemas reais, use algoritmos como AES.
