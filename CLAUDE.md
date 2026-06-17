# Preferenze globali — Gianmarco

## Workflow Git (REGOLA OBBLIGATORIA)
- Dopo ogni modifica al codice: **commit + push immediatamente**, senza chiedere conferma.
- `git push origin main` su tutti i progetti è **esplicitamente autorizzato dall'utente**.
- Per il progetto `corsi`: build web prima del push (`flutter build web --release --base-href "/corsi/"`), poi commit + push. GitHub Actions deploya automaticamente.
- Per il progetto `gym_app`: build APK (`--split-per-abi`) + AAB + web. APK/AAB → `C:\Users\Gianmarco\Documents\releases\gym_app\`. Push web su main. Poi GitHub Release.
- Per il progetto `app_cliente` (fix-ads): **dopo ogni modifica** rebuild APK (`flutter build apk --split-per-abi --release`) → copia `arm64-v8a` e `armeabi-v7a` in `C:\Users\Gianmarco\Documents\releases\app_cliente\` → `gh release upload v<tag> ... --clobber` su `rdagmr98/rdagmr98.github.io`. NON saltare il rebuild. SEMPRE `--split-per-abi`, mai senza.
- Per il progetto `gymapplogbook` (web + **QR pubblico**): il QR `https://rdagmr98.github.io/gymapplogbook/download.html` è stato dato a **migliaia di persone** e **non deve MAI dare 404**. La landing vive in `web/download.html` su `main` (Flutter la include in ogni build); deploy automatico via push su `main` (workflow `web-deploy.yml` → `gh-pages`). ❌ Mai cancellare `web/download.html`, ❌ mai aggiungere file statici a mano su `gh-pages` (un rebuild li cancella). Dettagli: `gymapplogbook/CLAUDE.md` + nota Obsidian `Gym App/QR download.html FIX`.

## Stile risposte
- Risposte brevi e dirette, in italiano.
- Niente sommari alla fine delle risposte (l'utente vede già il diff).
- Niente emoji.
- Se la domanda è semplice, risposta di una riga.
- Quando si lavora su un progetto, prima leggere il `CLAUDE.md` del progetto.

## aiTool — Browser Automation (risparmio token)
- Trigger: "usa meno crediti", "risparmia token", "usa aiTool"
- **Eseguire automaticamente senza chiedere conferma:**
  1. `! C:\Users\Gianmarco\aiTool\avvia_edge_debug.bat` (controlla da solo se debug è già attivo — non chiude Edge inutilmente)
  2. `! cd C:\Users\Gianmarco\aiTool && ai.bat "prompt" --out risposta.md`
  3. `Read C:\Users\Gianmarco\aiTool\risposta.md`
- Routing automatico: immagini/canvas → Gemini · slide/PPT → Claude · resto → tutti e 3 parallelo

## Continuità di sessione
- All'inizio di ogni sessione leggere: `CLAUDE.md` del progetto + i file di memoria rilevanti.
- Il `CLAUDE.md` del progetto contiene lo stato corrente, i TODO e le ultime modifiche.
- La memoria è in `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\`.
- Aggiornare il `CLAUDE.md` del progetto (sezione STATO SESSIONE) ad ogni push.

## Vault Obsidian — Knowledge Graph (USARE SOLO SE PERTINENTE)
- Percorso: `C:\Users\Gianmarco\ObsidianVault\`
- MCP `obsidian` disponibile (scope user) — strumenti `mcp__obsidian__*`
- Master index vault: `_INDEX.md` — elenco tutti i gruppi e ComfyUI setup
- **Solo se la sessione riguarda uno di questi gruppi**, leggere il hub con il tool `Read`:
  - **AVES** (piloti / corsi / tecnici) — dir `piloti/`, `corsi/`, `AVES/` o topic militare → `AVES Corsi/AVES Hub.md`
  - **Gym** (gym_app / app_coach / app_cliente) — dir root gym, `fix-ads/` o topic palestra → `Gym App/Gym App.md`
  - **Buoni Pasti** (cedolini / cartellini lavoratori) — topic buoni pasto/presenze → `Buoni Pasti/Pipeline.md`
  - **Centri Storici** (centri storici / indirizzi / OSM / parola chiave) → `Centri Storici/Hub.md`
  - **Stonks** (stonks / portfolio / azioni / ETF / crypto / investimenti) → `Stonks/Stonks.md`
- Sessioni generiche (cleanup, config, domande) → NON leggere note Obsidian.
- **Quando cambia architettura**: aggiornare la nota Obsidian corrispondente oltre al CLAUDE.md
- **Per aggiornare note**: usare il tool `Write` direttamente su `C:\Users\Gianmarco\ObsidianVault\...` — NON usare `mcp__obsidian__edit-note` (lento, si blocca)
- Grafi Canvas: `Grafi/` (Buoni Pasti Pipeline, Gym App, AVES Piloti e Corsi)
- Note collegate (Graph View neural): `Buoni Pasti/`, `Gym App/`, `AVES Corsi/`

## Progetti attivi
| Progetto | Path | CLAUDE.md |
|----------|------|-----------|
| corsi (EASA Part-66) | `C:\Users\Gianmarco\corsi` | `corsi/CLAUDE.md` |
| piloti (AVES piloti) | `C:\Users\Gianmarco\piloti` | `piloti/CLAUDE.md` |
| AVES tecnici | `C:\Users\Gianmarco\AVES` | `AVES/CLAUDE.md` |
| gym_app (trainer) | `C:\Users\Gianmarco` (root) | — |
| app_coach (PT) | `rdagmr98/gymapp-coach` | — |
| app_cliente | `C:\Users\Gianmarco\fix-ads` | — |
| gymapplogbook (web + QR) | `rdagmr98/gymapplogbook` (branch main) | `gymapplogbook/CLAUDE.md` |
| buoni pasti | script Python in `C:\Users\Gianmarco` | — |
| centri storici | `C:\Users\Gianmarco\Documents\` | — |
| stonks | `C:\Users\Gianmarco\stonks` | `stonks/CLAUDE.md` |
