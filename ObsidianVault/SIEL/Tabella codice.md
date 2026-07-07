---
tags: [siel]
---
# Tabella codice
Catalogo dei componenti per tipo di velivolo. Chiave: **(id, tipo_vlv)** → `Parte` (denominazione).
È l'anagrafica che dà un nome alle posizioni delle [[Imbarco Sbarco Parti|parti]] imbarcate.

- `id = 1`, `id = 2` → posizioni **motore** (usate da [[cerca_motori]]).
- altri `id` → altri particolari soggetti a [[Scadenze LIC LOF]].
- `tipo_vlv` lega il codice al tipo di elicottero ([[Parco Elicotteri]]).

Sottigliezza: alcune righe esistono con `Parte = NULL` (es. la posizione motore 2 dei monomotore) → vanno trattate come "non esiste un secondo motore", non come motore a 0 ore.

Gestione nel portable: pagina **Codici** (CRUD) e report **Codici per tipo**.

← [[SIEL]] · [[Derivazione Ore Parte]] → [[cerca_motori]] · [[Parco Elicotteri]]
