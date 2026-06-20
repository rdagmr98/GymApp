#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrazione VERONA: 7 lavoratori già noti (PDF cumulativi in cartellini/)
+ 96 lavoratori dalla chiavetta USB (E:\\verona, un PDF per mese a cartella).
Stessi criteri di analisi_verona.py (solo buoni pasto maturati, nessun erogato/delta).
"""
import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\Users\Gianmarco\Documents\VERONA")
import analisi_verona as av

USB_ROOT = r"E:\verona"
BACKUP   = os.path.join(av.VERONA_PATH, "riepilogo_buoni_pasto_verona_BACKUP_7lavoratori.xlsx")


def find_worker_pdfs(folder):
    """Tutti i PDF in una cartella lavoratore, saltando le sottocartelle Cedolini/cedolini."""
    found = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if 'cedolin' not in d.lower()]
        for f in files:
            if f.lower().endswith('.pdf'):
                found.append(os.path.join(root, f))
    return found


def main():
    if os.path.exists(av.OUTPUT_EXCEL) and not os.path.exists(BACKUP):
        shutil.copy2(av.OUTPUT_EXCEL, BACKUP)
        print(f"Backup creato: {BACKUP}")

    all_results = []

    print("=" * 60)
    print("[1] Lavoratori già noti (7, PDF cumulativi)")
    print("=" * 60)
    for fname in sorted(os.listdir(av.CARTELLINI_PATH)):
        if not fname.lower().endswith('.pdf'):
            continue
        path = os.path.join(av.CARTELLINI_PATH, fname)
        print(f"\n  Lavoratore: {fname[:-4]}")
        results = av.process_pdf(path)
        all_results.extend(results)
        print(f"    Totale buoni pasto maturati: {sum(r['buoni'] for r in results)}")

    print("\n" + "=" * 60)
    print("[2] Lavoratori dalla chiavetta USB (E:\\verona)")
    print("=" * 60)
    worker_folders = sorted(
        d for d in os.listdir(USB_ROOT) if os.path.isdir(os.path.join(USB_ROOT, d))
    )
    print(f"  Cartelle trovate: {len(worker_folders)}")

    no_data = []
    for i, wf in enumerate(worker_folders, 1):
        wpath = os.path.join(USB_ROOT, wf)
        pdfs = find_worker_pdfs(wpath)
        worker_results = []
        for pdf_path in pdfs:
            try:
                r = av.process_pdf(pdf_path)
            except Exception as e:
                print(f"    ERRORE {pdf_path}: {e}")
                r = []
            worker_results.extend(r)
        if worker_results:
            names = {r['worker'] for r in worker_results}
            total = sum(r['buoni'] for r in worker_results)
            print(f"  [{i}/{len(worker_folders)}] {wf}: {len(pdfs)} PDF, "
                  f"{len(worker_results)} mesi, nomi={names}, buoni={total}")
            all_results.extend(worker_results)
        else:
            print(f"  [{i}/{len(worker_folders)}] {wf}: NESSUN DATO "
                  f"(0 mesi validi su {len(pdfs)} PDF trovati)")
            no_data.append(wf)

    print(f"\n  Cartelle senza dati: {len(no_data)}")
    for wf in no_data:
        print(f"    - {wf}")

    print("\n" + "=" * 60)
    print("[3] Generazione Excel combinato")
    print("=" * 60)
    av.create_excel(all_results)

    grand_total = sum(r['buoni'] for r in all_results)
    workers_set = {r['worker'] for r in all_results}
    print(f"\nLavoratori totali: {len(workers_set)}")
    print(f"Totale buoni pasto maturati: {grand_total}")


if __name__ == '__main__':
    main()
