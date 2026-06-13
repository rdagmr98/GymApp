# Vault Index — Gianmarco
Master index di tutti i progetti. Leggere per orientarsi nel vault.

---

## Progetti attivi

| Gruppo | Hub | Trigger sessione Claude |
|--------|-----|------------------------|
| [[AVES Corsi/AVES Hub]] | 3 app militari (piloti/corsi/tecnici AVES) | directory `piloti/`, `corsi/`, `AVES/` |
| [[Gym App/Gym App]] | 3 app palestra (trainer/coach/cliente) | directory root gym, `fix-ads/` |
| [[Buoni Pasti/Pipeline]] | Script buoni pasto e cartellini lavoratori | topic buoni pasto/cedolini |
| [[Centri Storici/Hub]] | DB indirizzi centro storico comuni italiani | topic centri storici/OSM |

---

## ComfyUI — Generazione immagini locale
- **Path**: `C:\Users\Gianmarco\ComfyUI`
- **Modello**: Flux Schnell GGUF Q4_K_S (`models/diffusion_models/`)
- **Avvio**: `avvia.bat` (usa `--cpu`, ~5-25 min per immagine)
- **MCP**: `comfyui-mcp` (88 tool, usa `enqueue_workflow` con UnetLoaderGGUF)
- **Output**: `C:\Users\Gianmarco\ComfyUI\output\`
- **Nota**: DirectML NON funziona (crash DLL), usare sempre `--cpu`

---

## Grafi Canvas
- `Grafi/Buoni Pasti Pipeline` — pipeline visuale buoni pasto
- `Grafi/Gym App` — architettura gym
- `Grafi/AVES Piloti e Corsi` — struttura AVES

---

## Note giornaliere
- `2026-06-13.md` — cleanup disco, ComfyUI setup, Obsidian reorganization
