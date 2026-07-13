---
tags: [claude, context, master]
---
# Claude Context — Gianmarco
> Leggi questo file SEMPRE per primo. Dà il contesto completo in 30 secondi.
> Aggiornare "Ultime sessioni" a fine di ogni sessione significativa.

---

## Profilo utente
Militare AVES (aviazione esercito), sviluppatore amatoriale. Stack: Flutter (mobile/web), Python (script/automation), HTML+JS (web app leggere). Backend preferito: GitHub JSON (zero hosting). Italiano nativo.

## Regole operative
- Git push immediato dopo ogni modifica — autorizzato senza conferma su tutti i progetti
- Modifiche filesystem locali autorizzate — solo cancellazioni irreversibili richiedono conferma
- Risposte brevi, italiane, niente emoji, niente sommario finale
- Dopo ogni sessione: aggiornare hub progetto + creare `Sessioni/YYYY-MM-DD.md`

## Strumenti disponibili
| Tool | Trigger / Come usarlo |
|------|-----------------------|
| **aiTool** | "usa meno crediti" / "risparmia token" → `ai.bat "prompt"` in `C:\Users\Gianmarco\aiTool\` |
| **ComfyUI MCP** | `mcp__comfyui__generate_image` — immagini locali CPU, Flux Schnell GGUF |
| **Higgsfield MCP** | `mcp__higgsfield__generate_image/video` — immagini/video cloud |
| **Obsidian MCP** | `mcp__obsidian__search-vault` — cerca nel vault |

## Progetti attivi
| Progetto | Path locale | Hub | Nota critica |
|----------|-------------|-----|--------------|
| corsi (EASA Part-66) | `C:\Users\Gianmarco\corsi` | [[AVES Corsi/AVES Hub]] | Flutter web, 4 ruoli, build before push |
| piloti AVES | `C:\Users\Gianmarco\piloti` | [[AVES Corsi/AVES Hub]] | Flutter, JSON GitHub |
| AVES tecnici | `C:\Users\Gianmarco\AVES` | [[AVES Corsi/AVES Hub]] | Flutter, JSON GitHub |
| gym_app | `C:\Users\Gianmarco` (root) | [[Gym App/Gym App]] | Flutter trainer |
| app_coach | `rdagmr98/gymapp-coach` | [[Gym App/Gym App]] | Flutter PT |
| app_cliente / gymapplogbook (stesso repo) | `C:\Users\Gianmarco\fix-ads` → `rdagmr98/gymapplogbook` | [[Gym App/Gym App]] | APK split-per-abi sempre · QR pubblico — NO 404 su `web/download.html` |
| SIEL gestionale | `Documents/SIEL_Portable` | [[SIEL/SIEL]] | Flask+SQLite portable, 1 istanza alla volta |
| SIEL web | `rdagmr98/siel` (privato) | [[SIEL/SIEL]] | SPA statica, dati su siel-data privato |
| buoni pasti | script Python root | [[Buoni Pasti/Pipeline]] | Cartellini/cedolini lavoratori |
| stonks | `C:\Users\Gianmarco\stonks` | [[Stonks/Stonks]] | Portfolio tracker Flutter |
| centri storici | `C:\Users\Gianmarco\Documents\` | [[Centri Storici/Hub]] | DB indirizzi centro storico Italia |
| aiTool | `C:\Users\Gianmarco\aiTool` | [[aiTool/aiTool Hub]] | Browser automation Playwright/Edge CDP |
| PDF Magic Tool | `C:\Users\Gianmarco\Python\pdfconverter.py` | [[PDF Magic Tool]] | Desktop tool PDF: converti/unisci/dividi/comprimi/ruota/password/PDF-A/img |
| CAAE (sito istituzionale) | `C:\Users\Gianmarco\caae` | [[CAAE/CAAE Hub]] | HTML statico GitHub Pages, sito CAAE Viterbo — corsi/flotta/storia/bandiera |
| PPL Quiz | `C:\Users\Gianmarco\ppl` → `rdagmr98/ppl` | [[PPL Quiz/PPL Quiz Hub]] | Flutter mobile+web, quiz teorico pilota privato, DB 2273 q ENAC/EASA, v1.3.0 con figure reali + spiegazioni su tutte le domande + statistiche/grafici, web https://rdagmr98.github.io/ppl/ |

## Ultime sessioni
_Solo ultimi 3 giorni. Storico completo: `Sessioni/YYYY-MM-DD.md` (una per giorno) + cronologia git di questo file._
- [[Sessioni/2026-07-13]] — **Corsi (AVES)**: utente segnala 5 richieste in un messaggio + xlsx allegato. Fix filtro assenze "da recuperare" frequentatore, evidenza corsi multipli per istruttore in agenda, vincolo doppia prenotazione istruttore stessa ora (eccetto stessa lezione/task con somma frequentatori ≤28 teoria/≤15 pratica), ID task pratico nelle assenze — commit `ac4210b`. Risolto anche audit currency gonfiata: root cause in 79 voci di bulk-import "Ore insegnamento NBTC" (2026-06-06) che duplicavano ore lezioni a calendario — escluse in `GradeService.isBulkImportArtifact`, commit `4fad288`. Da `F-2-4 Programma settimanale Cat C.xlsx`: nuove ore da accreditare Niespolo 28h (M10)/Signore 22h (M9), corso Cat.C MTOE-F-2-4 — crediting bloccato da vincolo PII, richiede l'utente via admin→Currency→"Aggiorna ore" (in coda con Minissi/Mirto di sessione 26). Hub [[AVES Corsi/AVES Hub]]. — **Gym App**: filtri corpo libero/manubri/bilanciere nell'archivio esercizi di gym_app e app_pt (`exerciseEquipment()`, euristica su nome, nessun campo equipment nei dati sorgente) — commit `e82be80`/`f1afab3`. Audit richiesto dall'utente ha trovato bug reale in app_pt: `category != 'altro'` escludeva 362/1213 esercizi + archivio non includeva mai `kExerciseCatalog` (62 voci) — entrambi fix, ora ~1275 esercizi visibili in entrambe le app. gym_app v1.0.2+31 in release (APK+AAB+web). Hub [[Gym App/Gym App]].
- [[Sessioni/2026-07-11]] — **Materiale Didattico CAAE**: chiuso il bug quiz non conforme aperto ieri — completati i fix su **51.1, 53.1, 53.2** (32 domande stringa-aperta → tuple 3-alternative), portando il totale a **91/91 domande corrette su 7/23 sottomoduli** (1.1/1.2/1.3/50.1 ieri + questi 3 oggi). Verifica finale con `check_quiz_format.py` su tutto `build.CONTENT`: **0/23 sottomoduli non conformi**. Risolta anche la decisione pendente sul **Modulo 3 (Electrical Fundamentals)**: il syllabus combinato `Documents\BTC\btc\02 - SYLLABUS_EI_B1_Combinato...pdf` conferma 3.13-3.18 come contenuto ufficiale reale (non un'invenzione) — si scrive il Modulo 3 per intero (3.1-3.18, 90h+20h*), nessuna domanda pendente. Aggiornate le note vault che riportavano ancora "decisione aperta" ([[CAAE/Materiale Didattico]], [[CAAE/Programmi Ufficiali — Argomenti per Sottomodulo]]). Avviato il Modulo 2 (Physics): **content_2_1** (Matter), **content_2_2** (Mechanics — 6 sezioni, 13 figure, 52 termini, 24 domande) e **content_2_3** (Thermodynamics — 6 sezioni, 11 figure tutte pre-verificate singolarmente sia a esecuzione sia visivamente, 49 termini, 24 domande) scritti e verificati (build PDF + QA visivo ancora da fare, task #54, **bloccato tecnicamente** finché non esistono anche 2.4/2.5 — dict `CONTENT` di `build.py` valutato a import time). Trovato e corretto un bug di rendering LaTeX (`\big(`/`\big)` non supportati da matplotlib mathtext) in 2.2, poi una seconda occorrenza (`\bigl(`/`\bigr)`) in 2.3 — stessa famiglia di comandi, mai supportata dal subset mathtext di matplotlib, scoperta solo eseguendo live la funzione: lezione confermata due volte, testare sempre l'esecuzione oltre a `qa.py --src`/`ast.parse`. Prossimo: content_2_4 (Optics)/2_5 (Wave Motion and Sound), poi build+QA Modulo 2, poi Modulo 3. Hub [[CAAE/Materiale Didattico]].
- [[Sessioni/2026-07-10]] — **Corsi (AVES)**: utente segnala 3 bug in un solo messaggio. (1) NOGO da scadenza DAA/NAM applicato per errore a tutti i moduli invece che solo al modulo 10 — causa 3 implementazioni duplicate della formula GO/NOGO, centralizzate in nuovo `GradeService.isGo(moduleNumber:)` (RISOLTO). (2) Overflow dashboard mobile frequentatore, riepilogo assenze/ore usciva dai box — fix `Expanded`+ellipsis in `attendee_attendance_screen.dart` (RISOLTO). (3) Slot calendario residuo dopo cancellazione (salva→cancella→riapri stesso slot mostra solo il modulo precedente) — analisi esaustiva di `schedule_tab.dart` (incl. `_editLessonInstructor` e `ScheduleService.deleteLesson`) non ha trovato alcun difetto di codice; ipotesi cache browser stale, in attesa di test hard-refresh dall'utente (APERTO). Commit `bc0536b` (fix) + `25fd734` (doc). Hub [[AVES Corsi/AVES Hub]]. — **Materiale Didattico CAAE**: avviata Fase 3 ("tutti i sottomoduli, tutti i corsi, dal Modulo 1") — **1.1-1.3** (Aritmetica/Algebra/Geometria) completati TB1+TB2, espansi secondo 2 nuove regole cardine per moduli 1-3 (dimostrazione obbligatoria di ogni formula + nessun limite di lunghezza/figura per ogni concetto visualizzabile, sinossi anche fino a 100 pagine), entrambe in memoria persistente. Scoperto e rimosso un 4° sottomodulo "1.4 Statistica" fabbricato senza fonte nel programma ufficiale (segnalato dall'utente); creata [[CAAE/Programmi Ufficiali — Argomenti per Sottomodulo]] per prevenire il ripetersi dell'errore. Scoperto un bug quiz (domande stringa-aperta invece di tuple 3-alternative) su 7/23 sottomoduli, fix avviato (completato il giorno dopo, vedi sopra). QA `qa.py` 0/0 su 60 PDF, spot-check pulito (1 falso positivo placeholder scartato: "todo" dentro "metodo"). **Decisione**: cartella (297 MB, mai pushata) resta **locale, non pushata** — l'unico repo raggiungibile è `rdagmr98/GymApp` (pubblico, app non correlata), utente ha scelto esplicitamente di non pubblicare per ora. Hub [[CAAE/Materiale Didattico]].

## Percorsi chiave
| Cosa | Path |
|------|------|
| Vault Obsidian | `C:\Users\Gianmarco\ObsidianVault\` |
| Memory Claude | `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\` |
| Releases | `C:\Users\Gianmarco\Documents\releases\` |
| ComfyUI output | `C:\Users\Gianmarco\ComfyUI\output\` |
| aiTool | `C:\Users\Gianmarco\aiTool\` |
