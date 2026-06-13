# Preferenze globali — Gianmarco

## Workflow Git (REGOLA OBBLIGATORIA)
- Dopo ogni modifica al codice: **commit + push immediatamente**, senza chiedere conferma.
- `git push origin main` su tutti i progetti è **esplicitamente autorizzato dall'utente**.
- Per il progetto `corsi`: build web prima del push (`flutter build web --release --base-href "/corsi/"`), poi commit + push. GitHub Actions deploya automaticamente.
- Per il progetto `gym_app`: build APK + web, GitHub Release se APK >100MB (non commit per APK), push web su main.

## Stile risposte
- Risposte brevi e dirette, in italiano.
- Niente sommari alla fine delle risposte (l'utente vede già il diff).
- Niente emoji.
- Se la domanda è semplice, risposta di una riga.
- Quando si lavora su un progetto, prima leggere il `CLAUDE.md` del progetto.

## Continuità di sessione
- All'inizio di ogni sessione leggere: `CLAUDE.md` del progetto + i file di memoria rilevanti.
- Il `CLAUDE.md` del progetto contiene lo stato corrente, i TODO e le ultime modifiche.
- La memoria è in `C:\Users\Gianmarco\.claude\projects\C--Users-Gianmarco\memory\`.
- Aggiornare il `CLAUDE.md` del progetto (sezione STATO SESSIONE) ad ogni push.

## Vault Obsidian — Knowledge Graph
- Percorso: `C:\Users\Gianmarco\ObsidianVault\`
- MCP `obsidian` disponibile (scope user) — usa `mcp__obsidian__*` per leggere/aggiornare i grafi
- Grafi Canvas: `ObsidianVault\Grafi\` (Buoni Pasti Pipeline, Gym App, AVES Piloti e Corsi)
- Note per Graph View neural: `Buoni Pasti\`, `Gym App\`, `AVES Corsi\`
- Aggiornare le note vault quando cambia architettura significativa

## Progetti attivi
| Progetto | Path | CLAUDE.md |
|----------|------|-----------|
| corsi (EASA Part-66) | `C:\Users\Gianmarco\corsi` | `corsi/CLAUDE.md` |
| piloti (AVES piloti) | `C:\Users\Gianmarco\piloti` | `piloti/CLAUDE.md` |
| AVES tecnici | `C:\Users\Gianmarco\AVES` | `AVES/CLAUDE.md` |
| gym_app (trainer) | `C:\Users\Gianmarco` (root) | — |
| app_coach (PT) | `rdagmr98/gymapp-coach` | — |
| app_cliente | `C:\Users\Gianmarco\fix-ads` | — |
| buoni pasti | script Python in `C:\Users\Gianmarco` | — |
