# Vault Index — Gianmarco
Master index di tutti i progetti. Leggere per orientarsi nel vault.

> **Claude**: leggi prima `[[_CLAUDE]]` — contiene contesto completo, progetti e ultime sessioni.

---

## File Claude (leggi sempre)
- [[_CLAUDE]] — contesto master: profilo, progetti, sessioni recenti, strumenti
- [[Preferenze]] — preferenze permanenti utente e workflow
- `Sessioni/` — log sessioni (una nota per data)

---

## Progetti attivi

| Gruppo | Hub | Trigger sessione Claude |
|--------|-----|------------------------|
| [[AVES Corsi/AVES Hub]] | 3 app militari (piloti/corsi/tecnici AVES) | directory `piloti/`, `corsi/`, `AVES/` |
| [[Gym App/Gym App]] | 3 app palestra (trainer/coach/cliente) | directory root gym, `fix-ads/` |
| [[Buoni Pasti/Pipeline]] | Script buoni pasto e cartellini lavoratori | topic buoni pasto/cedolini |
| [[Centri Storici/Hub]] | DB indirizzi centro storico comuni italiani | topic centri storici/OSM |
| [[Stonks/Stonks]] | Portfolio tracker (clone getquin) — azioni/ETF/crypto | directory `stonks/`, topic investimenti/portafoglio |
| [[SIEL/SIEL]] | Gestionale elicotteri AVES (ex Access) — desktop Flask + web app static | `SIEL_Portable/`, `siel_app/`, topic SIEL/elicotteri/manutenzione |

---

## ComfyUI — Generazione immagini locale
- **Path**: `C:\Users\Gianmarco\ComfyUI`
- **Modello**: Flux Schnell GGUF Q4_K_S (`models/diffusion_models/`)
- **Avvio**: `avvia.bat` (usa `--cpu`, ~5-25 min per immagine)
- **MCP**: `comfyui-mcp` (88 tool, usa `enqueue_workflow` con UnetLoaderGGUF)
- **Output**: `C:\Users\Gianmarco\ComfyUI\output\`
- **Nota**: DirectML NON funziona (crash DLL), usare sempre `--cpu`

---

## aiTool — Browser Automation Multi-AI (risparmio token)
- **Path**: `C:\Users\Gianmarco\aiTool` | Fork: `rdagmr98/aiTool`
- **Hub**: [[aiTool/aiTool Hub]]
- **Avvio**: `avvia_edge_debug.bat` poi `ai.bat "prompt"`
- **Auto-routing**: immagine/canvas → Gemini · slide/ppt → Claude · resto → tutti e 3 in parallelo
- **Quando usarlo**: se l'utente dice "usa meno crediti" o "risparmia token"

---

## Grafi Canvas
- `Grafi/Buoni Pasti Pipeline` — pipeline visuale buoni pasto
- `Grafi/Gym App` — architettura gym
- `Grafi/AVES Piloti e Corsi` — struttura AVES

---

## Note giornaliere / Sessioni
- `Sessioni/2026-06-20.md` — aiTool batch mode, Obsidian memoria Claude impostata
- `2026-06-13.md` — cleanup disco, ComfyUI setup, Obsidian reorganization
