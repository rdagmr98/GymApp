---
tags: [siel]
---
# SIEL Portable
Riscrittura del gestionale Access in **Flask + SQLite**, pensata per girare da chiavetta sui PC senza Access.
Path: `C:\Users\Gianmarco\Documents\SIEL_Portable` (Python embedded in `python/`).

- DB: `siel.sqlite` accanto all'app, oppure path indicato da env `SIEL_DB` (il launcher gira da cache locale ma scrive nel DB della cartella originale).
- Funzioni ore centesimali ([[Ore Centesimali]]) registrate in SQLite → query di [[Derivazione Ore Parte|derivazione]] identiche all'Access.
- 40 route = tutte le maschere/report ([[Maschere e Report Access]]).
- ⚠️ Cartella **gitignorata** (dati militari reali) → nessun push.
- Regola: **una sola istanza alla volta** (più server su DB diversi = numeri incoerenti).

Ruolo: **ripiego** quando non c'è Access. Per il lavoro quotidiano resta primario l'[[Access accdb]].

← [[SIEL]] · [[Maschere e Report Access]] → [[SIEL Web App]] · [[Logica Motori e Scadenze]]
