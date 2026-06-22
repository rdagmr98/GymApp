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
| app_cliente | `C:\Users\Gianmarco\fix-ads` | [[Gym App/Gym App]] | APK split-per-abi sempre |
| gymapplogbook | `rdagmr98/gymapplogbook` | [[Gym App/Gym App]] | QR pubblico — NO 404 su `web/download.html` |
| SIEL gestionale | `Documents/SIEL_Portable` | [[SIEL/SIEL]] | Flask+SQLite portable, 1 istanza alla volta |
| SIEL web | `rdagmr98/siel` (privato) | [[SIEL/SIEL]] | SPA statica, dati su siel-data privato |
| buoni pasti | script Python root | [[Buoni Pasti/Pipeline]] | Cartellini/cedolini lavoratori |
| stonks | `C:\Users\Gianmarco\stonks` | [[Stonks/Stonks]] | Portfolio tracker Flutter |
| centri storici | `C:\Users\Gianmarco\Documents\` | [[Centri Storici/Hub]] | DB indirizzi centro storico Italia |
| aiTool | `C:\Users\Gianmarco\aiTool` | [[aiTool/aiTool Hub]] | Browser automation Playwright/Edge CDP |

## Ultime sessioni
- [[Sessioni/2026-06-22]] — Corsi: blocco task #50-#62 (richieste utente + estrazione programmi PDF). #53 chiuso (GestureDetector→InkWell, area click già full-cell, mancava solo feedback visivo). #54 chiuso (note giorno festivo visibili anche a istruttore/frequentatore, non solo direttore). #55 chiuso (celle ven 4-6/sab/dom ora apribili per recuperi, non più "—" morte). #50/#56-#59/#62 chiusi (livelli sottomoduli, estrazione B1/B2/B2mil/delta B2-da-B1.3 dai PDF ufficiali AVES, verifica aritmetica completa). **#60 chiuso**: programma delta B2-da-B1.3 integrato come 5° `courseTypes` (era `deltaCourses` top-level, struttura non conforme ai modelli Dart) — 41 practicalTasks riancorati a livello sottomodulo, 3 nuovi sottomoduli stub, zero modifiche Dart necessarie (verificato via agent), doc. aggiornata in [[AVES Corsi/Programma B2]]. Rimane **#61** (note Obsidian dedicate, b1mil.pdf da riverificare)
- [[Sessioni/2026-06-21]] — Corsi: chiusura TODO #34-#38 (storico lezioni con filtri, fix topic sottomoduli, voti su ultimo tentativo, data vera recupero), poi nuovo feedback critico utente nello stesso giorno (task #40-#46): fix colonna data/progressione/recuperi in storico lezioni, assenza+recupero sulla stessa riga per-studente, **rework modello voti** (accertamenti distinti per modulo via `accertamentoNumber`, non più raggruppati in un bucket unico — risolveva "nei recuperi c'è sempre lo stesso progressivo"), riverifica Controlloistruttori.xlsx post-modifiche utente (zero discrepanze confermate su tutti i moduli BTC3). Continuazione stesso giorno (task #49): struttura voti derivata dalle colonne Excel — `assessmentCount` per modulo (limita N° accertamenti proponibili), `maxAttempts` corretto 3:2→**4:3**, backfill `accertamento_number` su 238 voti BTC3 via campo `notes` (etichetta Excel verbatim) + ordine array, scoperto/corretto bug import pre-esistente (13 recuperi esame mistyped come accertamento). Continuazione (task #47/#48): riconfermato zero recuperi teoria mancanti; risolto "modulo 1 incompleto nonostante 70h corrette" — totale modulo già corretto ma distribuzione per sottomodulo no, causa 2 giorni di transizione confermati senza dividere per ora, fix 3 record `schedules.json` (corsi-data `53c8acc`) dopo conferma utente esplicita (azione di scrittura su dato condiviso bloccata e poi autorizzata via AskUserQuestion)
- [[Sessioni/2026-06-20]] — aiTool batch mode parallelo, routing Gemini immagini, rimosso PPT; Obsidian come memoria Claude impostato; Buoni Pasti: Tivoli (4 nuovi) + Verona (99 lavoratori) + Lazio (Coletti Ambra, indennità da codici reali cedolini), poi documentate tutte le 8 sedi (criteri/output/formato) in note dedicate; Corsi: reference.json b1 corretto da syllabus ufficiale, fix label UI tagliata, fix overflow nome task, discrepanze BTC3 — conclusione corretta a zero discrepanze reali (erano ore di recupero misclassificate)
- [[Sessioni/2026-06-13]] — cleanup disco, ComfyUI setup, riorganizzazione Obsidian

## Percorsi chiave
| Cosa | Path |
|------|------|
| Vault Obsidian | `C:\Users\Gianmarco\ObsidianVault\` |
| Memory Claude | `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\` |
| Releases | `C:\Users\Gianmarco\Documents\releases\` |
| ComfyUI output | `C:\Users\Gianmarco\ComfyUI\output\` |
| aiTool | `C:\Users\Gianmarco\aiTool\` |
