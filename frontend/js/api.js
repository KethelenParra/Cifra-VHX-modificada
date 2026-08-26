/**
 * Cliente HTTP da API VHX Dupla.
 *
 * Todas as chamadas passam por /api. Em caso de erro, o FastAPI devolve
 * { detail: "mensagem" }, que vira uma Exception para a tela tratar.
 */

const API_BASE = "/api";

/**
 * @param {string} path  Caminho após /api, por exemplo "/encrypt"
 * @param {object|null} body  Corpo JSON (POST) ou null (GET)
 * @returns {Promise<object>}
 */
export async function apiRequest(path, body = null) {
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
