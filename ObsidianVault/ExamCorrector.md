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

## Idee per sviluppi futuri
- Timer di esame in student_form.py (countdown configurabile)
- Importa risposte da Excel invece di solo PDF
- Storico sessioni con SQLite (confronto cross-sessione KPI)
- Report PDF per singolo studente (per invio email)
- OCR webcam per fogli cartacei (OpenCV)
- Correzione penalità (−0.5 per sbagliata)
