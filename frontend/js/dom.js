/**
 * Funções de tela reutilizadas pelos dois modos.
 *
 * Mensagens de erro/sucesso, validação do texto, mostrar/ocultar senha
 * e montagem das tabelas pedagógicas (passos e contas).
 */

export function setMessage(element, text, type = "error") {
  element.textContent = text;
  element.classList.remove("hidden", "error", "success");
  element.classList.add(type);
}

export function clearMessage(element) {
  element.textContent = "";
  element.classList.add("hidden");
  element.classList.remove("error", "success");
}

/**
 * Exige pelo menos uma letra A–Z (acentos valem, porque são normalizados).
 * @returns {string|null} mensagem de erro, ou null se estiver ok
 */
export function validateText(text) {
  const hasLetter = /[a-zA-Z]/.test(
    text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  );

  if (!text.trim()) {
    return "Digite um texto.";
  }
  if (!hasLetter) {
    return "O texto precisa possuir pelo menos uma letra de A a Z.";
  }
  return null;
}

export function toggleInputVisibility(input, button) {
  const hidden = input.type === "password";
  input.type = hidden ? "text" : "password";
  button.textContent = hidden ? "Ocultar" : "Mostrar";
}

/** Cartões de cada etapa; a tabela de contas entra dentro do próprio cartão. */
export function renderSteps(container, steps, data = null) {
  container.innerHTML = "";

  steps.forEach((step) => {
    const article = document.createElement("article");
    article.className = "step-card";

    const title = document.createElement("h4");
    title.textContent = step.titulo;

    const description = document.createElement("p");
    description.textContent = step.descricao;

    article.appendChild(title);
    article.appendChild(description);

    if (step.valor) {
      const value = document.createElement("div");
      value.className = "step-value";
      value.textContent = step.valor;
      article.appendChild(value);
    }

    if (data && step.tabela) {
      const calc = calculationFor(step.tabela, data);
      if (calc) {
        article.appendChild(calc);
      }
    }

    container.appendChild(article);
  });
}

function tableFromRows(headers, rows) {
  const wrap = document.createElement("div");
  wrap.className = "calc-table-wrap";

  const table = document.createElement("table");
  table.className = "calc-table";
  table.innerHTML = `
    <thead>
      <tr>${headers.map((header) => `<th>${header}</th>`).join("")}</tr>
    </thead>
    <tbody>
      ${rows
        .map(
          (cells) => `
        <tr>
          ${cells
            .map((cell) => {
              const formulaClass = String(cell).includes("mod 26") ? ' class="formula"' : "";
              return `<td${formulaClass}>${cell}</td>`;
            })
            .join("")}
        </tr>`
        )
        .join("")}
    </tbody>
  `;

  wrap.appendChild(table);
  return wrap;
}

function calcArticle(metaItems, table, summary) {
  const article = document.createElement("article");
  article.className = "calc-block";

  const meta = document.createElement("p");
  meta.className = "calc-meta";
  meta.innerHTML = metaItems
    .map((item) => `<span>${item.label}: <strong>${item.value}</strong></span>`)
    .join("");

  const note = document.createElement("p");
  note.className = "calc-summary";
  note.textContent = summary;

  article.appendChild(meta);
  article.appendChild(table);
  article.appendChild(note);
  return article;
}

function vigenereTable(letras, isEncrypt) {
  return tableFromRows(
    [
      isEncrypt ? "P" : "C",
      "Valor",
      "K",
      "Valor",
      "Fórmula",
      "Conta",
      isEncrypt ? "C" : "P",
    ],
    letras.map((letra) => [
      letra.letra,
      letra.valor,
      letra.letra_chave,
      letra.valor_chave,
      letra.operacao,
      letra.conta,
      `${letra.letra_resultado} (${letra.valor_resultado})`,
    ])
  );
}

function vigenereBlock({ texto, chave, resultado, letras, isEncrypt, summary }) {
  return calcArticle(
    [
      { label: "Texto", value: texto },
      { label: "Chave montada", value: chave },
      { label: "Resultado", value: resultado },
    ],
    vigenereTable(letras, isEncrypt),
    summary
  );
}

function calculationFor(kind, data) {
  const isEncrypt = data.operacao === "criptografar";

  if (kind === "vigenere_1") {
    return vigenereBlock({
      texto: isEncrypt ? data.texto_normalizado : data.depois_blocos,
      chave: data.chave_montada,
      resultado: isEncrypt ? data.depois_vigenere : data.texto_saida,
      letras: data.letras_vigenere,
      isEncrypt,
      summary: isEncrypt
        ? `${data.texto_normalizado} com chave ${data.chave_montada} resulta em ${data.depois_vigenere}.`
        : `${data.depois_blocos} menos a chave ${data.chave_montada} recupera ${data.texto_saida}.`,
    });
  }

  if (kind === "vigenere_2") {
    return vigenereBlock({
      texto: isEncrypt ? data.depois_blocos : data.texto_normalizado,
      chave: data.chave_montada_2,
      resultado: data.depois_vigenere_2,
      letras: data.letras_vigenere_2,
      isEncrypt,
      summary: isEncrypt
        ? `${data.depois_blocos} com chave ${data.chave_montada_2} resulta em ${data.depois_vigenere_2}.`
        : `${data.texto_normalizado} menos a chave ${data.chave_montada_2} resulta em ${data.depois_vigenere_2}.`,
    });
  }

  if (kind === "blocos") {
    return calcArticle(
      [
        { label: "Antes", value: isEncrypt ? data.depois_vigenere : data.depois_vigenere_2 },
        { label: "Depois", value: data.depois_blocos },
      ],
      tableFromRows(
        ["Bloco", "Antes", "Depois da inversão"],
        data.blocos.map((bloco) => [bloco.titulo, bloco.bloco, bloco.bloco_invertido])
      ),
      data.blocos.map((bloco) => bloco.resumo).join(" · ")
    );
  }

  return null;
}
