# Cifra VHX

Projeto acadêmico de criptografia simétrica: Vigenère com chave alternada, inversão de blocos e cifra de Hill.

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
    service/          # regra da cifra (Vigenère, blocos, Hill)
  frontend/
    index.html
    css/
    js/
```

A chave **não é digitada na tela**. Ela fica fixa no backend: `SOL`.

## Fluxo da criptografia

```text
TEXTO
 ↓
Vigenère com chave normal / invertida
 ↓
Dividir em blocos de 3
 ↓
Inverter cada bloco
 ↓
Dividir em pares (acrescentar X se for ímpar)
 ↓
Hill
 ↓
TEXTO CIFRADO
```

1. Normaliza o texto para `A-Z`.
2. Monta a chave no tamanho da mensagem: `SOL`, depois `LOS`, depois `SOL`...
3. Aplica Vigenère: `C = (P + K) mod 26`.
4. Divide em blocos de 3 e inverte cada bloco.
5. Se o comprimento for ímpar, acrescenta `X`.
6. Divide em pares e aplica Hill com a matriz:

```text
[ 3 3 ]
[ 2 5 ]
```

Exemplo com `DADOS`:

```text
DADOS
chave SOLLO
Vigenère → VOOZG
blocos   → VOO | ZG
inversão → OOV | GZ
padding  → OOVGZX
pares    → OO | VG | ZX
Hill     → GU | DU | OJ

Resultado: GUDUOJ
```

A descriptografia faz o caminho inverso: Hill inversa, tira o `X` se existir, desfaz a inversão dos blocos e aplica `P = (C - K) mod 26`.

## Modos do frontend

### Modo desafio

Mostra só o texto secreto e o resultado. Não revela a chave nem as etapas.

### Modo explicação

Mostra a chave `SOL`, a montagem `SOL / LOS`, as contas da Vigenère, a inversão dos blocos e a Hill letra a letra.

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
  "texto": "DADOS"
}
```

## Observação acadêmica

A VHX é uma cifra de demonstração. Não use para proteger dados reais; em sistemas reais, use algoritmos como AES.
