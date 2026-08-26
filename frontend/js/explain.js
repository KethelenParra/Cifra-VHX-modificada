/**
 * Modo explicação.
 *
 * Mostra as chaves SOL e TPM, as etapas e as contas letra a letra.
 * A descriptografia só é habilitada depois de uma criptografia nesta sessão.
 */

import { apiRequest } from "./api.js";
import { clearMessage, renderSteps, setMessage, validateText } from "./dom.js";
import { withProcessOverlay } from "./overlay.js";

const ENCRYPT_PROCESS = [
  "Normalizando o texto",
  "Aplicando Vigenère 1 com SOL / LOS",
  "Invertendo blocos de 3 letras",
  "Aplicando Vigenère 2 com TPM / MPT",
];

const DECRYPT_PROCESS = [
  "Desfazendo a Vigenère 2 (TPM / MPT)",
  "Desinvertendo os blocos",
  "Desfazendo a Vigenère 1 (SOL / LOS)",
  "Recompondo o texto original",
];

const state = {
  cipher: "",
};

export function initExplain() {
  const explainPlain = document.getElementById("explainPlain");
  const explainEncryptBtn = document.getElementById("explainEncryptBtn");
  const explainDecryptBtn = document.getElementById("explainDecryptBtn");
  const explainMessage = document.getElementById("explainMessage");
  const explainResults = document.getElementById("explainResults");
  const explainCipherResult = document.getElementById("explainCipherResult");
  const explainRecoveredResult = document.getElementById("explainRecoveredResult");
  const encryptSteps = document.getElementById("encryptSteps");
  const decryptSteps = document.getElementById("decryptSteps");
  const encryptAlphabet = document.getElementById("encryptAlphabet");
  const decryptPlaceholder = document.getElementById("decryptPlaceholder");
  const decryptContent = document.getElementById("decryptContent");

  explainPlain.addEventListener("input", () => {
    explainPlain.value = explainPlain.value.toUpperCase();
  });

  explainEncryptBtn.addEventListener("click", async () => {
    clearMessage(explainMessage);
    const validationError = validateText(explainPlain.value);
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
        work: () => apiRequest("/encrypt", { texto: explainPlain.value }),
      });

      state.cipher = data.texto_saida;
      explainCipherResult.textContent = data.texto_saida;
      encryptAlphabet.textContent = `Alfabeto numérico: ${data.alfabeto}`;
      renderSteps(encryptSteps, data.passos, data);
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

    if (!state.cipher) {
      setMessage(explainMessage, "Execute primeiro a criptografia.");
      return;
    }

    explainDecryptBtn.disabled = true;
    try {
      const data = await withProcessOverlay({
        title: "Descriptografando",
        steps: DECRYPT_PROCESS,
        work: () => apiRequest("/decrypt", { texto: state.cipher }),
      });

      explainRecoveredResult.textContent = data.texto_saida;
      renderSteps(decryptSteps, data.passos, data);
      decryptPlaceholder.classList.add("hidden");
      decryptContent.classList.remove("hidden");
    } catch (error) {
      setMessage(explainMessage, error.message);
    } finally {
      explainDecryptBtn.disabled = false;
    }
  });
}
