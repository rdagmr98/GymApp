import os
import re
import sys
import pathlib
import fitz
from pptx import Presentation

sys.stdout.reconfigure(encoding="utf-8")

SRC = pathlib.Path(__file__).resolve().parent
ROOT = SRC.parent
CACHE_DIR = SRC / "_pptx_cache"
PPTX_DIR = ROOT / "pptx"
MASTER_PPTX = ROOT / "MTG_Slide.pptx"

# Simboli/parole vietate dal §4
BANNED_PDF = [r"\\", "dot", "frac", "mathrm", "sqrt"]
# Nel PPTX le parole vietate dal §4:
BANNED_PPTX_EXACT = [r"\\", "frac", "mathrm", "sqrt", "{", "}"]
# Cerca '\dot', 'dot' isolato, o 'dot' seguito da variabile matematica, escludendo parole del dizionario italiano (dotat*, dotaz*)
RE_DOT_PPTX = re.compile(r"(?:\\dot\b|\bdot\b|\bdot\s+[a-zA-Z_]|\bdot(?!(?:at|az))[a-zA-Z_])", re.IGNORECASE)

errors_found = 0
pdf_checked = 0
pptx_checked = 0

print("=" * 70)
print("GATE DI CONTROLLO FORMULE E TESTO PPTX (§4 UNINETTUNO M15 REGOLE)")
print("=" * 70)

# 1. Controllo dei PDF delle formule compilate in CACHE_DIR
print("\n--- 1. CONTROLLO TESTO ESTRATTO DAI PDF DELLE FORMULE ---")
pdf_files = sorted(CACHE_DIR.glob("single_*.pdf"))
if not pdf_files:
    print("ATTENZIONE: Nessun file PDF di formula trovato in CACHE_DIR!")
else:
    for pdf_path in pdf_files:
        pdf_checked += 1
        try:
            doc = fitz.open(str(pdf_path))
            text = "".join(page.get_text() for page in doc)
            doc.close()
            
            for b in BANNED_PDF:
                if b in text:
                    print(f"[ERRORE PDF] {pdf_path.name} contiene '{b}':")
                    for line in text.splitlines():
                        if b in line:
                            print(f"   -> {line.strip()}")
                    errors_found += 1
        except Exception as e:
            print(f"[ERRORE LETTURA] {pdf_path.name}: {e}")
            errors_found += 1

print(f"PDF formule verificati: {pdf_checked}")

# 2. Controllo dei file PowerPoint (.pptx)
print("\n--- 2. CONTROLLO TESTO SLIDE E NOTE PPTX ---")
pptx_list = sorted(PPTX_DIR.glob("*.pptx"))
if MASTER_PPTX.exists():
    pptx_list.append(MASTER_PPTX)

for p_path in pptx_list:
    pptx_checked += 1
    fname = p_path.name
    try:
        prs = Presentation(str(p_path))
    except Exception as e:
        print(f"[ERRORE APERTURA PPTX] {fname}: {e}")
        errors_found += 1
        continue
    
    for idx, slide in enumerate(prs.slides, start=1):
        # Shape e tabelle
        shapes_text = []
        for s in slide.shapes:
            if s.has_text_frame:
                shapes_text.append(s.text_frame.text)
            if s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        shapes_text.append(cell.text)
        slide_body = "\n".join(shapes_text)
        
        # Note oratore
        notes_body = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notes_body = slide.notes_slide.notes_text_frame.text
            
        # Verifica slide
        for b in BANNED_PPTX_EXACT:
            if b in slide_body:
                print(f"[ERRORE PPTX SLIDE] {fname} Slide {idx} contiene '{b}':")
                for line in slide_body.splitlines():
                    if b in line:
                        print(f"   -> {line.strip()[:100]}")
                errors_found += 1
        m_dot = RE_DOT_PPTX.search(slide_body)
        if m_dot:
            print(f"[ERRORE PPTX SLIDE] {fname} Slide {idx} contiene 'dot' anomalo ('{m_dot.group(0)}'):")
            for line in slide_body.splitlines():
                if RE_DOT_PPTX.search(line):
                    print(f"   -> {line.strip()[:100]}")
            errors_found += 1

        # Verifica note
        for b in BANNED_PPTX_EXACT:
            if b in notes_body:
                print(f"[ERRORE PPTX NOTE] {fname} Slide {idx} NOTE contiene '{b}':")
                for line in notes_body.splitlines():
                    if b in line:
                        print(f"   -> {line.strip()[:100]}")
                errors_found += 1
        m_dot_n = RE_DOT_PPTX.search(notes_body)
        if m_dot_n:
            print(f"[ERRORE PPTX NOTE] {fname} Slide {idx} NOTE contiene 'dot' anomalo ('{m_dot_n.group(0)}'):")
            for line in notes_body.splitlines():
                if RE_DOT_PPTX.search(line):
                    print(f"   -> {line.strip()[:100]}")
            errors_found += 1

print(f"File PPTX verificati: {pptx_checked}")

print("\n" + "=" * 70)
if errors_found == 0:
    print("ESITO GATE: SUCCESSO (0 errori rilevati)")
    print("=" * 70)
    sys.exit(0)
else:
    print(f"ESITO GATE: FALLITO ({errors_found} errori rilevati)")
    print("=" * 70)
    sys.exit(1)
