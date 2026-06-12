#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Processa TIVOLI 12062026: integra nuovi cartellini negli Excel esistenti (11062026).
Logica:
  - Cerca Excel esistente in tivoli11062026/buonipasto DEFINITIVO/{LAVORATORE}.xlsx
  - Legge i mesi già presenti nell'Excel esistente
  - Processa i PDF nel ZIP (tutti i formati: OLD, OLD_REV, NEW)
  - Aggiunge solo i mesi NUOVI (non già presenti) all'Excel
  - Se nessun Excel esistente: crea da zero con tutti i dati trovati
  - Supporta formato invertito RTL (Meucci 2013-2022)
"""
import os, sys, re, zipfile, io, tempfile
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"C:\Users\Gianmarco\Documents\tivoli")
import analisi_tivoli, openpyxl

DOWNLOADS    = r"C:\Users\Gianmarco\Downloads"
ZIP_DIR      = os.path.join(DOWNLOADS, "tivoli12062026")
EXISTING_DIR = os.path.join(DOWNLOADS, "tivoli11062026", "buonipasto DEFINITIVO")
OUT_ROOT     = os.path.join(DOWNLOADS, "tivoli12062026_output")
DEFINITIVO   = os.path.join(OUT_ROOT, "buonipasto DEFINITIVO")
OUT_ZIP      = os.path.join(DOWNLOADS, "tivoli12062026_DEFINITIVO.zip")

BUONO_ORE  = 0.5
BUONO_EURO = 4.13

MONTH_ABBR = {'Gen':1,'Feb':2,'Mar':3,'Apr':4,'Mag':5,'Giu':6,
              'Lug':7,'Ago':8,'Set':9,'Ott':10,'Nov':11,'Dic':12}

os.makedirs(DEFINITIVO, exist_ok=True)
analisi_tivoli.OUTPUT_DIR = DEFINITIVO
analisi_tivoli.LOG_FILE   = os.path.join(OUT_ROOT, "pdf_non_leggibili.log")
os.makedirs(OUT_ROOT, exist_ok=True)
with open(analisi_tivoli.LOG_FILE, 'w', encoding='utf-8') as f:
    f.write('PDF NON LEGGIBILI - Tivoli 12062026\n\n')


# ── Legge maturati/erogati dall'Excel esistente ───────────────────────────────

def read_existing_excel(xlsx_path, worker_name):
    """Ritorna lista record {year, month, maturati, erogati, details=[]} dal file esistente."""
    records = []
    try:
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        for sn in wb.sheetnames:
            try:
                year = int(sn)
            except ValueError:
                continue
            ws = wb[sn]
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[1] == 'TOTALE MESE':
                    mese = row[0]
                    mat  = row[5]
                    ero  = row[6]
                    if mese in MONTH_ABBR:
                        records.append({
                            'worker': worker_name,
                            'year': year,
                            'month': MONTH_ABBR[mese],
                            'maturati': int(mat) if isinstance(mat, (int, float)) else 0,
                            'erogati': int(ero) if isinstance(ero, (int, float)) else 0,
                            'erogati_found': True,
                            'details': [],
                        })
        wb.close()
    except Exception as e:
        print(f"  ⚠ Errore lettura Excel esistente {os.path.basename(xlsx_path)}: {e}")
    return records


# ── Legge erogati dall'XLSX dentro il ZIP ────────────────────────────────────

def read_erogati_from_zip_xlsx(xlsx_bytes):
    """Ritorna {(year, month): erogati} dai fogli anno dell'XLSX nel ZIP."""
    result = {}
    try:
        wb = openpyxl.load_workbook(io.BytesIO(xlsx_bytes), read_only=True, data_only=True)
        for sn in wb.sheetnames:
            try:
                year = int(sn)
            except ValueError:
                continue
            ws = wb[sn]
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[1] == 'TOTALE MESE':
                    mese = row[0]
                    ero  = row[6]
                    if mese in MONTH_ABBR and isinstance(ero, (int, float)) and ero > 0:
                        result[(year, MONTH_ABBR[mese])] = int(ero)
        wb.close()
    except Exception:
        pass
    return result


# ── Processa un outer ZIP ─────────────────────────────────────────────────────

def collect_pdfs_from_zip(zf):
    """Raccoglie tutti i PDF da un ZipFile (ricorsivo su un livello di inner ZIP)."""
    names = zf.namelist()
    pdf_bytes = {}
    # PDF diretti
    for n in names:
        if n.lower().endswith('.pdf'):
            pdf_bytes[n] = zf.read(n)
    # Inner ZIP (un solo livello)
    for n in names:
        if n.lower().endswith('.zip'):
            try:
                inner_data = zf.read(n)
                with zipfile.ZipFile(io.BytesIO(inner_data)) as inner:
                    for pn in inner.namelist():
                        if pn.lower().endswith('.pdf'):
                            key = f"{n}/{pn}"
                            pdf_bytes[key] = inner.read(pn)
            except Exception:
                pass
    return pdf_bytes


