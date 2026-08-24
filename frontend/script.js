const API_BASE = "/api";
const THEME_KEY = "vhx-theme";

const CHALLENGE_ENCRYPT_PROCESS = [
  "Preparando o texto",
  "Aplicando a cifra",
  "Gerando o resultado",
];

const CHALLENGE_DECRYPT_PROCESS = [
  "Lendo o texto cifrado",
  "Recuperando a mensagem",
  "Montando o resultado",
];

const ENCRYPT_PROCESS = [
  "Normalizando o texto para A–Z",
  "Dividindo em blocos de 3 letras",
  "Somando cada letra à chave (mod 26)",
  "Invertendo as letras de cada bloco",
];

const DECRYPT_PROCESS = [
  "Separando o texto cifrado em blocos",
  "Desfazendo a inversão de cada bloco",
  "Subtraindo a chave de cada letra (mod 26)",
  "Recompondo o texto original",
];

const state = {
  challenge: {
    cipher: "",
    key: "",
  },
  explain: {
    cipher: "",
    key: "",
  },
};

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function normalizeKeyVisual(input) {
  input.value = input.value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z]/g, "")
    .toUpperCase()
    .slice(0, 3);
}

function normalizeTextVisual(input) {
  input.value = input.value.toUpperCase();
}

function setMessage(element, text, type = "error") {
  element.textContent = text;
  element.classList.remove("hidden", "error", "success");
  element.classList.add(type);
}

function clearMessage(element) {
  element.textContent = "";
  element.classList.add("hidden");
  element.classList.remove("error", "success");
}

function validateInputs(text, key) {
  const normalizedKey = key
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-zA-Z]/g, "");
  const hasLetter = /[a-zA-Z]/.test(
    text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  );

  if (!text.trim()) {
    return "Digite um texto.";
  }
  if (!hasLetter) {
    return "O texto precisa possuir pelo menos uma letra de A a Z.";
  }
  if (normalizedKey.length !== 3) {
    return "A chave deve possuir exatamente 3 letras de A a Z.";
  }
  return null;
}

async function apiRequest(path, body = null) {
  const options = {
    method: body ? "POST" : "GET",
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Ocorreu um erro inesperado.");
  }

  return data;
}

async function generateRandomKey(targetInput) {
  const data = await apiRequest("/random-key");
  targetInput.value = data.key;
}

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") || "light";
}

function applyTheme(theme) {
  const next = theme === "dark" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem(THEME_KEY, next);
  themeToggle.textContent = next === "light" ? "Modo escuro" : "Modo claro";
  themeToggle.setAttribute("aria-pressed", String(next === "dark"));
}

function renderSteps(container, steps) {
  container.innerHTML = "";

  steps.forEach((step) => {
    const article = document.createElement("article");
    article.className = "step-card";

    const title = document.createElement("h4");
    title.textContent = step.title;

    const description = document.createElement("p");
    description.textContent = step.description;

    article.appendChild(title);
    article.appendChild(description);

    if (step.value) {
      const value = document.createElement("div");
      value.className = "step-value";
      value.textContent = step.value;
      article.appendChild(value);
    }

    container.appendChild(article);
  });
}

