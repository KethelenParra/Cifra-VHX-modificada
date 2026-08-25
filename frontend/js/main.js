/**
 * Ponto de entrada do frontend.
 *
 * Liga, nesta ordem: tema, troca de modo, tela de desafio e tela de explicação.
 */

import { initChallenge } from "./challenge.js";
import { initExplain } from "./explain.js";
import { initModeSwitch } from "./mode.js";
import { initTheme } from "./theme.js";

initTheme();
initModeSwitch();
initChallenge();
initExplain();
