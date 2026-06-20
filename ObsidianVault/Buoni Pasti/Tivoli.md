# Buoni Pasto Tivoli

Elaborazione buoni pasto maturati vs erogati per i lavoratori ASL RMG (Tivoli), per vertenza di recupero retributivo.

## Fonti dati
- Cartellini PDF per lavoratore, 3 formati supportati: OLD ("AZIENDA USL RMG - Cartellino contratto Sanitario"), NEW ("Cartellino Orario", dal 2023), CART ("STAMPA CARTELLINO", formato Cittadella)
- Cedolini PDF per i buoni erogati (quando non presenti sul cartellino stesso)

## Script
- `C:\Users\Gianmarco\Documents\tivoli\analisi_tivoli.py` — motore di parsing: detection formato, estrazione timbrature (gestisce anche testo RTL invertito e split-row con tolleranza 6px), calcolo maturato/erogato/Δ
- `C:\Users\Gianmarco\Documents\tivoli\analizza_tivoli20062026.py` — driver attuale (sostituisce le versioni datate precedenti: `analizza_tivoli12062026.py`, `analizza_tivoli17062026.py`, ecc. — la cartella contiene molte iterazioni storiche, questa è l'ultima)

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
- Consegna finale: ZIP `tivoli20062026_DEFINITIVO.zip`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata (nessuna nuova elaborazione in questa sessione). Ultima elaborazione reale: 4 nuovi lavoratori (Battisti, Raiola, Lirosi, Lovallo), vedi sessione 2026-06-20 in `_CLAUDE.md`.
- Nota: il path nella tabella "Script principali" di [[Pipeline]] era stale (puntava a `C:\Users\Gianmarco\` root con nomi `analizza_tivoli12062026.py`) — i file reali sono in `Documents\tivoli\`, aggiornato in questa sessione.
