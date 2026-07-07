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
| tutto il resto | **Tutti e 3 in parallelo** |

> PPT/slide rimosso: Claude.ai richiede Pro per artifacts — non gratis.

```powershell
ai.bat "genera un logo"              # → Gemini
ai.bat "cos'è il SQL injection"      # → Perplexity + Gemini + Claude parallelo
ai.bat "..." -p all                  # forza tutti e 3
ai.bat "..." -p claude               # forza provider specifico
ai.bat "..." -r                      # abilita Reasoning/Thinking
ai.bat "..." --out note.md           # salva output su file
ai.bat --batch "task1" "task2" "task3"  # task diversi in parallelo
```

---

## In Claude Code (risparmio token)

Quando l'utente dice "usa meno crediti" o "risparmia token":

```bash
! cd C:\Users\Gianmarco\aiTool && ai.bat "prompt" --out risposta.md
# poi leggi: Read C:\Users\Gianmarco\aiTool\risposta.md
```

---

## Immagini per il materiale didattico CAAE (policy — deciso 2026-06-29)
Per i PDF dell'MTO (documento controllato, AER(EP).P-147):
1. **Schemi/diagrammi tecnici** (architetture, principi, catene funzionali) → li genera **Claude/Opus con matplotlib** (raster, mai ASCII). Non delegati a Sonnet.
2. **Foto reali** → solo da fonti **libere e senza watermark**, in quest'ordine di preferenza:
   - **Wikimedia Commons** (CC / pubblico dominio) — API `https://commons.wikimedia.org/w/api.php`
   - **DVIDS** `dvidshub.net` (immagini DoD, pubblico dominio)
   - foto PA militari / Difesa con licenza compatibile
   Claude scarica il **file originale pulito** (curl / Invoke-WebRequest) in `_engine\figcache\`.
3. **NO Getty Images / Shutterstock**: le anteprime sono **watermarkate** e a **licenza a pagamento** → inutilizzabili in un documento ufficiale.
4. Le foto reali libere sono la **scelta preferita**; se non si trova nulla di adatto → Claude genera lo schema con matplotlib (come moduli 50/51).
5. Gemini (via aiTool) si usa per **individuare** le immagini candidate e le loro fonti, non per scaricare watermark.

## Chiedere a Gemini e copiare (risparmio token — contenuti)
Per bozze/ricerca lunga senza bruciare token API:
```powershell
! cd C:\Users\Gianmarco\aiTool && ai.bat "prompt di ricerca o bozza" --out risposta.md
```
Poi `Read risposta.md` e Claude **integra/corregge** (accenti à è é ì ò ù, fisica dai fondamenti, vincolo Latin-1 dell'engine). Utile per abbozzare prosa; la correttezza tecnica la rifinisce Claude/Opus.

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
