/**
 * Tema claro / escuro.
 *
 * A preferência fica em localStorage para sobreviver ao recarregar a página.
 */

const THEME_KEY = "vhx-theme";

function currentTheme() {
  return document.documentElement.getAttribute("data-theme") || "light";
}

export function applyTheme(theme, toggle) {
  const next = theme === "dark" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem(THEME_KEY, next);
  toggle.textContent = next === "light" ? "Modo escuro" : "Modo claro";
  toggle.setAttribute("aria-pressed", String(next === "dark"));
}

export function initTheme() {
  const themeToggle = document.getElementById("themeToggle");
  applyTheme(localStorage.getItem(THEME_KEY) || "light", themeToggle);
  themeToggle.addEventListener("click", () => {
    applyTheme(currentTheme() === "light" ? "dark" : "light", themeToggle);
  });
}
