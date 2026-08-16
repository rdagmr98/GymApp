# Preferenze globali — Gianmarco

## Workflow Git (REGOLA OBBLIGATORIA)
- Dopo ogni modifica al codice: **commit + push immediatamente**, senza chiedere conferma.
- `git push origin main` su tutti i progetti è **esplicitamente autorizzato dall'utente**.
- Per il progetto `corsi`: build web prima del push (`flutter build web --release --base-href "/corsi/"`), poi commit + push. GitHub Actions deploya automaticamente.
- Ecosistema gym (`gym_app`, `app_cliente`/`gymapplogbook`, `app_coach`): regole di build/release/deploy complete vivono SOLO nel vault (single source of truth, per evitare che due copie divergano) — leggere `ObsidianVault/Gym App/Gym App.md` (hub) + `Gym App/Regole.md` (checklist build/release/deploy standing) + `Gym App/QR download.html FIX.md` (regola critica: QR pubblico dato a migliaia di persone, `web/download.html` non deve MAI dare 404, mai file statici a mano su `gh-pages`) prima di ogni modifica a queste app. Non duplicare quel contenuto qui.
- Qualsiasi progetto con un'istruzione operativa standing (build automatica dopo modifica, output in cartella specifica, checklist di release): la regola vive in `ObsidianVault/<Progetto>/Regole.md` (`tipo: regole`), non va ripetuta a voce — vedi protocollo vault sotto.

