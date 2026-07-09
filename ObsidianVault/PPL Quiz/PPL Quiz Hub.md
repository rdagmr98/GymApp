---
tags: [progetto, flutter, hub, ppl, aviazione]
---
# PPL Quiz — Hub

App per allenarsi all'**esame teorico PPL(A)** (licenza di pilota privato). Veloce: tocchi la risposta e vedi subito **verde** se giusta (avanza da sola dopo ~0,5s) o **rossa** se sbagliata, indicando quella corretta. Nessun "invia / sei sicuro?". Nata perché quizppl online è lento e scomodo (devi inviare ogni risposta per la correzione).

## Coordinate
| Cosa | Valore |
|------|--------|
| Path locale | `C:\Users\Gianmarco\ppl` |
| Repo | `github.com/rdagmr98/ppl` (branch `main`) |
| Web live | https://rdagmr98.github.io/ppl/ |
| APK (release) | `C:\Users\Gianmarco\Documents\releases\ppl\` — `ppl-v1.1.0-arm64-v8a.apk` (15,0 MB, telefoni moderni 64-bit), `ppl-v1.1.0-armeabi-v7a.apk` (12,5 MB, telefoni vecchi 32-bit) |
| Versione | `1.2.0+3` (era `1.0.0+1` → `1.1.0+2` → `1.2.0+3`) |
| Stack | Flutter 3.38.5 / Dart 3.10.4 / Java 17 |

## Database quesiti
- **2273 quesiti** del pool ufficiale ENAC/EASA PPL(A), 10 materie (era 1384, **+889** il 28/06).
- Fonti: scraping iniziale di `tastoeffeuno.it` (1384) + **harvest per-materia da `quizvds.it`** (28/06) che ha aggiunto 889 nuovi quesiti e corretto gli accenti di altri 1163.
- Bundled come asset: `assets/ppl_quiz.json` (UTF-8 pulito, **0 mojibake**, 1592 quesiti con accenti veri à è é ì ò ù).
- Distribuzione per materia (PARTE) dopo il merge: P1=267, P2=220, P3=230, P4=122, P5=315, P6=289, P7=293, P8=170, P9=158, P10=209.
- Sorgente quesito tracciata nel campo `src` (`quizvds` per quelli aggiunti/corretti).
- **Fix testo OCR/scraping (03/07)**: corretti ~130 errori nel testo dei quesiti — pattern I/l confuse (`l-ABCD`→`I-ABCD`, 63 occorrenze), `rn`→`m` (intemazionale→internazionale, attomo→attorno, alternate, pattern, tum→turn), `i`→`dl`/`di` (32x; in/Hg), refusi radiotelefonia EN (temporarily, probability, surveillance, reselecting, instructions, transmitting, wicken, apache, five). Zero residui verificati via scan automatico. Commit `77a152a`.

### Harvest quizvds (28/06)
- `quizvds.it` è CakePHP: pagine esame per-materia sotto `/it-it/esame/ppl/<slug>` (mapping 1:1 slug↔materia). Form `manda_form`, niente CSRF.
- Trucco: si fa **POST con risposte qualunque** e la pagina di **correzione gratuita** rivela TUTTE le risposte corrette (`<tr class="success">`). Nessun login.
- Harvester per-materia (`qv_harvest.py`, nello scratchpad): GET pagina → POST → parse correzione → dedup globale **accent-insensitive** (NFKD + strip combining + lowercase alfanumerico), satura quando una materia smette di dare nuovi. 2052 unici raccolti.
- Merge (`merge_db.py`): PASS 1 sostituisce i quesiti esistenti che combaciano con la versione UTF-8 pulita di quizvds (fix accenti); PASS 2 aggiunge i non-combacianti alla materia giusta. Backup pre-merge salvato (non nel repo, c'è già nella history git).

### Le 10 materie
1. Regolamentazione Aeronautica · 2. Nozioni generali sugli Aeromobili · 3. Prestazioni di volo e pianificazione · 4. Prestazioni e limitazioni umane · 5. Meteorologia · 6. Navigazione · 7. Procedure operative · 8. Principi del volo · 9. Comunicazioni (italiano) · 10. Comunicazioni in inglese.

## Modalità
| Modalità | Quesiti | Note |
|----------|---------|------|
| Esame completo | 132 | distribuzione ufficiale ENAC per materia |
| Esame + fonia inglese | 152 | 132 + 20 di comunicazioni EN (P10) |
| Allenamento rapido | 30 | casuali su tutte le materie |
| Studio per materia | scelta utente | scegli materia + 10/20/40/tutte |

- Distribuzione esame (`examDistribution`): P1=20, P2=12, P3=12, P4=12, P5=20, P6=20, P7=12, P8=12, P9=12 → 132. +20 EN.
- **Soglia 75% per materia** per essere PROMOSSO. A fine prova: punteggio totale, dettaglio per materia con barre, revisione degli errori.

## UX (il punto centrale della richiesta)
- Tap risposta → se **giusta**: verde + HapticFeedback leggero + auto-avanza dopo 480 ms. Se **sbagliata**: rosso + mostra la corretta in verde + haptic forte; resta finché l'utente tocca (ovunque, o bottone "CONTINUA").
- Nessuna conferma, nessun "invia risposta".
- Tema scuro Material3, seed `#1E88E5`, sfondo `#0E1116`.

