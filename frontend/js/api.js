const API_BASE = "/api";

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
