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
}