## Icona app (28/06)
- Generata in locale con **Pillow** (`tool/make_icon.py`, supersampling 2x): aereo top-down bianco su **anello di prua blu** (#1E88E5) con tacche N/E/S/W e **arco verde** (#26C478, richiamo "risposta corretta"), sfondo gradiente navy.
- Sorgenti: `assets/icon/icon.png` (1024 full-bleed) + `assets/icon/icon_foreground.png` (trasparente, per adaptive Android).
- Applicata via `flutter_launcher_icons 0.14.4`: **web** (favicon, `manifest.json`, maskable 192/512) + **Android** (adaptive `mipmap-anydpi-v26/ic_launcher.xml` + `drawable-*/ic_launcher_foreground.png` + `colors.xml` bg #0E1116 + mipmap legacy).
- ComfyUI locale scartato: nessun modello GGUF installato; l'icona vettoriale Pillow è comunque più adatta per un launcher icon.

## Architettura codice (`lib/`)
| File | Ruolo |
|------|-------|
| `models.dart` | `Question`, `Subject`, `QuizDb` (+ `QuizDb.load()` da rootBundle), costanti (`examDistribution`, `subjectNames`, `passThreshold=0.75`) |
| `builder.dart` | `buildExam(withEnglish)`, `buildStudy(subject,limit)`, `buildMixed(count)`, `AnsweredQuestion` |
| `quiz_screen.dart` | UI core del quiz veloce (tap→verde/rosso, auto-advance, `_OptionCard`); a fine tentativo chiama `StatsService.record(...)` |
| `results_screen.dart` | esito PROMOSSO/NON PROMOSSO, score per materia, revisione errori |
| `main.dart` | `HomeScreen` FutureBuilder<QuizDb>, 5 card modalità (+ Statistiche), `SubjectPickerScreen` |
| `stats_service.dart` | `QuizAttempt` (timestamp, titolo, isExam, perSubject) + `StatsService` (persistenza `shared_preferences`, chiave `quiz_attempts_v1`, cap 300 tentativi) |
| `stats_screen.dart` | `StatsScreen`: verdetto prontezza (pronto/quasi pronto/da migliorare, soglia 75%), bar chart per materia, trend line nel tempo, donut corrette/errate — libreria `fl_chart 1.2.0` |

## Deploy
- **Web**: `.github/workflows/deploy.yml` — push su `main` → `flutter build web --release --base-href "/ppl/"` → `peaceiris/actions-gh-pages` (`force_orphan`) su branch `gh-pages`.
- **GitHub Pages**: configurato `build_type=legacy` (sorgente = branch `gh-pages`), non workflow-artifact.
- **APK**: `flutter build apk --split-per-abi --release` → copia in `Documents\releases\ppl\`.

## Scraper (one-shot, non nel repo)
- Script `scrape2.ps1` (vissuto nello scratchpad di sessione) che ha prodotto il dataset.
- Logica: enumera **finestre di 10 ID globali** da 1; POST a `genera_parte_correttore.asp` con `-SkipHttpErrorCheck` (legge il body anche su HTTP 500); decodifica **windows-1252**; parsa i blocchi `boxquesito`; bucket per prefisso reale `"materia.numero"`; **dedup per ID globale**; stop quando una finestra rende 0 domande.

## Bug risolti (per non ripeterli)
- **Dati mal-etichettati (primo scraper)**: il parametro `PARTE` dell'URL è **ignorato** dal sito e gli ID sono **globali sequenziali** (non per-PARTE). Il primo scraper bucketava per PARTE richiesta → ~4000 "quesiti" duplicati nelle materie sbagliate. Fix: bucket per prefisso reale `P.q` + dedup per ID globale → 1384 corretti.
- **Falso negativo sul MAX ID**: un POST con singolo ID a fine DB rende la domanda ma poi lancia ADODB EOF (HTTP 500) → veniva scartato. Fix: finestre di 10 + `-SkipHttpErrorCheck`.
- **MSYS path conversion**: in Bash `--base-href "/ppl/"` diventa `C:/Program Files/Git/ppl/`. Usare il tool **PowerShell** per i build Flutter.
- **GitHub Pages 404**: era `build_type=workflow` (Pages aspettava un artifact Actions). Fix: `gh api -X PUT .../pages -f build_type=legacy -f "source[branch]=gh-pages"` poi `POST .../pages/builds`. Live HTTP 200.
- **GitHub Release v1.0.0 NEGATA** dal classifier auto (l'utente aveva chiesto APK locale + web, non una release pubblica). **Non ritentare** senza richiesta esplicita; consegnato l'APK via path locale.
- **Mojibake accenti (U+FFFD)**: il primo dataset da tastoeffeuno aveva perso à/è/ì/ò/ù (decode windows-1252 sbagliato → carattere irreversibile per-char). Fix 28/06: sostituiti 1163 quesiti con la versione UTF-8 pulita di quizvds → 0 mojibake residui. NB: la console Windows mostra `�` quando stampa à, ma è solo un artefatto di code page del terminale, **non** corruzione dei dati (validator: 0 U+FFFD reali).

## Figure domande + spiegazioni errori (v1.3.0, completato 06-09/07)
- **Figure**: per le domande con immagine (`fig`), scaricata la figura reale della domanda originale (mai generata via AI) e bundlata come asset. Fatto e pushato (commit `20fd76f`).
- **Home page**: rimosse le 2 righe di testo informative sul database in fondo (commit `7e008ed`).
- **Spiegazioni risposte** (richiesta: capire perché si è sbagliato, studiare teoria mentre si fa il quiz, non serve fonte esterna se non disponibile — generate io stesso in quel caso): campo `explanation` per-domanda in `ppl_quiz.json`, già renderizzato da `quiz_screen.dart` (nessuna modifica UI necessaria, era già pronta). **Copertura: 2273/2273 (100%)**.
- **Pattern di lavoro per materia** (ripetuto identico per ogni parte): estrarre le domande della materia in un file compatto (`node -e` inline, un file `subjN_compact.txt` nello scratchpad) → leggerle tutte → scrivere `explN.json` (spiegazioni indicizzate per `gid`) → merge in `assets/ppl_quiz.json` via script `inject_explN.js` (filtra a livello di **subject** con `s.parte !== N`, non `q.parte` — il campo `parte` sta sul subject, non sulla singola domanda) → `flutter analyze` → commit + push.
- **Stato avanzamento — completo**:
  - [x] Parte 1 Regolamentazione (267 q.) — commit `f6e268c`
  - [x] Parte 2 Nozioni generali Aeromobili (220 q.) — commit `c3eb4bb`
  - [x] Parte 3 Prestazioni volo e pianificazione (230 q.) — commit `a29213a`
  - [x] Parte 4 Prestazioni e limitazioni umane (122 q.) — commit `a5aa826`
  - [x] Parte 5 Meteorologia (315 q.) — commit `293eaec`
  - [x] Parte 6 Navigazione (289 q.) — commit `3a5d50f`
  - [x] Parte 7 Procedure operative (293 q.) — commit `8189dd7`
  - [x] Parte 8 Principi del volo (170 q.) — commit `63759bc`
  - [x] Parte 9 Comunicazioni italiano (158 q.) — commit `c7f9241`
  - [x] Parte 10 Comunicazioni inglese (209 q.) — commit `f51f044`
- **Bug qualità dati risolto (09/07)**: le 209 spiegazioni della parte 10 erano state scritte con ASCII invece di accenti italiani corretti (è/à/ì/ò/ù), in violazione della regola permanente sugli accenti — scoperto tramite verifica post-completamento, non era un problema nelle parti 1-9. Root cause: bug pervasivo (111/209 stringhe), non i soli 13 casi rilevati da un primo controllo regex stretto (che non copriva il caso più comune, "e" bare al posto di "è" verbo). Include 2 correzioni di significato, non solo estetiche: "ci si atterra alle istruzioni" (atterrare = to land, sbagliato) → "ci si atterrà alle istruzioni" (attenersi = to abide by, corretto). Fix completo via riscrittura manuale mirata + merge script, verificato con scansione automatica (0 pattern ASCII-accento residui) + `flutter analyze` pulito. Commit `7b9e716`.
- **Nota qualità dati (FYI, non "bug" da correggere)**: il pool mischia domande storiche ENAC/JAR-FCL (gid bassi) e domande EASA/Part-FCL correnti (gid 200000+), a volte con risposta corretta diversa per evoluzione normativa. Caso trovato: gid 10 (vecchia) indica "lampeggiamenti bianchi" come segnale di rientro per atterraggio, mentre lo standard ICAO Annex 2 reale è lampeggiamenti **verdi** — coerente con gid 200006 (nuova) che infatti usa "verde". Non ho toccato l'indice `correct` di nessuna domanda né incrociato i riferimenti nel testo delle spiegazioni: se l'utente nota risposte apparentemente in conflitto tra una domanda vecchia e una nuova sullo stesso argomento, è quasi sempre questo (evoluzione normativa, non errore di battitura).

## Statistiche / prontezza esame (v1.2.0, 03/07)
- Nuova card "Statistiche" in home → `StatsScreen`. Ogni quiz/esame completato viene registrato da `StatsService.record()` (shared_preferences, locale, no backend).
- Verdetto a 3 livelli calcolato su **aggregato cumulativo di tutti i tentativi salvati** (non solo l'ultimo): PRONTO (tutte le materie ≥75%), QUASI PRONTO (overall ≥65%), DA MIGLIORARE (sotto).
- 3 grafici differenziati (`fl_chart 1.2.0`): bar chart per materia (con linea tratteggiata soglia 75%), line chart andamento nel tempo (1 punto per tentativo, solo se >1 tentativo), donut corrette/errate totali. Dettaglio per materia anche in righe testuali con barra di progresso.
- Pulsante cancella storico con conferma (dialog "azione non reversibile").
- **Verifica**: `flutter analyze` pulito (solo 2 lint info preesistenti non correlati), `flutter build web --release` completato senza errori. **Non verificato visivamente in browser** (nessun tool di automazione browser disponibile in questa sessione) — solo verifica di compilazione, non di resa grafica reale.

## TODO / possibili evoluzioni
- [x] Icona app personalizzata (aereo su anello di prua) — fatta 28/06, web + Android.
- [x] Ampliare il pool oltre i 1384 (preoccupazione utente "~4000 EASA") — portato a 2273 via quizvds.
- [x] Correggere errori di testo OCR/scraping nelle domande — fatto 03/07, ~130 fix (commit `77a152a`).
- [x] Salvataggio progressi/statistiche storiche — fatto 03/07, `StatsScreen` + grafici (v1.2.0).
- [ ] Verifica visiva delle statistiche in un browser reale (non fatta in questa sessione, nessun tool disponibile).
- [ ] Modalità "ripassa solo gli errori".
- [ ] Aggiornamento periodico del database (ri-harvest quizvds).
- [ ] (Se l'utente la vuole) GitHub Release con gli APK allegati.

## Collegamenti
- Profilo aviazione utente: vedi [[_CLAUDE]] (militare AVES).
- Sessione di creazione: [[Sessioni/2026-06-28]]. Espansione pool + icona (v1.1.0): [[Sessioni/2026-06-29]]. Fix testo + statistiche (v1.2.0): [[Sessioni/2026-07-03]]. Figure + spiegazioni + fix accenti (v1.3.0): [[Sessioni/2026-07-09]].
