# aiTool — Hub
Browser automation multi-AI per risparmiare token API. Usa Edge in debug mode.

**Path locale**: `C:\Users\Gianmarco\aiTool`
**Fork GitHub**: `rdagmr98/aiTool` (originale: `ivanlombardi/aiTool`)

---

## Avvio rapido

```powershell
# 1. Avvia Edge in debug (una volta per sessione)
C:\Users\Gianmarco\aiTool\avvia_edge_debug.bat

# 2. Accedi su claude.ai + gemini.google.com + perplexity.ai nel browser

# 3. Usa il tool
cd C:\Users\Gianmarco\aiTool
ai.bat "il tuo prompt"
```

---

## Auto-Routing

| Keyword nel prompt | Provider scelto |
|---|---|
| immagine, foto, logo, canvas, diagram, grafico | **Gemini** (+ salva img automatico) |
| presentazione, slide, ppt, deck | **Claude** (artifact HTML) |
| tutto il resto | **Tutti e 3 in parallelo** |

```powershell
ai.bat "genera un logo"              # → Gemini
ai.bat "crea slide su Python"        # → Claude
ai.bat "cos'è il SQL injection"      # → Perplexity + Gemini + Claude parallelo
ai.bat "..." -p all                  # forza tutti e 3
ai.bat "..." -p claude               # forza provider specifico
ai.bat "..." -r                      # abilita Reasoning/Thinking
ai.bat "..." --out note.md           # salva output su file
```

---

## In Claude Code (risparmio token)

Quando l'utente dice "usa meno crediti" o "risparmia token":

```bash
! cd C:\Users\Gianmarco\aiTool && ai.bat "prompt" --out risposta.md
# poi leggi: Read C:\Users\Gianmarco\aiTool\risposta.md
```

---

## Architettura

```
aiTool.py        — orchestratore (threading parallelo, auto-routing)
router.py        — keyword detection → provider selection
geminiPage.py    — Gemini driver + download immagini
claudePage.py    — Claude driver + download artifact HTML
perplexityPage.py — Perplexity driver
avvia_edge_debug.bat — lancia Edge su porta 9222
```

---

## Note tecniche
- Playwright sync API: ogni thread usa la propria istanza `sync_playwright()`
- CDP port: `127.0.0.1:9222` (Edge debug)
- Immagini Gemini: salvate come `gemini_img_N.png` nella cartella corrente
- Artifact Claude: salvati come `claude_artifact.html`
