/**
 * Modo desafio.
 *
 * Mostra só o texto cifrado. A chave e as contas não aparecem nesta tela.
 * O texto original some do campo depois de criptografar, para a apresentação
 * em sala não revelar a mensagem.
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

/** Guarda o último cifrado desta sessão (não fica visível no campo de entrada). */
const state = {
  cipher: "",
};

export function initChallenge() {
  const challengePlain = document.getElementById("challengePlain");
  const challengeEncryptBtn = document.getElementById("challengeEncryptBtn");
  const challengeDecryptBtn = document.getElementById("challengeDecryptBtn");
  const challengeCipher = document.getElementById("challengeCipher");
  const challengeRecovered = document.getElementById("challengeRecovered");
  const challengeReveal = document.getElementById("challengeReveal");
  const challengeMessage = document.getElementById("challengeEncryptMessage");
  const toggleChallengePlain = document.getElementById("toggleChallengePlain");
  const copyChallengeCipher = document.getElementById("copyChallengeCipher");

  challengePlain.addEventListener("input", () => {
    challengePlain.value = challengePlain.value.toUpperCase();
  });

  toggleChallengePlain.addEventListener("click", () => {
    toggleInputVisibility(challengePlain, toggleChallengePlain);
  });

  challengeEncryptBtn.addEventListener("click", async () => {
    clearMessage(challengeMessage);
    challengeReveal.classList.add("hidden");

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
      challengeDecryptBtn.disabled = false;
      copyChallengeCipher.disabled = false;
      challengePlain.value = "";

      setMessage(
        challengeMessage,
        "Criptografia concluída. O texto original foi removido do campo visível.",
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

    if (!state.cipher) {
      setMessage(challengeMessage, "Nenhum texto foi criptografado nesta sessão.");
      return;
    }

    challengeDecryptBtn.disabled = true;
    try {
      const data = await withProcessOverlay({
        title: "Descriptografando",
        steps: CHALLENGE_DECRYPT_PROCESS,
        work: () => apiRequest("/decrypt", { texto: state.cipher }),
      });

      challengeRecovered.textContent = data.texto_saida;
      challengeReveal.classList.remove("hidden");
    } catch (error) {
      setMessage(challengeMessage, error.message);
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
