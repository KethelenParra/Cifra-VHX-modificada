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

/** Cartões resumidos de cada etapa (normalização, Vigenère, blocos, Hill). */
export function renderSteps(container, steps) {
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

function calcArticle(title, metaItems, table, summary) {
  const article = document.createElement("article");
  article.className = "calc-block";

  const heading = document.createElement("h4");
  heading.textContent = title;

  const meta = document.createElement("p");
  meta.className = "calc-meta";
  meta.innerHTML = metaItems
    .map((item) => `<span>${item.label}: <strong>${item.value}</strong></span>`)
    .join("");

  const note = document.createElement("p");
  note.className = "calc-summary";
  note.textContent = summary;

  article.appendChild(heading);
  article.appendChild(meta);
  article.appendChild(table);
  article.appendChild(note);
  return article;
}

/** Três tabelas: Vigenère letra a letra, inversão dos blocos e Hill nos pares. */
export function renderCalculations(container, data) {
  container.innerHTML = "";
  const isEncrypt = data.operacao === "criptografar";

  const vigenere = calcArticle(
    isEncrypt ? "Vigenère letra a letra" : "Vigenère inversa letra a letra",
    [
      { label: "Texto", value: isEncrypt ? data.texto_normalizado : data.depois_vigenere },
      { label: "Chave montada", value: data.chave_montada },
      { label: "Resultado", value: isEncrypt ? data.depois_vigenere : data.texto_saida },
    ],
    tableFromRows(
      [
        isEncrypt ? "P" : "C",
        "Valor",
        "K",
        "Valor",
        "Fórmula",
        "Conta",
        isEncrypt ? "C" : "P",
      ],
      data.letras_vigenere.map((letra) => [
        letra.letra,
        letra.valor,
        letra.letra_chave,
        letra.valor_chave,
        letra.operacao,
        letra.conta,
        `${letra.letra_resultado} (${letra.valor_resultado})`,
      ])
    ),
    isEncrypt
      ? `${data.texto_normalizado} com chave ${data.chave_montada} resulta em ${data.depois_vigenere}.`
      : `${data.depois_vigenere} menos a chave ${data.chave_montada} recupera ${data.texto_saida}.`
  );
  container.appendChild(vigenere);

  const blocksTable = tableFromRows(
    ["Bloco", "Antes", "Depois da inversão"],
    data.blocos.map((bloco) => [bloco.titulo, bloco.bloco, bloco.bloco_invertido])
  );
  container.appendChild(
    calcArticle(
      "Inversão dos blocos de 3",
      [
        { label: "Antes", value: isEncrypt ? data.depois_vigenere : data.depois_blocos },
        { label: "Depois", value: isEncrypt ? data.depois_blocos : data.depois_vigenere },
      ],
      blocksTable,
      data.blocos.map((bloco) => bloco.resumo).join(" · ")
    )
  );

  const hill = calcArticle(
    isEncrypt ? "Cifra de Hill nos pares" : "Hill inversa nos pares",
    [
      { label: "Matriz", value: data.matriz_hill },
      { label: "Entrada", value: isEncrypt ? data.texto_com_x : data.texto_normalizado },
      { label: "Saída", value: isEncrypt ? data.texto_saida : data.texto_com_x },
    ],
    tableFromRows(
      ["Par", "Letras", "Valores", "1ª linha", "2ª linha", "Resultado"],
      data.pares_hill.map((par) => [
        String(par.indice),
        par.par,
        `${par.valor_esq}, ${par.valor_dir}`,
        par.conta_linha1,
        par.conta_linha2,
        par.par_resultado,
      ])
    ),
    data.usou_x
      ? isEncrypt
        ? `Como havia número ímpar de letras, foi acrescentado X: ${data.depois_blocos} → ${data.texto_com_x}.`
        : `O X de preenchimento foi removido: ${data.texto_com_x} → ${data.depois_blocos}.`
      : data.pares_hill.map((par) => par.resumo).join(" · ")
  );
  container.appendChild(hill);
}