function renderCalculations(container, data) {
  container.innerHTML = "";
  const isEncrypt = data.operation === "encrypt";

  data.blocks.forEach((block) => {
    const article = document.createElement("article");
    article.className = "calc-block";

    const title = document.createElement("h4");
    title.textContent = `${block.title} · cálculo letra a letra`;

    const meta = document.createElement("p");
    meta.className = "calc-meta";
    meta.innerHTML = isEncrypt
      ? `<span>Texto: <strong>${block.working_block}</strong></span>
         <span>Chave ${block.key_type}: <strong>${block.key_used}</strong></span>
         <span>Vigenère: <strong>${block.after_vigenere}</strong></span>
         <span>Bloco invertido: <strong>${block.after_reverse}</strong></span>`
      : `<span>Bloco cifrado: <strong>${block.input_block}</strong></span>
         <span>Desinvertido: <strong>${block.working_block}</strong></span>
         <span>Chave ${block.key_type}: <strong>${block.key_used}</strong></span>
         <span>Texto recuperado: <strong>${block.after_vigenere}</strong></span>`;

    const wrap = document.createElement("div");
    wrap.className = "calc-table-wrap";

    const table = document.createElement("table");
    table.className = "calc-table";
    table.innerHTML = `
      <thead>
        <tr>
          <th>${isEncrypt ? "P" : "C"}</th>
          <th>Valor</th>
          <th>K</th>
          <th>Valor</th>
          <th>Fórmula</th>
          <th>Conta</th>
          <th>${isEncrypt ? "C" : "P"}</th>
        </tr>
      </thead>
      <tbody>
        ${block.letters
          .map(
            (letter) => `
          <tr>
            <td>${letter.input_letter}</td>
            <td>${letter.input_value}</td>
            <td>${letter.key_letter}</td>
            <td>${letter.key_value}</td>
            <td>${letter.operation}</td>
            <td class="formula">${letter.formula}</td>
            <td>${letter.result_letter} (${letter.result_value})</td>
          </tr>`
          )
          .join("")}
      </tbody>
    `;

    const summary = document.createElement("p");
    summary.className = "calc-summary";
    summary.textContent = block.summary;

    wrap.appendChild(table);
    article.appendChild(title);
    article.appendChild(meta);
    article.appendChild(wrap);
    article.appendChild(summary);
    container.appendChild(article);
  });
}

function toggleInputVisibility(input, button) {
  const hidden = input.type === "password";
  input.type = hidden ? "text" : "password";
  button.textContent = hidden ? "Ocultar" : "Mostrar";
}

async function withProcessOverlay({ title, steps, work }) {
  const overlay = document.getElementById("processOverlay");
  const titleEl = document.getElementById("processTitle");
  const list = document.getElementById("processSteps");

  titleEl.textContent = title;
  list.innerHTML = "";
  steps.forEach((label) => {
    const item = document.createElement("li");
    item.textContent = label;
    list.appendChild(item);
  });

  overlay.classList.remove("hidden");
  overlay.setAttribute("aria-busy", "true");
  document.body.classList.add("is-processing");

  try {
    const workPromise = work();
    const items = [...list.children];

    for (const item of items) {
      item.classList.add("running");
      await wait(340);
      item.classList.remove("running");
      item.classList.add("done");
    }

    const result = await workPromise;
    await wait(160);
    return result;
  } finally {
    overlay.classList.add("hidden");
    overlay.setAttribute("aria-busy", "false");
    document.body.classList.remove("is-processing");
  }
}


const themeToggle = document.getElementById("themeToggle");
applyTheme(localStorage.getItem(THEME_KEY) || "light");
themeToggle.addEventListener("click", () => {
  applyTheme(currentTheme() === "light" ? "dark" : "light");
});


const challengeTab = document.getElementById("challengeTab");
const explainTab = document.getElementById("explainTab");
const challengeMode = document.getElementById("challengeMode");
const explainMode = document.getElementById("explainMode");
const headerTitle = document.getElementById("headerTitle");
const headerKicker = document.getElementById("headerKicker");
const pageFooter = document.getElementById("pageFooter");

function setAppMode(mode) {
  const isExplain = mode === "explain";

  challengeTab.classList.toggle("active", !isExplain);
  explainTab.classList.toggle("active", isExplain);
  challengeMode.classList.toggle("hidden", isExplain);
  explainMode.classList.toggle("hidden", !isExplain);

  headerTitle.textContent = isExplain ? "Cifra VHX" : "Desafio de criptografia";
  headerKicker.textContent = isExplain
    ? "Criptografia simétrica · projeto acadêmico"
    : "Projeto acadêmico · tente descobrir a mensagem";
  document.title = isExplain ? "Cifra VHX" : "Desafio de criptografia";
  pageFooter.textContent = isExplain
    ? "Cifra VHX · projeto acadêmico de criptografia simétrica · Kethelen Parra e Gisele Veloso"
    : "Projeto acadêmico de criptografia simétrica · Kethelen Parra e Gisele Veloso";
}

