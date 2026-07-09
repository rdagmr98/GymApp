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
- [[Sessioni/2026-07-09]] — **PPL Quiz**: chiuso v1.3.0. Figure reali scaricate (mai AI-generate) per le domande con immagine (commit `20fd76f`), rimossa info database da home (commit `7e008ed`), completate le spiegazioni per-domanda sulle ultime 6 materie (parte 5-10, commit `293eaec`/`3a5d50f`/`8189dd7`/`63759bc`/`c7f9241`/`f51f044`) → **copertura 2273/2273 (100%)**. Bug scoperto post-completamento: 111/209 spiegazioni della parte 10 avevano ASCII invece di accenti italiani (incl. 2 errori di significato, "atterra"→"atterrà"), corretto e verificato (commit `7b9e716`). Scoperta ambientale non bloccante: `git commit -m` via heredoc Bash su questa macchina Windows può perdere accenti nel testo del messaggio (non nei file) — memoria [[feedback_bash_heredoc_accenti]]. Hub [[PPL Quiz/PPL Quiz Hub]].
- [[Sessioni/2026-07-08]] — **Gym App**: analizzati e risolti 3 warning tecnici Play Console per GymApp. (1) Edge-to-edge deprecato — causa reale: `lib/main.dart` passava colori espliciti a `SystemUiOverlayStyle` in 3 punti (avvio + tema chiaro con preset `.dark` che forza nav bar nera anche a tema chiaro + tema scuro senza override); fix rimuove tutti i colori, mantiene solo icon brightness (percorso non deprecato). Bonus: risolto bug nav bar nera forzata in tema chiaro. (2) BitmapFactory downsampling — NON in codice app (verificato tutto Kotlin+Dart), probabile causa interna a `google_mobile_ads` (4 major indietro); bump non eseguito senza retest reale, segnalato all'utente come decisione aperta. Scoperto (e scartato) un branch `gh-pages` orfano con relativo worktree in `C:\Temp` — **non è la pipeline reale**, Pages serve da `main` (confermato via API, coerente con memoria esistente). Release **v1.0.2+29**: fix commit `572174a`, deploy web commit `0910d27`, APK×3+AAB+GitHub Release pubblicati. **Poi**: l'utente ha verificato sul device reale che il fix "floor 64px" del bug S23 (v1.0.2+28, sessione 07 lug) era in realtà un overcorrection — v27 posizionava già bene il pulsante "Salva serie", il floor lo alzava troppo. Revertito in **v1.0.2+30** (commit `86e1bd4`+`7f8314d`), tornato al calcolo semplice senza floor, mantenuta la fix strutturale v27. App_cliente ha lo stesso floor 64px (commit `5050ab4`) non ancora verificato/corretto. Hub [[Gym App/Gym App]].
- [[Sessioni/2026-07-07]] — **Gym App**: 3 tentativi falliti sul bug pulsante Salva Serie invisibile su S23 (dopo il fix del 06/07, incluso un fix strutturale Round 4 — Row fissa fuori da scroll, v1.0.2+27 — corretto ma insufficiente) prima di trovare la causa reale: `MediaQuery.padding.bottom`/`viewPadding.bottom` sottostima l'inset nav bar su questo Samsung One UI anche in edge-to-edge. Fix Round 5: floor hardcoded 64px (max tra inset OS e soglia fissa) su gym_app (commit `214bef5`) e app_cliente (commit `5050ab4`). Release gym_app **v1.0.2+28** (APK×3+AAB+web, live verificato), app_cliente APK ricaricato su v1.0.1. 4° tentativo complessivo sul bug — da confermare sul device reale, se fallisce ancora serve una misura reale della nav bar invece di continuare a indovinare. Ipotesi gap distribuzione Play Store esclusa (sideload diretto riproduce lo stesso bug). Hub [[Gym App/Gym App]]. — **Corsi (AVES)**: chiuso il 2° punto della sessione 26, M9/M10 staccati. Trovato 1 corso standalone reale negli xlsx forniti (2° M9/3° M10 B1/B2, nov.2024, Minissi 14h + Mirto 12h). Bloccante PII (nomi cifrati AES) risolto senza decifratura offline: `currency_tab.dart` decifra già i nomi nella UI admin autenticata, via corretta per risolvere nome→ID. Scelto di non creare un `Course` record (corso chiuso, no attendee) — solo 2 voci `updates.json` via `addUpdate`/"Aggiorna ore", da inserire manualmente dall'utente in-app. Dettaglio `corsi/CLAUDE.md`. Hub [[AVES Corsi/AVES Hub]]. — **Buoni Pasti**: Rieti — trovato e corretto bug `elabora_rieti.py` (zip annidati saltati silenziosamente, 9/62 lavoratori colpiti), rielaborati e verificati, nuovo totale 1.461.530,41 EUR (+124.790,47). Verona — script incrementale `integra_verona_gianmarco.py`, +10 lavoratori (109 tot, 105.688 buoni), 1 escluso (CARDONE FABIOLA, formato cartellino incompatibile, da segnalare all'utente). Hub [[Buoni Pasti/Pipeline]], dettagli [[Buoni Pasti/Rieti]] e [[Buoni Pasti/Verona]].

## Percorsi chiave
| Cosa | Path |
|------|------|
| Vault Obsidian | `C:\Users\Gianmarco\ObsidianVault\` |
| Memory Claude | `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\` |
| Releases | `C:\Users\Gianmarco\Documents\releases\` |
| ComfyUI output | `C:\Users\Gianmarco\ComfyUI\output\` |
| aiTool | `C:\Users\Gianmarco\aiTool\` |
