# Buoni Pasto Tivoli

Elaborazione buoni pasto maturati vs erogati per i lavoratori ASL RMG (Tivoli), per vertenza di recupero retributivo.

## Fonti dati
- Cartellini PDF per lavoratore, 3 formati supportati: OLD ("AZIENDA USL RMG - Cartellino contratto Sanitario"), NEW ("Cartellino Orario", dal 2023), CART ("STAMPA CARTELLINO", formato Cittadella)
- Cedolini PDF per i buoni erogati (quando non presenti sul cartellino stesso)

## Script
- `C:\Users\Gianmarco\Documents\tivoli\analisi_tivoli.py` — motore di parsing: detection formato, estrazione timbrature (gestisce anche testo RTL invertito e split-row con tolleranza 6px), calcolo maturato/erogato/Δ
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli08072026.py` — driver attuale (sostituisce `analizza_tivoli02072026.py`). Stessa struttura (carry-forward da singolo DEFINITIVO sorgente + `process_worker()`), con `pdf_paths` reintrodotto da `analizza_tivoli01072026.py` per i PDF singoli fuori zip.
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
- Consegna finale: ZIP `tivoli08072026_DEFINITIVO.zip`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-07-08: **3 nuovi lavoratori** integrati dagli ultimi download in Downloads. **DI CENSI LORETTA** (Matricola 0000050129, CHIRURGIA GENER. E D'URGENZA T): base xlsx pre-esistente nello zip (36 mesi 2023-2025) + cartellino PDF 72 pagine per il residuo 2017-2022, delta 951 (3.927,63 EUR). **MARIANI ALESSANDRO** (Matricola 0000061163, MEDIC URG P.S.Osser Breve MONTEROTONDO): del tutto nuovo, 39 PDF da zip (33 mensili formato NEW 2023-2026 + 1 storico OLD 101 pagine 2015-2023) — verificata Matricola/reparto per escludere confusione con 3 omonimi "ALESSANDRO" già in archivio (AMATO, CERCHI, VENTURINI — persone diverse), 137 mesi 2015-2026, delta 1760 (7.268,80 EUR). **TANTARI VANESSA** (Matricola 0000081464, MEDICINA INTERNA TIVOLI): del tutto nuova, 1 PDF diretto fuori zip (formato misto OLD+NEW nello stesso file, gestito automaticamente dal motore), 58 mesi 2021-2025, delta 637 (2.630,81 EUR). Risultato: **218 lavoratori**, RIEPILOGO 2013-2026, **217.254 buoni Δ = 897.259,02 EUR**, 64.331 erogati. Script: `analizza_tivoli08072026.py` (commit `5edb8d2`). Output: `Downloads\tivoli08072026_output\` + `Downloads\tivoli08072026_DEFINITIVO.zip`.
- 2026-07-02: 2 nuovi lavoratori (TILIA EMANUELA, ABBATI MARIA) + risolta ambiguità identità TILIA/ATTILIA via verifica Matricola+reparto. Risultato: 215 lavoratori, 213.904 buoni Δ = 883.423,52 EUR. Dettaglio completo in `Sessioni/2026-07-02.md` (o cronologia git della nota).
- Sessioni precedenti (2026-07-01 unificazione due archivi → 213 lavoratori/870.380,98 EUR; 2026-06-23 primi 31 lavoratori → 122.966,62 EUR): dettaglio in cronologia git della nota.
- Nota: il path nella tabella "Script principali" di [[Pipeline]] era stale (puntava a `C:\Users\Gianmarco\` root con nomi `analizza_tivoli12062026.py`) — i file reali sono in `Documents\tivoli\`, aggiornato in sessione 2026-07-01.