challengeTab.addEventListener("click", () => setAppMode("challenge"));
explainTab.addEventListener("click", () => setAppMode("explain"));


const challengePlain = document.getElementById("challengePlain");
const challengeKey = document.getElementById("challengeKey");
const challengeEncryptBtn = document.getElementById("challengeEncryptBtn");
const challengeDecryptBtn = document.getElementById("challengeDecryptBtn");
const challengeCipher = document.getElementById("challengeCipher");
const challengeRecovered = document.getElementById("challengeRecovered");
const challengeReveal = document.getElementById("challengeReveal");
const challengeMessage = document.getElementById("challengeEncryptMessage");
const randomChallengeKey = document.getElementById("randomChallengeKey");
const toggleChallengePlain = document.getElementById("toggleChallengePlain");
const toggleChallengeKey = document.getElementById("toggleChallengeKey");
const copyChallengeCipher = document.getElementById("copyChallengeCipher");

challengePlain.addEventListener("input", () => normalizeTextVisual(challengePlain));
challengeKey.addEventListener("input", () => normalizeKeyVisual(challengeKey));

toggleChallengePlain.addEventListener("click", () => {
  toggleInputVisibility(challengePlain, toggleChallengePlain);
});

toggleChallengeKey.addEventListener("click", () => {
  toggleInputVisibility(challengeKey, toggleChallengeKey);
});

randomChallengeKey.addEventListener("click", async () => {
  try {
    await generateRandomKey(challengeKey);
    clearMessage(challengeMessage);
  } catch (error) {
    setMessage(challengeMessage, error.message);
  }
});

challengeEncryptBtn.addEventListener("click", async () => {
  clearMessage(challengeMessage);
  challengeReveal.classList.add("hidden");

  const text = challengePlain.value;
  const key = challengeKey.value;
  const validationError = validateInputs(text, key);
  if (validationError) {
    setMessage(challengeMessage, validationError);
    return;
  }

  challengeEncryptBtn.disabled = true;
  try {
    const data = await withProcessOverlay({
      title: "Criptografando",
      steps: CHALLENGE_ENCRYPT_PROCESS,
      work: () => apiRequest("/encrypt", { text, key }),
    });

    state.challenge.cipher = data.output_text;
    state.challenge.key = data.key;

    challengeCipher.textContent = data.output_text;
    challengeDecryptBtn.disabled = false;
    copyChallengeCipher.disabled = false;

    challengePlain.value = "";
    challengeKey.value = "";

    setMessage(
      challengeMessage,
      "Criptografia concluída. O texto original e a chave foram removidos dos campos visíveis.",
      "success"
    );
  } catch (error) {
    setMessage(challengeMessage, error.message);
  } finally {
    challengeEncryptBtn.disabled = false;
  }
});

challengeDecryptBtn.addEventListener("click", async () => {
  clearMessage(challengeMessage);

  if (!state.challenge.cipher || !state.challenge.key) {
    setMessage(challengeMessage, "Nenhum texto foi criptografado nesta sessão.");
    return;
  }

  challengeDecryptBtn.disabled = true;
  try {
    const data = await withProcessOverlay({
      title: "Descriptografando",
      steps: CHALLENGE_DECRYPT_PROCESS,
      work: () =>
        apiRequest("/decrypt", {
          text: state.challenge.cipher,
          key: state.challenge.key,
        }),
    });

    challengeRecovered.textContent = data.output_text;
    challengeReveal.classList.remove("hidden");
  } catch (error) {
    setMessage(challengeMessage, error.message);
  } finally {
    challengeDecryptBtn.disabled = false;
  }
});

