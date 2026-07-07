---
tags: [siel]
---
# SIEL Web App
Versione web statica per accesso da browser/mobile. **Live:** https://rdagmr98.github.io/siel/
SPA hash-router in `app.js` (~23 route = tutte le maschere/report, [[Maschere e Report Access]]).

Architettura **dati separati dal codice** (vincolo militare):
- repo **pubblico** `rdagmr98/siel` = solo guscio codice, **zero dati** (deploy via `pages.yml`);
- repo **privato** `rdagmr98/siel-data` = un JSON per tabella;
- accesso via GitHub Contents API col **PAT personale in localStorage** (mai nel codice); scritture = commit del JSON.

Logica fedele all'Access: stesse [[Derivazione Ore Parte|derivazioni]] e [[cerca_motori|motori]] (smoke-test round-trip volo PASS).

⚠️ Manca un solo passo: la default branch di `siel-data` è **vuota** → finché non si pushano i JSON (dati reali ⇒ **solo con OK esplicito**) l'app online carica vuoto.

← [[SIEL]] · [[SIEL Portable]] → [[Maschere e Report Access]]
