/**
 * Troca entre modo desafio e modo explicação.
 *
 * Atualiza as abas, o título da página e o rodapé (autoria do trabalho).
 */

export function initModeSwitch() {
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

    headerTitle.textContent = isExplain ? "Cifra Criptografia" : "Desafio de criptografia";
    headerKicker.textContent = isExplain
      ? "Criptografia simétrica · projeto acadêmico"
      : "Projeto acadêmico · tente descobrir a mensagem";
    document.title = isExplain ? "Cifra Criptografia" : "Desafio de criptografia";
    pageFooter.textContent = isExplain
      ? "Cifra Criptografia · projeto acadêmico de criptografia simétrica · Kethelen Parra e Gisele Veloso"
      : "Projeto acadêmico de criptografia simétrica · Kethelen Parra e Gisele Veloso";
  }

  challengeTab.addEventListener("click", () => setAppMode("challenge"));
  explainTab.addEventListener("click", () => setAppMode("explain"));
}