copyChallengeCipher.addEventListener("click", async () => {
  if (!state.challenge.cipher) return;

  try {
    await navigator.clipboard.writeText(state.challenge.cipher);
    copyChallengeCipher.textContent = "Copiado";
    setTimeout(() => {
      copyChallengeCipher.textContent = "Copiar";
    }, 1200);
  } catch {
    setMessage(challengeMessage, "Não foi possível copiar automaticamente.");
  }
});


const explainPlain = document.getElementById("explainPlain");
const explainKey = document.getElementById("explainKey");
const randomExplainKey = document.getElementById("randomExplainKey");
const explainEncryptBtn = document.getElementById("explainEncryptBtn");
const explainDecryptBtn = document.getElementById("explainDecryptBtn");
const explainMessage = document.getElementById("explainMessage");
const explainResults = document.getElementById("explainResults");
const explainCipherResult = document.getElementById("explainCipherResult");
const explainRecoveredResult = document.getElementById("explainRecoveredResult");
const encryptSteps = document.getElementById("encryptSteps");
const decryptSteps = document.getElementById("decryptSteps");
const encryptCalcs = document.getElementById("encryptCalcs");
const decryptCalcs = document.getElementById("decryptCalcs");
const encryptAlphabet = document.getElementById("encryptAlphabet");
const decryptPlaceholder = document.getElementById("decryptPlaceholder");
const decryptContent = document.getElementById("decryptContent");

explainPlain.addEventListener("input", () => normalizeTextVisual(explainPlain));
explainKey.addEventListener("input", () => normalizeKeyVisual(explainKey));

randomExplainKey.addEventListener("click", async () => {
  try {
    await generateRandomKey(explainKey);
    clearMessage(explainMessage);
  } catch (error) {
    setMessage(explainMessage, error.message);
  }
});

explainEncryptBtn.addEventListener("click", async () => {
  clearMessage(explainMessage);
  const validationError = validateInputs(explainPlain.value, explainKey.value);
  if (validationError) {
    setMessage(explainMessage, validationError);
    return;
  }

  decryptContent.classList.add("hidden");
  decryptPlaceholder.classList.remove("hidden");

  explainEncryptBtn.disabled = true;
  try {
    const data = await withProcessOverlay({
      title: "Criptografando",
      steps: ENCRYPT_PROCESS,
      work: () =>
        apiRequest("/encrypt", {
          text: explainPlain.value,
          key: explainKey.value,
        }),
    });

    state.explain.cipher = data.output_text;
    state.explain.key = data.key;

    explainCipherResult.textContent = data.output_text;
    encryptAlphabet.textContent = `Alfabeto numérico: ${data.alphabet}`;
    renderSteps(encryptSteps, data.steps);
    renderCalculations(encryptCalcs, data);

    explainResults.classList.remove("hidden");
    explainResults.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    setMessage(explainMessage, error.message);
  } finally {
    explainEncryptBtn.disabled = false;
  }
});

explainDecryptBtn.addEventListener("click", async () => {
  clearMessage(explainMessage);

  if (!state.explain.cipher || !state.explain.key) {
    setMessage(explainMessage, "Execute primeiro a criptografia.");
    return;
  }

  explainDecryptBtn.disabled = true;
  try {
    const data = await withProcessOverlay({
      title: "Descriptografando",
      steps: DECRYPT_PROCESS,
      work: () =>
        apiRequest("/decrypt", {
          text: state.explain.cipher,
          key: state.explain.key,
        }),
    });

    explainRecoveredResult.textContent = data.output_text;
    renderSteps(decryptSteps, data.steps);
    renderCalculations(decryptCalcs, data);

    decryptPlaceholder.classList.add("hidden");
    decryptContent.classList.remove("hidden");
  } catch (error) {
    setMessage(explainMessage, error.message);
  } finally {
    explainDecryptBtn.disabled = false;
  }
});
