/**
 * Overlay de “processando”.
 *
 * Enquanto a API responde, a tela mostra as etapas da operação.
 * A animação e a chamada HTTP correm juntas; o resultado só volta
 * quando as duas terminam.
 */

function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * @param {{ title: string, steps: string[], work: () => Promise<any> }} options
 */
export async function withProcessOverlay({ title, steps, work }) {
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