def process_worker_zip(zip_path):
    fname = os.path.basename(zip_path)
    print(f"\n{'='*60}\n{fname}")

    try:
        with zipfile.ZipFile(zip_path) as outer:
            names = outer.namelist()

            # Nome canonico dal file XLSX nel ZIP
            xlsx_names = [n for n in names if n.lower().endswith('.xlsx')]
            if xlsx_names:
                worker_name = os.path.splitext(os.path.basename(xlsx_names[0]))[0].strip().upper()
                xlsx_data   = outer.read(xlsx_names[0])
                erogati_map = read_erogati_from_zip_xlsx(xlsx_data)
            else:
                worker_name = None
                erogati_map = {}

            pdf_bytes = collect_pdfs_from_zip(outer)

    except Exception as e:
        print(f"  ERRORE apertura ZIP: {e}")
        return None

    if not pdf_bytes:
        print("  SKIP: nessun PDF trovato")
        return None

    print(f"  Lavoratore: {worker_name or '(da PDF)'}  |  PDF: {len(pdf_bytes)}")

    # Processa tutti i PDF
    new_records = []
    for pname, pdata in sorted(pdf_bytes.items()):
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(pdata); tmp = f.name
        try:
            recs = analisi_tivoli.process_pdf(tmp)
        except Exception as e:
            print(f"    ERRORE {os.path.basename(pname)}: {e}")
            recs = []
        finally:
            os.unlink(tmp)

        for r in recs:
            if worker_name:
                r['worker'] = worker_name
            # Prendi erogati dall'XLSX se presenti e i PDF non li hanno
            key = (r['year'], r['month'])
            if not r.get('erogati_found') and key in erogati_map:
                r['erogati'] = erogati_map[key]
                r['erogati_found'] = True
        new_records.extend(recs)

    # Se non c'era XLSX, prendi nome dal record più frequente nei PDF
    if not worker_name and new_records:
        from collections import Counter as _C
        worker_name = _C(r['worker'] for r in new_records).most_common(1)[0][0]
        print(f"  Nome da PDF: {worker_name}")

    if not new_records:
        print("  SKIP: nessun dato estratto dai PDF")
        return None

    # Statistiche PDF
    new_mat = sum(r['maturati'] for r in new_records)
    new_anni = sorted({r['year'] for r in new_records})
    print(f"  Da PDF: mat={new_mat}  anni={new_anni}")

    # Cerca Excel esistente in tivoli11062026
    existing_path = os.path.join(EXISTING_DIR, f"{worker_name}.xlsx")
    if os.path.exists(existing_path):
        existing_records = read_existing_excel(existing_path, worker_name)
        existing_keys    = {(r['year'], r['month']) for r in existing_records}

        truly_new = [r for r in new_records if (r['year'], r['month']) not in existing_keys]

        if not truly_new:
            print(f"  SKIP: nessun mese nuovo (esistenti: {sorted(existing_keys)})")
            return None

        merged = existing_records + truly_new
        new_ym = sorted({(r['year'], r['month']) for r in truly_new})
        print(f"  Nuovi mesi aggiunti: {new_ym}")
    else:
        merged = new_records
        print(f"  Nessun Excel esistente → nuovo Excel da zero")

    # Crea Excel integrato
    out_path, _ = analisi_tivoli.create_worker_excel(worker_name, merged, DEFINITIVO)

    total_mat = sum(r['maturati'] for r in merged)
    total_ero = sum(r['erogati'] for r in merged)
    delta     = total_mat - total_ero
    anni      = sorted({r['year'] for r in merged})
    print(f"  Salvato: {os.path.basename(out_path)}")
    print(f"  Totale: mat={total_mat} ero={total_ero} delta={delta} ({delta*BUONO_EURO:.2f}€)  anni={anni}")
    return out_path


# ── Main ─────────────────────────────────────────────────────────────────────

print("=" * 60)
print("TIVOLI 12062026 - Integrazione cartellini")
print("=" * 60)

zip_files = sorted(
    os.path.join(ZIP_DIR, f)
    for f in os.listdir(ZIP_DIR)
    if f.lower().endswith('.zip')
)
print(f"ZIP trovati: {len(zip_files)}")

output_files = []
for zf in zip_files:
    out = process_worker_zip(zf)
    if out:
        output_files.append(out)

# ── ZIP finale ────────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"File prodotti: {len(output_files)}")

if output_files:
    print(f"Creazione ZIP: {OUT_ZIP}")
    with zipfile.ZipFile(OUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zout:
        for fp in sorted(output_files):
            zout.write(fp, os.path.basename(fp))
            print(f"  + {os.path.basename(fp)}")
    print(f"ZIP creato: {OUT_ZIP}")
else:
    print("Nessun file da includere nel ZIP.")

print("=" * 60)
print("COMPLETATO.")
