---
tags: [siel]
---
# Access accdb (soluzione primaria)
Il file che funziona **esattamente** come l'originale: `Desktop\SIEL.accdb` (copia di `Documents/siel_convertito/siel.accdb`).
È l'app Access originale **convertita** in formato moderno (.accdb, Office/Access 2016), con TUTTO dentro: 31 maschere, 19 report, 38 query, 6 moduli VBA (incl. `funzioni_ore` → [[Ore Centesimali]]), tabelle locali coi dati. Fedeltà 100% perché **è** l'Access, non una riscrittura.

**Perché "non funzionava":** aperto da cartella non attendibile, Office **disabilita le macro/VBA** → i pulsanti delle [[Maschere e Report Access|maschere]] non fanno nulla. Fix: rendere **attendibile** la cartella (Trusted Location, registro Office 16.0). Helper per i PC di lavoro/chiavetta: `Desktop\ABILITA SIEL su questo PC.bat`.

Alternative (no-Access): [[SIEL Portable]] (USB) e [[SIEL Web App]] (browser).

← [[SIEL]] → [[Maschere e Report Access]] · [[SIEL Portable]] · [[SIEL Web App]]
