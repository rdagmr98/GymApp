# Buoni Pasto Tivoli

Elaborazione buoni pasto maturati vs erogati per i lavoratori ASL RMG (Tivoli), per vertenza di recupero retributivo.

## Fonti dati
- Cartellini PDF per lavoratore, 3 formati supportati: OLD ("AZIENDA USL RMG - Cartellino contratto Sanitario"), NEW ("Cartellino Orario", dal 2023), CART ("STAMPA CARTELLINO", formato Cittadella)
- Cedolini PDF per i buoni erogati (quando non presenti sul cartellino stesso)

## Script
- `C:\Users\Gianmarco\Documents\tivoli\analisi_tivoli.py` — motore di parsing: detection formato, estrazione timbrature (gestisce anche testo RTL invertito e split-row con tolleranza 6px), calcolo maturato/erogato/Δ
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli09072026.py` — driver attuale (sostituisce `analizza_tivoli08072026.py`). Stessa struttura, con l'aggiunta di un filtro esplicito `__MACOSX`/`._...` in `collect_pdfs_recursive()` per scartare a monte i resource-fork AppleDouble presenti negli zip creati su macOS (evita errori di parsing spuri).
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli08072026.py` — versione precedente. Stessa struttura (carry-forward da singolo DEFINITIVO sorgente + `process_worker()`), con `pdf_paths` reintrodotto da `analizza_tivoli01072026.py` per i PDF singoli fuori zip.
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli02072026.py` — versione precedente. Carry-forward semplificato (singolo DEFINITIVO sorgente, solo copia file), stesso `process_worker()` riusato.
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli01072026.py` — versione precedente (unifica due archivi, 213 lavoratori). Aggiunge: merge carry-forward da due DEFINITIVI distinti (risolve il problema dei due bacini separati), supporto file `.7z` via `py7zr.extractall()` in `collect_pdfs_recursive()`, parametri `base_records` (baseline pre-calcolata) e `pdf_paths` (PDF singoli fuori zip) in `process_worker()`.
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli23062026.py` — versione precedente (31 lavoratori, secondo archivio Downloads).

## Criteri di assegnazione/maturazione buono pasto
- **Soglia minima**: 6h15m = 375 minuti di ore lavorate nel giorno
- Giorno qualifica se ore lavorate (da timbrature, anche ricostruite se manca il valore colonna "Lav.") superano la soglia
- **Buoni erogati**: letti direttamente dal PDF (cartellino o cedolino) via regex su "Buoni Pasto Salvo Conguaglio"
- **Valore buono**: 4.13 EUR — **0.5 ore** equivalenti

## Criteri di ricerca indennità da cedolino
N/A — Tivoli riguarda solo buoni pasto, nessuna indennità accessoria viene cercata.

## Output desiderato
Confronto buoni MATURATI (da soglia 6h15m sui cartellini) vs buoni EROGATI (da cedolino/cartellino) per quantificare il debito residuo (Δ) ai fini di vertenza.

## Formato output
- File per lavoratore: `{LAVORATORE}.xlsx` — foglio "Riepilogo" + un foglio per anno (righe giornaliere: Mese, Giorno, GG, Lavorato, Qualifica, Maturato, Erogato, Δ, Note; riga "TOTALE MESE")
- Δ = `MAX(0, Maturato - Erogato)`; EUR da recuperare = Δ × 4.13; Ore da recuperare = Erogati × 0.5
- File aggregato: `RIEPILOGO_BUONI_PASTO.xlsx`, foglio "Riepilogo Generale" (righe=lavoratori, colonne=anni, TOTALE Δ/EUR/Ore)
- Consegna finale: ZIP `tivoli09072026_DEFINITIVO.zip`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-07-09: **1 nuovo lavoratore**. **CRICCHI ALESSANDRA** (Matricola 0000061038, A.06M LABORATORIO ANALISI TIVOLI) — del tutto nuova, zip esterno con 2 zip annidati (Cartellini-2015-2024.zip + Cartellini-2025.zip) pesantemente inquinati da garbage `__MACOSX`/`._...` (~130 entry spurie filtrate esplicitamente in `collect_pdfs_recursive`, 0 errori di parsing residui); identità verificata via Matricola+reparto su PDF sia OLD (2017) che NEW (2025) format per risolvere l'ambiguità del nome file (`cricchialessandrativoli` → poteva leggersi "Alessandro", confermato invece "ALESSANDRA" femminile; nessun conflitto con l'omonimo per cognome `CERCHI ALESSANDRO` già in archivio, persona diversa). 132 PDF → 133 mesi 2015-2025, delta 1577 (6.513,01 EUR). Risultato: **219 lavoratori**, RIEPILOGO 2013-2026, **218.831 buoni Δ = 903.772,03 EUR**, 64.454 erogati. Script: `analizza_tivoli09072026.py` (commit `4695637`). Output: `Downloads\tivoli09072026_output\` + `Downloads\tivoli09072026_DEFINITIVO.zip`.
- 2026-07-08: 3 nuovi lavoratori (DI CENSI LORETTA, MARIANI ALESSANDRO, TANTARI VANESSA). Risultato: 218 lavoratori, 217.254 buoni Δ = 897.259,02 EUR. Dettaglio completo in cronologia git della nota (commit `b8e4056`).
- Sessioni precedenti (2026-07-02 → 215 lavoratori/883.423,52 EUR; 2026-07-01 unificazione due archivi → 213 lavoratori/870.380,98 EUR; 2026-06-23 primi 31 lavoratori → 122.966,62 EUR): dettaglio in cronologia git della nota.
- Nota: il path nella tabella "Script principali" di [[Pipeline]] era stale (puntava a `C:\Users\Gianmarco\` root con nomi `analizza_tivoli12062026.py`) — i file reali sono in `Documents\tivoli\`, aggiornato in sessione 2026-07-01.
