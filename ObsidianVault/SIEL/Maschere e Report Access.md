---
tags: [siel]
---
# Maschere e Report Access (parità)
L'Access originale ha **31 maschere** e **19 report**. Mappa sulle funzionalità del [[SIEL Portable]] / [[SIEL Web App]] (parità funzionale, non solo dati).

**Maschere → coperte** da: Dashboard, Situazione giornaliera (+ins/mod/canc volo), Gestione velivoli (CRUD), Parti (CRUD + imbarco), Codici (CRUD), Utilità (ente + indirizzi).

**Report → route portable:**
- Situazione velivoli (+ motori [[cerca_motori]] + sottoreport [[Scadenze LIC LOF|scadenze]]) → `/report/situazione`
- Situazione mensile / giornaliera intervallo → `/report/mensile`, `/report/giornaliero`
- Prospetto manutenzione, Elenco matricole, Codici per tipo, LIC/LOF per codice
- **Aggiunti per chiudere la parità (2026-06-20):** Elenco parti velivolo (*stampa parti II*), **Verbale imbarco**, **Verbale sbarco** componente → [[Imbarco Sbarco Parti]]

Gli unici 3 report che mancavano sono stati aggiunti → parità report completa.

← [[SIEL]] · [[Access accdb]] → [[SIEL Portable]] · [[SIEL Web App]] · [[Imbarco Sbarco Parti]]