## Stile risposte
- Risposte brevi e dirette, in italiano.
- Niente sommari alla fine delle risposte (l'utente vede già il diff).
- Niente emoji.
- Se la domanda è semplice, risposta di una riga.
- Quando si lavora su un progetto, prima leggere il `CLAUDE.md` del progetto.
- Ponytail full obbligatorio in ogni sessione (già attivo di default). Eccezione permanente: progetti a densità testuale dove il prodotto stesso è testo (es. Materiale Didattico CAAE — poco codice, tanto contenuto per i PDF) — lì non tagliare l'output testuale richiesto esplicitamente.

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

**STEP 2 — se la sessione riguarda un progetto specifico**: leggere il hub (colonna "Hub" in `_CLAUDE.md`) **+ il suo `Regole.md` se esiste** (checklist operative standing: build/release/deploy, vincoli ricorrenti — evita di dover richiedere di nuovo a voce istruzioni già date in passato)

**STEP 2.5 — DURANTE il lavoro, non solo a fine sessione**: scrivere subito nella nota atomica pertinente (crearla se non esiste) quando si verifica:
- Un errore/bug capito o risolto (causa + fix, non solo il sintomo)
- Un file/script analizzato per la prima volta (cosa fa, dove vive, come si collega ad altri)
- Una decisione presa con l'utente (non solo a posteriori nel riepilogo)
In parallelo aggiungere una riga in `Sessioni/YYYY-MM-DD.md`: link alla nota atomica + pointer brevissimo (cosa, non perché/come — quello sta nella nota atomica). `Sessioni/YYYY-MM-DD.md` è un **indice**, mai narrativa: il dettaglio si scrive una volta sola, nella nota atomica. Non aspettare la fine della sessione per non perdere il contesto se la sessione si interrompe (compattazione, crash, rate limit).

**STEP 3 — a fine di ogni sessione significativa**:
1. Aggiornare il hub del progetto (stato, decisioni, TODO)
2. Creare/aggiornare `ObsidianVault/Sessioni/YYYY-MM-DD.md` — solo indice (vedi STEP 2.5), non narrativa
3. Aggiornare `_CLAUDE.md` → sezione "Ultime sessioni"
4. **Rolling window (anti-bloat, OBBLIGATORIO)**: `_CLAUDE.md` → "Ultime sessioni" tiene SOLO le ultime 3 giornate — quando si aggiunge la voce nuova, comprimere o rimuovere quelle più vecchie della finestra. Ogni hub progetto → sezione "STATO SESSIONE" tiene SOLO le ultime 1-2 voci, stesso criterio. Non è perdita di dati: lo storico completo resta sempre recuperabile da `Sessioni/YYYY-MM-DD.md` e dalla cronologia git della nota (il vault è nello stesso repo). Verificato il 2026-07-06: senza questa regola le sezioni crescono senza limite e vengono rilette per intero ad ogni sessione, indipendentemente dalla rilevanza per il task corrente — è il costo reale in token, non le note atomiche del vault (quelle restano piccole per natura).

## Note atomiche nel vault (OBBLIGATORIO, anti-bloat strutturale)
Non solo "Ultime sessioni"/"STATO SESSIONE" (regola sopra): anche gli **hub di progetto standalone** (es. `CAAE/Materiale Didattico.md`) possono gonfiarsi in changelog monolitici se si continua ad aggiungere narrativa dettagliata invece di linkare. Regola:
- Un hub è un **MOC** (Map of Content): elenco di link + una riga di pointer per argomento/fase, **mai** paragrafi lunghi di narrativa/bugfix/decisioni.
- Quando si scrive il resoconto dettagliato di un bugfix, di una fase di lavoro o di un argomento specifico e la sezione supererebbe ~15-20 righe → scriverlo direttamente in una **nota atomica separata** (un argomento per nota, titolo descrittivo, link `[[...]]` all'hub), non nell'hub.
- Se si scopre un hub già cresciuto in questo modo, va **diviso subito** (non rimandato): creare le note atomiche e **tagliare** il testo duplicato dall'hub nella stessa sessione — altrimenti il vault cresce invece di ridursi. Esempio fatto il 2026-07-18 su `CAAE/Materiale Didattico.md` (da 225 a ~130 righe, contenuto spostato in `Fase 2 - Sottomoduli DT-024.md`, `Fase 3 - Modulo 1 Mathematics.md`, `Fase 3 - Modulo 2 Physics.md`, `Bug e Lezioni Trasversali.md`). Pattern replicato il 2026-08-06 su `Gym App/Gym App.md` (142 → ~50 righe).
- Ogni nota ha `tipo:` nel frontmatter YAML — 4 valori: `hub` (MOC), `regole` (checklist standing, vedi STEP 2 sopra), `atomica` (un fatto/bugfix/decisione), `sessioni` (indice cronologico: link + riga breve per nota toccata, mai il dettaglio — regola 2026-08-07). Serve a leggere solo il set minimo di note pertinenti a un task invece dell'intero progetto. Tabella completa: `ObsidianVault/_CLAUDE.md` → sezione "Tipi di nota".
- Ogni nota che cita uno script modificato o un file fornito dall'utente (PDF, xlsx, esempio) include il **path locale completo**, non solo il nome — evita scan di cartelle o richiesta ripetuta a voce del percorso (2026-08-07). Pattern già in uso: `Buoni Pasti/Tivoli.md` (sezione Script), `reference_corsi_files.md`.
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
| Materiale Didattico CAAE (PDF corsi Part-66/147) | `C:\Users\Gianmarco\Materiale Didattico\_engine` → GitHub `rdagmr98/caae-materiale-didattico` (privato, solo codice — PDF output locali, non pushati) | `CAAE/Materiale Didattico.md` (Obsidian) |
| PDF Magic Tool Pro (editor/convertitore PDF desktop) | `C:\Users\Gianmarco\Python\pdfconverter.py` (+ `test_modifica.py`, `Setup_PDF_Magicpro.iss`) → GitHub `rdagmr98/pdfmagictool` — repo dedicato con `.gitignore` allowlist (solo questi file: `Python\` è una cartella di lavoro condivisa con script/media non correlati) | `PDF Magic Tool.md` (Obsidian) |
| PDF Unlock (app companion sblocco PDF Magic Tool) | `C:\Users\Gianmarco\PdfMagicToolUnlock` → GitHub `rdagmr98/pdfmagictool-unlock` (privato) | `PDF Magic Tool Sblocco Device-ID.md` (Obsidian) |
