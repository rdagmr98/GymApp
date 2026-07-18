# Preferenze globali — Gianmarco

## Workflow Git (REGOLA OBBLIGATORIA)
- Dopo ogni modifica al codice: **commit + push immediatamente**, senza chiedere conferma.
- `git push origin main` su tutti i progetti è **esplicitamente autorizzato dall'utente**.
- Per il progetto `corsi`: build web prima del push (`flutter build web --release --base-href "/corsi/"`), poi commit + push. GitHub Actions deploya automaticamente.
- Ecosistema gym (`gym_app`, `app_cliente`/`gymapplogbook`, `app_coach`): regole di build/release/deploy complete vivono SOLO nel vault (single source of truth, per evitare che due copie divergano) — leggere `ObsidianVault/Gym App/Gym App.md` (hub, build APK+AAB+web/Play Store/versionCode) + `Gym App/app_cliente.md` (chiarimento repo unico) + `Gym App/QR download.html FIX.md` (regola critica: QR pubblico dato a migliaia di persone, `web/download.html` non deve MAI dare 404, mai file statici a mano su `gh-pages`) prima di ogni modifica a queste app. Non duplicare quel contenuto qui.

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
- Routing automatico: immagini/canvas → Gemini · resto → tutti e 3 parallelo · `--batch` per task diversi in parallelo

## Vault Obsidian — Memoria Persistente (PROTOCOLLO OBBLIGATORIO)

**STEP 1 — SEMPRE, prima di tutto**: `Read C:\Users\Gianmarco\ObsidianVault\_CLAUDE.md`
- Dà: profilo utente, progetti attivi, ultime sessioni, strumenti disponibili
- 30 secondi, evita di re-derivare contesto ogni sessione

**STEP 2 — se la sessione riguarda un progetto specifico**: leggere il hub (colonna "Hub" in `_CLAUDE.md`)

**STEP 2.5 — DURANTE il lavoro, non solo a fine sessione**: scrivere subito nel vault (hub progetto o `Sessioni/YYYY-MM-DD.md`) quando si verifica:
- Un errore/bug capito o risolto (causa + fix, non solo il sintomo)
- Un file/script analizzato per la prima volta (cosa fa, dove vive, come si collega ad altri)
- Una decisione presa con l'utente (non solo a posteriori nel riepilogo)
Non aspettare la fine della sessione per non perdere il contesto se la sessione si interrompe (compattazione, crash, rate limit).

**STEP 3 — a fine di ogni sessione significativa**:
1. Aggiornare il hub del progetto (stato, decisioni, TODO)
2. Creare/aggiornare `ObsidianVault/Sessioni/YYYY-MM-DD.md`
3. Aggiornare `_CLAUDE.md` → sezione "Ultime sessioni"
4. **Rolling window (anti-bloat, OBBLIGATORIO)**: `_CLAUDE.md` → "Ultime sessioni" tiene SOLO le ultime 3 giornate — quando si aggiunge la voce nuova, comprimere o rimuovere quelle più vecchie della finestra. Ogni hub progetto → sezione "STATO SESSIONE" tiene SOLO le ultime 1-2 voci, stesso criterio. Non è perdita di dati: lo storico completo resta sempre recuperabile da `Sessioni/YYYY-MM-DD.md` e dalla cronologia git della nota (il vault è nello stesso repo). Verificato il 2026-07-06: senza questa regola le sezioni crescono senza limite e vengono rilette per intero ad ogni sessione, indipendentemente dalla rilevanza per il task corrente — è il costo reale in token, non le note atomiche del vault (quelle restano piccole per natura).

## Note atomiche nel vault (OBBLIGATORIO, anti-bloat strutturale)
Non solo "Ultime sessioni"/"STATO SESSIONE" (regola sopra): anche gli **hub di progetto standalone** (es. `CAAE/Materiale Didattico.md`) possono gonfiarsi in changelog monolitici se si continua ad aggiungere narrativa dettagliata invece di linkare. Regola:
- Un hub è un **MOC** (Map of Content): elenco di link + una riga di pointer per argomento/fase, **mai** paragrafi lunghi di narrativa/bugfix/decisioni.
- Quando si scrive il resoconto dettagliato di un bugfix, di una fase di lavoro o di un argomento specifico e la sezione supererebbe ~15-20 righe → scriverlo direttamente in una **nota atomica separata** (un argomento per nota, titolo descrittivo, link `[[...]]` all'hub), non nell'hub.
- Se si scopre un hub già cresciuto in questo modo, va **diviso subito** (non rimandato): creare le note atomiche e **tagliare** il testo duplicato dall'hub nella stessa sessione — altrimenti il vault cresce invece di ridursi. Esempio fatto il 2026-07-18 su `CAAE/Materiale Didattico.md` (da 225 a ~130 righe, contenuto spostato in `Fase 2 - Sottomoduli DT-024.md`, `Fase 3 - Modulo 1 Mathematics.md`, `Fase 3 - Modulo 2 Physics.md`, `Bug e Lezioni Trasversali.md`).
- Dettaglio/esempi ulteriori: `ObsidianVault/_CLAUDE.md` → sezione "Note atomiche".

## Note vuote/stub nel vault
Se una nota ha solo titolo + 1 riga (creata per il Graph View), e durante il lavoro si scopre il contenuto reale (da codice, script, hub), arricchirla subito invece di lasciarla stub. Non creare nuove note-stub senza poi riempirle nella stessa sessione.

- Vault path: `C:\Users\Gianmarco\ObsidianVault\`
- MCP disponibile: `mcp__obsidian__search-vault`, `mcp__obsidian__read-note`, etc.
- **Scrivere/aggiornare note**: `Write` tool su path diretto — NON `mcp__obsidian__edit-note` (lento, si blocca)

## Progetti attivi
| Progetto | Path | CLAUDE.md |
|----------|------|-----------|
| corsi (EASA Part-66) | `C:\Users\Gianmarco\corsi` | `corsi/CLAUDE.md` |
| piloti (AVES piloti) | `C:\Users\Gianmarco\piloti` | `piloti/CLAUDE.md` |
| AVES tecnici | `C:\Users\Gianmarco\AVES` | `AVES/CLAUDE.md` |
| gym_app (trainer) | `C:\Users\Gianmarco` (root) | — |
| app_coach (PT) | `rdagmr98/gymapp-coach` | — |
| app_cliente / gymapplogbook (mobile+web, stesso repo) | `C:\Users\Gianmarco\fix-ads` → remote `rdagmr98/gymapplogbook` (branch main) | `fix-ads/CLAUDE.md` |
| buoni pasti | script Python in `C:\Users\Gianmarco` | — |
| centri storici | `C:\Users\Gianmarco\Documents\` | — |
| stonks | `C:\Users\Gianmarco\stonks` | `stonks/CLAUDE.md` |
| SIEL desktop | `C:\Users\Gianmarco\Documents\SIEL_Portable` (+ `siel_app`) | — |
| SIEL web app | `rdagmr98/siel` + dati `rdagmr98/siel-data` (privati) | `SIEL/SIEL.md` (Obsidian) |
| Gestione Flotta (flotta elicotteri completa) | `C:\Users\Gianmarco\Documents\gestione_flotta` → GitHub `rdagmr98/gestione_flotta` (privato, solo codice — dati locali via `.gitignore`) | `Gestione Manutenzione/Gestione Flotta.md` (Obsidian) |
