/**
 * Modo desafio.
 *
 * Mostra só o texto cifrado. As chaves e as contas não aparecem nesta tela.
 * O texto original some do campo depois de criptografar, para a apresentação
 * em sala não revelar a mensagem.
 *
 * O fluxo do enunciado (copiar e colar): criptografa → copia o cifrado →
 * cola no painel Descriptografar para recuperar o texto claro.
 */

import { apiRequest } from "./api.js";
import { withProcessOverlay } from "./overlay.js";
import { clearMessage, setMessage, toggleInputVisibility, validateText } from "./dom.js";

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

/** Guarda o último cifrado desta sessão, usado só pelo botão Copiar. */
const state = {
  cipher: "",
};

export function initChallenge() {
  const challengePlain = document.getElementById("challengePlain");
  const challengeEncryptBtn = document.getElementById("challengeEncryptBtn");
  const challengeDecryptBtn = document.getElementById("challengeDecryptBtn");
  const challengeCipher = document.getElementById("challengeCipher");
  const challengeCipherPaste = document.getElementById("challengeCipherPaste");
  const challengeRecovered = document.getElementById("challengeRecovered");
  const challengeMessage = document.getElementById("challengeEncryptMessage");
  const challengeDecryptMessage = document.getElementById("challengeDecryptMessage");
  const toggleChallengePlain = document.getElementById("toggleChallengePlain");
  const copyChallengeCipher = document.getElementById("copyChallengeCipher");

  challengePlain.addEventListener("input", () => {
    challengePlain.value = challengePlain.value.toUpperCase();
  });

  challengeCipherPaste.addEventListener("input", () => {
    challengeCipherPaste.value = challengeCipherPaste.value.toUpperCase();
  });

  toggleChallengePlain.addEventListener("click", () => {
    toggleInputVisibility(challengePlain, toggleChallengePlain);
  });

  challengeEncryptBtn.addEventListener("click", async () => {
    clearMessage(challengeMessage);
    clearMessage(challengeDecryptMessage);
    challengeRecovered.textContent = "—";

    const text = challengePlain.value;
    const validationError = validateText(text);
    if (validationError) {
      setMessage(challengeMessage, validationError);
      return;
    }

    challengeEncryptBtn.disabled = true;
    try {
      const data = await withProcessOverlay({
        title: "Criptografando",
        steps: CHALLENGE_ENCRYPT_PROCESS,
        work: () => apiRequest("/encrypt", { texto: text }),
      });

      state.cipher = data.texto_saida;
      challengeCipher.textContent = data.texto_saida;
      copyChallengeCipher.disabled = false;
      challengePlain.value = "";

      setMessage(
        challengeMessage,
        "Criptografia concluída. Copie o texto cifrado e cole em Descriptografar.",
        "success"
      );
    } catch (error) {
      setMessage(challengeMessage, error.message);
    } finally {
      challengeEncryptBtn.disabled = false;
    }
  });

  challengeDecryptBtn.addEventListener("click", async () => {
    clearMessage(challengeDecryptMessage);

    const pasted = challengeCipherPaste.value;
    const validationError = validateText(pasted);
    if (validationError) {
      setMessage(challengeDecryptMessage, validationError);
      return;
    }

    challengeDecryptBtn.disabled = true;
    try {
      const data = await withProcessOverlay({
        title: "Descriptografando",
        steps: CHALLENGE_DECRYPT_PROCESS,
        work: () => apiRequest("/decrypt", { texto: pasted }),
      });

      challengeRecovered.textContent = data.texto_saida;
    } catch (error) {
      setMessage(challengeDecryptMessage, error.message);
    } finally {
      challengeDecryptBtn.disabled = false;
    }
  });

  copyChallengeCipher.addEventListener("click", async () => {
    if (!state.cipher) return;

    try {
      await navigator.clipboard.writeText(state.cipher);
      copyChallengeCipher.textContent = "Copiado";
      setTimeout(() => {
        copyChallengeCipher.textContent = "Copiar";
      }, 1200);
    } catch {
      setMessage(challengeMessage, "Não foi possível copiar automaticamente.");
    }
  });
}
