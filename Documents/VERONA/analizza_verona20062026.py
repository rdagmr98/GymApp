#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrazione VERONA: 7 lavoratori già noti (PDF cumulativi in cartellini/)
+ 96 lavoratori dalla chiavetta USB (E:\\verona, un PDF per mese a cartella).
Stessi criteri di analisi_verona.py (solo buoni pasto maturati, nessun erogato/delta).
"""
import os, sys, shutil, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"C:\Users\Gianmarco\Documents\VERONA")
import analisi_verona as av

USB_ROOT = r"E:\verona"
BACKUP   = os.path.join(av.VERONA_PATH, "riepilogo_buoni_pasto_verona_BACKUP_7lavoratori.xlsx")


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def find_worker_pdfs(folder):
    """Tutti i PDF in una cartella lavoratore, saltando le sottocartelle Cedolini/cedolini.
    Esclude duplicati byte-identici (stesso file esportato più volte, es. *_2.pdf)."""
    found = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if 'cedolin' not in d.lower()]
        for f in files:
            if f.lower().endswith('.pdf'):
                found.append(os.path.join(root, f))

    seen_hashes = {}
    unique = []
    for path in found:
        h = _md5(path)
        if h in seen_hashes:
            print(f"    DUPLICATO IGNORATO (identico a {os.path.basename(seen_hashes[h])}): {path}")
            continue
        seen_hashes[h] = path
        unique.append(path)
    return unique


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
    all_conflicts = []
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

        # Dedup semantico: stesso (worker, anno, mese) con stesse identiche righe
        # giorno-per-giorno (es. mese ristampato in date diverse -> bytes diversi,
        # MD5 diverso, ma dato reale identico). Se le righe differiscono per la
        # stessa chiave è un conflitto vero (dati diversi): si tiene quello con
        # più buoni (più giorni con timbratura reale), l'altro è uno snapshot
        # parziale preso prima che i dati fossero completati nel sistema.
        # Le entry con details vuoti sono pagine di spillover (continuazione
        # indennità senza dati orari, sempre buoni=0): non sono conflitti.
        deduped = {}
        for r in worker_results:
            key = (r['worker'], r['year'], r['month'])
            sig = tuple(
                (d['day'], d['dow'], d['turno'], d['worked'], d['qualifies'],
                 d.get('entry', ''), d.get('exit', ''), d.get('duration_hm', ''),
                 d.get('note', ''))
                for d in r['details']
            )
            if key in deduped:
                prev_r, prev_sig = deduped[key]
                if not r['details']:
                    continue  # spillover vuoto, nessun dato reale da confrontare
                if not prev_r['details']:
                    deduped[key] = (r, sig)  # prev era lo spillover vuoto
                    continue
                if prev_sig != sig:
                    all_conflicts.append(key)
                    if r['buoni'] > prev_r['buoni']:
                        print(f"    CONFLITTO DATI per {key}: due PDF con dati diversi, "
                              f"tenuto quello con più buoni ({r['buoni']} > {prev_r['buoni']})")
                        deduped[key] = (r, sig)
                    else:
                        print(f"    CONFLITTO DATI per {key}: due PDF con dati diversi, "
                              f"tenuto quello con più buoni ({prev_r['buoni']} >= {r['buoni']})")
                else:
                    print(f"    DUPLICATO SEMANTICO IGNORATO per {key} "
                          f"(stesso mese ristampato, dati identici)")
                continue
            deduped[key] = (r, sig)
        worker_results = [v[0] for v in deduped.values()]

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

    print(f"\n  Conflitti dati (stesso mese, dati diversi tra due PDF): {len(all_conflicts)}")
    for key in all_conflicts:
        print(f"    - {key}")

    print("\n" + "=" * 60)
    print("[3] Controllo finale duplicati su tutto il dataset")
    print("=" * 60)
    from collections import Counter
    final_keys = Counter((r['worker'], r['year'], r['month']) for r in all_results)
    final_dups = {k: n for k, n in final_keys.items() if n > 1}
    if final_dups:
        print(f"  ATTENZIONE: {len(final_dups)} chiavi (worker, anno, mese) duplicate residue:")
        for k, n in final_dups.items():
            print(f"    - {k}: {n} occorrenze")
    else:
        print("  OK: nessuna chiave (worker, anno, mese) duplicata.")

    print("\n" + "=" * 60)
    print("[4] Generazione Excel combinato")
    print("=" * 60)
    av.create_excel(all_results)

    grand_total = sum(r['buoni'] for r in all_results)
    workers_set = {r['worker'] for r in all_results}
    print(f"\nLavoratori totali: {len(workers_set)}")
    print(f"Totale buoni pasto maturati: {grand_total}")


if __name__ == '__main__':
    main()
