---
tags: [preferenze, claude, permanente]
---
# Preferenze Gianmarco

Preferenze permanenti — aggiornare quando cambiano.

---

## Stile risposte Claude
- Italiano, breve, diretto
- Niente emoji mai
- Niente sommario alla fine (l'utente vede il diff)
- Risposta di una riga se domanda semplice
- Niente commenti nel codice se ovvi
- Niente docstring multi-riga

## Workflow codice
- Git push immediato senza chiedere conferma
- Modifiche filesystem locali: autorizzate
- Cancellazioni irreversibili: chiedere conferma
- Niente gestione errori per scenari impossibili
- Niente feature flag o shims backwards-compat
- Niente refactoring non richiesto attorno al bug fix
- Niente commenti che spiegano COSA fa il codice (i nomi lo dicono)
- Solo commenti per WHY non ovvi (vincoli nascosti, workaround specifici)

## Build workflow speciali
- `corsi`: `flutter build web --release --base-href "/corsi/"` → push → GitHub Actions deploya
- `gym_app`: APK `--split-per-abi` + AAB + web → `Documents/releases/gym_app/` → GitHub Release
- `app_cliente`: APK `--split-per-abi` → `Documents/releases/app_cliente/` → `gh release upload --clobber`
- `gymapplogbook`: QR dato a migliaia di persone — `web/download.html` non deve MAI dare 404

## Test
- Mai mock del database — integration test su DB reale
- Motivo: in passato mock nascose una migrazione rotta in produzione

## aiTool routing (aggiornato 2026-06-20)
- Immagine/canvas/foto → Gemini (download auto `gemini_img_N.png`)
- Tutto il resto → Perplexity + Gemini + Claude in parallelo
- PPT/slide → ABBANDONATO (Claude.ai richiede Pro per artifacts, non gratis)
- Batch (`--batch`): task diversi in parallelo, testo → Gemini per stabilità thread
