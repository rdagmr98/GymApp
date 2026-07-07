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
| PPL Quiz | `C:\Users\Gianmarco\ppl` → `rdagmr98/ppl` | [[PPL Quiz/PPL Quiz Hub]] | Flutter mobile+web, quiz teorico pilota privato, DB 2273 q ENAC/EASA, v1.2.0 con statistiche/grafici, web https://rdagmr98.github.io/ppl/ |

## Ultime sessioni
_Solo ultimi 3 giorni. Storico completo: `Sessioni/YYYY-MM-DD.md` (una per giorno) + cronologia git di questo file._
- [[Sessioni/2026-07-07]] — **Gym App**: 3 tentativi falliti sul bug pulsante Salva Serie invisibile su S23 (dopo il fix del 06/07, incluso un fix strutturale Round 4 — Row fissa fuori da scroll, v1.0.2+27 — corretto ma insufficiente) prima di trovare la causa reale: `MediaQuery.padding.bottom`/`viewPadding.bottom` sottostima l'inset nav bar su questo Samsung One UI anche in edge-to-edge. Fix Round 5: floor hardcoded 64px (max tra inset OS e soglia fissa) su gym_app (commit `214bef5`) e app_cliente (commit `5050ab4`). Release gym_app **v1.0.2+28** (APK×3+AAB+web, live verificato), app_cliente APK ricaricato su v1.0.1. 4° tentativo complessivo sul bug — da confermare sul device reale, se fallisce ancora serve una misura reale della nav bar invece di continuare a indovinare. Ipotesi gap distribuzione Play Store esclusa (sideload diretto riproduce lo stesso bug). Hub [[Gym App/Gym App]]. — **Corsi (AVES)**: chiuso il 2° punto della sessione 26, M9/M10 staccati. Trovato 1 corso standalone reale negli xlsx forniti (2° M9/3° M10 B1/B2, nov.2024, Minissi 14h + Mirto 12h). Bloccante PII (nomi cifrati AES) risolto senza decifratura offline: `currency_tab.dart` decifra già i nomi nella UI admin autenticata, via corretta per risolvere nome→ID. Scelto di non creare un `Course` record (corso chiuso, no attendee) — solo 2 voci `updates.json` via `addUpdate`/"Aggiorna ore", da inserire manualmente dall'utente in-app. Dettaglio `corsi/CLAUDE.md`. Hub [[AVES Corsi/AVES Hub]].
- [[Sessioni/2026-07-06]] — **Gym App ecosystem**: fix pulsante "Salva serie" invisibile su Samsung S23 (segnalato dall'utente come critico) — causa doppia: popup limitato al 56% altezza schermo senza `isScrollControlled` (aggravato in gym_app dalla pubblicità nel popup) + padding nav bar fisso (`32`) insufficiente per barre a 3 tasti Samsung. Fix identico su gym_app e app_cliente (codice condiviso): `isScrollControlled: true` + `SingleChildScrollView` + padding dinamico da `MediaQuery` (nav bar/gesture inset reali del dispositivo). `flutter analyze` pulito su entrambe. gym_app v1.0.2+26 (APK+AAB+web, GitHub Release, web deploy live confermato), app_cliente APK ri-caricato su release v1.0.1 esistente. Hub [[Gym App/Gym App]]. — **Corsi (AVES)**: sessione 26 avviata, 1° punto chiuso — OJT auto-decay currency rule implementata e deployata (commit `08d9629`).
- [[Sessioni/2026-07-05]] — **CAAE Materiale Didattico**: direttiva utente di economia token (troppi token per 20 pagine di PDF) → policy **foto reali prima dei matplotlib** (Wikimedia/DVIDS pubblico dominio/CC, attribuite, mai Getty/Shutterstock), **2-4 figure/sottomodulo**, **quiz ridotto a ~10 domande**, QA ridotto a gate strutturale + ispezione visiva leggera una tantum (non più page-by-page) — profondità di contenuto/fisica invariata. Chiusi **11A.13** (Carrello di atterraggio), **11A.14** (Impianto luci) e **12.9** (Equipaggiamenti e arredi), tutti maml+TB1/TB1, contenuto unico. Task #22/#23/#24 chiusi. Prossimo: #25 (13.4, Comm/Nav TACAN/GLS/TLS). Hub [[CAAE/Materiale Didattico]].

## Percorsi chiave
| Cosa | Path |
|------|------|
| Vault Obsidian | `C:\Users\Gianmarco\ObsidianVault\` |
| Memory Claude | `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\` |
| Releases | `C:\Users\Gianmarco\Documents\releases\` |
| ComfyUI output | `C:\Users\Gianmarco\ComfyUI\output\` |
| aiTool | `C:\Users\Gianmarco\aiTool\` |
