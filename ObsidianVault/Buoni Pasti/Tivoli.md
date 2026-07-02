# Buoni Pasto Tivoli

Elaborazione buoni pasto maturati vs erogati per i lavoratori ASL RMG (Tivoli), per vertenza di recupero retributivo.

## Fonti dati
- Cartellini PDF per lavoratore, 3 formati supportati: OLD ("AZIENDA USL RMG - Cartellino contratto Sanitario"), NEW ("Cartellino Orario", dal 2023), CART ("STAMPA CARTELLINO", formato Cittadella)
- Cedolini PDF per i buoni erogati (quando non presenti sul cartellino stesso)

## Script
- `C:\Users\Gianmarco\Documents\tivoli\analisi_tivoli.py` — motore di parsing: detection formato, estrazione timbrature (gestisce anche testo RTL invertito e split-row con tolleranza 6px), calcolo maturato/erogato/Δ
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli02072026.py` — driver attuale (sostituisce `analizza_tivoli01072026.py`). Carry-forward semplificato (singolo DEFINITIVO sorgente, solo copia file), stesso `process_worker()` riusato.
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
- Consegna finale: ZIP `tivoli02072026_DEFINITIVO.zip`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-07-02: **2 nuovi lavoratori + risolta ambiguità identità**. L'utente ha scaricato 2 nuovi zip in Downloads: `tiliaemanuelativoli.zip` e `abbatimariativoli.zip`. Il primo conteneva un nominativo "TILIA EMANUELA" molto simile a un lavoratore già in archivio, "ATTILIA EMANUELA" — dati in conflitto. **Metodo di verifica identità (riusabile)**: invece di assumere errore di battitura, estratto testo (via `fitz`/PyMuPDF) dai PDF sorgente originali di entrambi — cedolino/cartellino di ATTILIA EMANUELA (Matricola 10025, CF TTLMNL67T42B595F, reparto OSTET GINECOLOGIA TIVOLI) vs cartellino di TILIA EMANUELA (Matricola 40585, reparto MEDIC URG P.S.Osser Breve SUBIACO) → confermate **2 persone diverse** (matricola e reparto incompatibili). **TILIA EMANUELA**: nuova all'archivio, base = xlsx nello zip (109 mesi 2016-2023+2025) + 12 mesi PDF 2024, delta 1430 (5.905,90 EUR). **ABBATI MARIA**: del tutto nuova, solo PDF da due zip annidati (`cartellini 24-25.zip` + `cartellini 2023 (2).zip`, 130 PDF, 2015-2025 con 2023 solo gen-ott), delta 1728 (7.136,64 EUR). Risultato: **215 lavoratori**, RIEPILOGO 2013-2026, **213.904 buoni Δ = 883.423,52 EUR**, 63.744 erogati (verificato per quadratura: 883.423,52 − 870.380,98 = 13.042,54 = (1430+1728)×4.13). Script: `analizza_tivoli02072026.py`. Output: `Downloads\tivoli02072026_output\` + `Downloads\tivoli02072026_DEFINITIVO.zip`.
- 2026-07-01: **unificazione due archivi** + 3 nuovi/aggiornati. Scoperto che Tivoli aveva due DEFINITIVI separati: `Documents\tivoli\buonipasto tivoli DEFINITIVO\` (191 lavoratori, primo archivio, "vecchio") e `Downloads\tivoli23062026_output\buonipasto DEFINITIVO\` (31 lavoratori, secondo). Il nuovo script li fonde in un unico bacino (10 worker in overlap mergiati per max maturati). Nuovi: **SILVESTRI PAOLA** (53 mesi base 2019-2023 dal DEF1 + 26 mesi PDF nov 2023-dic 2025, delta 683/2.820,79 EUR), **PAPA ANTONELLA** (51 mesi base 2019-2023 + 22 mesi da file `.7z` interno allo zip feb 2024-nov 2025, delta 819/3.382,47 EUR), **IACHINI SANDRA** (nuova, 64 mesi da PDF diretto 2015-2020, Matricola 0000060341, DISTRETTO MONTEROTONDO, delta 587/2.424,31 EUR). Risultato: **213 lavoratori**, RIEPILOGO 2013-2026, **210.746 buoni Δ = 870.380,98 EUR**, 63.383 erogati. Script: `analizza_tivoli01072026.py` (commit `b92ec00`). Output: `Downloads\tivoli01072026_output\` + `Downloads\tivoli01072026_DEFINITIVO.zip`.
- 2026-06-23: integrati 9 nuovi lavoratori da 6 zip scaricati in Downloads (`Gianmarco tivoli.zip`, `gianmarco tivoli 2.zip`, `Lombardi Delia.zip`, `Panunzi Giovanna.zip`, `TABULATO 2015-2025-1-70 (1).zip`, `TABULATO 2015-2025-71-133.zip`): ROSATI ALESSIO, SALVATI SIMONA, SCALABRINO FABIOLA JOSEFINA, TANONI TERESA, BUGARA ZUZANNA MARIA, GENNARI MARIA CHIARA, LOMBARDI DELIA, PANUNZI GIOVANNA, MARRACCINI CINZIA (lavoratrice del tutto nuova all'archivio, scoperta dai due TABULATO — Matricola 0000010604, reparto ORTOP TRAUMATOLOGIA TIVOLI, 133 mesi 2015-2025 da 2 PDF da 70+63 pagine). Scalabrino e Tanoni avevano XLSX storico pre-esistente nello zip (dual-source, merge per (anno,mese) con priorità al maturati più alto in caso di conflitto — stesso pattern già usato per Battisti). Due zip (`Gianmarco tivoli`/`gianmarco tivoli 2`) contenevano più lavoratori come sottocartelle sorelle, non zip annidati: gestito con `path_filter` per-lavoratore su `collect_pdfs_recursive`. Risultato: 31 lavoratori totali, RIEPILOGO 2013-2026, totale 29.774 buoni Δ = 122.966,62 EUR da recuperare, 11.178 erogati. Script: `analizza_tivoli23062026.py` (committato, solo lo script — niente dati grezzi/output in git, pattern consolidato). Output: `Downloads\tivoli23062026_output\` + `Downloads\tivoli23062026_DEFINITIVO.zip`.
- Nota: il path nella tabella "Script principali" di [[Pipeline]] era stale (puntava a `C:\Users\Gianmarco\` root con nomi `analizza_tivoli12062026.py`) — i file reali sono in `Documents\tivoli\`, aggiornato in questa sessione.
