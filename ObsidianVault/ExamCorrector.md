---
tags: [progetto, python, tkinter, docente]
---
# ExamCorrector

App desktop Python/tkinter per la correzione automatica di esami a risposta multipla (A/B/C).

## Funzionalità principali
- **Tab 1 — Configura Esame**: imposta nome, N domande, scala voto (30/10/100/personalizzato), soglia %, alternative (A-B / A-B-C / A-B-C-D / A-B-C-D-E). Importa risposte corrette da PDF marksheet QBGenerator (PyMuPDF + pdfplumber). Salva/carica config JSON. Genera modulo HTML per studenti (alternativa web a student_form.py).
- **Tab 2 — Correggi Esami**: carica cartella JSON studenti, correzione batch, classifica colorata (verde/rosso), export CSV/Excel voti, report per studente (Excel). Drag-and-drop.
- **Tab 3 — Statistiche**: KPI summary cards colorate (N studenti, media, mediana, dev std, % idonei), distribuzione voti (matplotlib), % errori per domanda, export Item Analysis/KPI Excel, stampa PDF (reportlab).
- **student_form.py**: modulo risposta studenti (tkinter), alternativa locale all'HTML. Salva JSON con chiave `name`.

## Path
- `C:\Users\Gianmarco\exam_corrector\`
- EXE generato con PyInstaller: `dist/ExamCorrector.exe`

## Stack
Python 3.x, tkinter/ttk, PyMuPDF (fitz), pdfplumber, openpyxl, matplotlib, reportlab, windnd (drag-and-drop Windows)

## Miglioramenti UI (2026-06-26)
- **Header**: doppia riga titolo+subtitle, si aggiorna con l'esame caricato
- **Griglia risposte (Tab 1)**: numero con badge navy, pulsanti A/B/C in stile toggle (blu chiaro → blu navy quando selezionato)
- **KPI cards (Tab 3)**: 5 card colorate (Studenti / Media / Mediana / Dev std / Idonei %) sopra grafici e testo statistico
- **student_form.py**: redesign completo con ttk, Segoe UI, header navy, progress counter live, stile coerente con main.py
- **Bug fix**: grader ora legge `name` e `student_name` come fallback (era solo `name`); file detection accetta entrambe le chiavi

## Timer esame (2026-06-26)
Campo `duration_minutes` (Spinbox, 0 = nessun timer) in Tab 1 → salvato in `exam_info.json` e nel config JSON.

**Flusso studente (sia student_form.py che HTML):**
1. Schermata dati: inserisci nome → "Avvia Esame"
2. Il countdown parte nel header (nave blu); warning giallo <5 min, rosso <1 min
3. A zero: auto-salva il file JSON con `"auto_saved": true` e mostra dialogo
4. "Salva Risposte" manuale ferma il timer

**Note implementative:**
- `HTML_TEMPLATE` usa `__PLACEHOLDER__` invece di `{format}` per evitare l'escaping `{{}}` in JS/CSS
- Il timer usa `root.after(1000, _tick)` in tkinter, `setInterval` in HTML
- `_timer_active[0]` (lista mutable) per stoppar il tick da closure senza `nonlocal`

## Idee per sviluppi futuri
- **KPI cross-sessione**: SQLite locale che accumula risultati sessione per sessione; Tab 3 aggiunge un grafico di trend (media voto, % idonei nel tempo)
- **QBGenerator multi-variante**: carica N marksheet PDF (uno per variante A/B/C/...); studente seleziona la propria variante nel form; grader usa la chiave giusta per ognuno — utile se QBGenerator genera copie con domande rimescolate per anticopying
- **Watch folder**: monitora cartella per nuovi PDF QBGenerator → auto-import risposte
- **Importa risposte da Excel** invece di solo PDF
- **Report PDF per singolo studente** (per invio email) — reportlab già disponibile
- **OCR webcam per fogli cartacei** (OpenCV)
- **Correzione penalità** (−0.5 per sbagliata)
