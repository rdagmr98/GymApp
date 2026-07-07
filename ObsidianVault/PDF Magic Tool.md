---
tags: [progetto, python, tool, pdf]
---
# PDF Magic Tool — Pro Suite

## Cos'è
App desktop Windows per manipolazione PDF, sviluppata in Python con CustomTkinter e tkinterdnd2. Interfaccia dark mode, drag & drop, tutto su thread separato (UI non si blocca).

**Sorgente**: `C:\Users\Gianmarco\Python\pdfconverter.py`
**Versione attuale**: 3.0
**Build**: `C:\Users\Gianmarco\Python\dist\PDF_Magic_Tool_Pro\`
**Installer script**: `C:\Users\Gianmarco\Python\Setup_PDF_Magicpro.iss`
**Password installer**: `osare199`

## Tab e funzioni

### Converti
PDF → `.xlsx` / `.docx` / `.pptx` / `.txt` con traduzione opzionale (Google Translate).
- xlsx: estrae testo riga per riga (fallback tabelle per PDF scan)
- pptx: ricostruisce posizione testi e immagini via PyMuPDF

### Gestisci PDF
| Funzione | Output |
|---|---|
| Unisci PDF | `PDF_UNITO_MAGIC.pdf` nella cartella del primo file |
| Dividi / Estrai pagine | `_pag{da}-{a}.pdf` |
| Comprimi | `_compresso.pdf` — mostra KB prima/dopo e % riduzione |
| Ruota (90/180/270°) | `_ruotato{N}.pdf` |
| Aggiungi password | `_protetto.pdf` |
| Rimuovi password | `_sbloccato.pdf` |

### PDF/A
Converte in PDF/A-1a/1b/2a/2b/3a/3b.
- **Con Ghostscript nel PATH**: piena conformità ISO 19005 (usa `gswin64c`)
- **Senza Ghostscript**: PyMuPDF + XMP metadata (conformità parziale)
- Il banner nel tab è verde (GS trovato) o rosso (GS non trovato)
- Output: `_PDFA-{livello}.pdf`

### Immagini
- PDF → immagini: cartella `{nome}_immagini/`, formato PNG/JPEG/WebP, DPI configurabile (default 150)
- Immagini → PDF: assembla PNG/JPG/WebP in `IMMAGINI_PDF_MAGIC.pdf`

## Stack librerie
| Libreria | Uso |
|---|---|
| customtkinter | UI dark mode |
| tkinterdnd2 | Drag & drop |
| PyMuPDF (fitz) | Estrazione testo/immagini, comprimi, PDF→img, img→PDF, PDF/A fitz |
| pdfplumber | Estrazione testo/tabelle per xlsx/docx/txt |
| pypdf | Merge, split, rotate, password |
| pandas | Export xlsx |
| python-docx | Export docx |
| python-pptx | Export pptx |
| deep-translator | Google Translate |
| Pillow | Elaborazione immagini (trasparenza sfondo bianco) |

## Build & distribuzione
```bash
# 1. Build exe (nella cartella Python/)
.venv\Scripts\pyinstaller PDF_Magic_Tool_Pro.spec --noconfirm

# 2. Build installer Inno Setup
"C:\Users\Gianmarco\AppData\Local\Programs\Inno Setup 6\ISCC.exe" Setup_PDF_Magicpro.iss
```
L'installer prodotto è `Python\Output\pdfmagictoolpro.exe`, password `osare199`.

## Note tecniche
- Ghostscript per PDF/A completo: https://ghostscript.com/releases/gsdnld.html → aggiungere `gswin64c` al PATH
- Il regex `pulisci_testo_xml` rimuove caratteri non validi XML (necessario per PPTX)
- Le operazioni lunghe usano `threading.Thread(daemon=True)` + `root.after(0, ...)` per aggiornare la UI dal thread principale

## Cronologia versioni
- v1/v2: conversione PDF base, un solo tab, no threading
- **v3.0** (2026-06-26): 4 tab, progress bar, threading, PDF/A, comprimi, ruota, password, img↔PDF, file list, browse button
