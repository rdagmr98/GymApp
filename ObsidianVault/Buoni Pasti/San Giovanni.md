# Indennità San Giovanni

Estrazione indennità accessorie da cedolino + giorni/ferie da cartellino per i lavoratori dell'Ospedale San Giovanni. È la metodologia ORIGINALE da cui prende nome "Sangiovanni" — il `modello.xlsx` di questa cartella è il template riusato anche per [[Roma3]] e per [[Lazio]] (quest'ultima con 2 colonne indennità aggiuntive, G/H).

## Fonti dati
- Cedolini + cartellini PDF per lavoratore in `C:\Users\Gianmarco\Documents\sangiovanni\OUTPUT_FINALE\<LAVORATORE>\`

## Script
- Tre varianti in `C:\Users\Gianmarco\Python\`: `sangiovanni.py` (più vecchio, 03/03), `sangiovanniprogramma.py` (24/03, legge PDF con `os.walk` ricorsivo, genera anche report mancanti), `sangiovanniprogrammaversionegianmarco.py` (24/03, stesso giorno — legge PDF con `os.listdir` non ricorsivo, senza report mancanti)
- **Script attivo**: `sangiovanniprogrammaversionegianmarco.py` (variante esplicitamente personalizzata da Gianmarco — nome del file) — ma non è confermato al 100% che sia quella effettivamente usata per l'ultimo run reale; se in dubbio confrontare con l'utente prima di rielaborare dati esistenti
- `BASE_PATH = C:\Users\Gianmarco\Documents\sangiovanni\OUTPUT_FINALE`
- `OUTPUT_PATH = C:\Users\Gianmarco\Documents\sangiovanni\ELABORATI`
- Template: `C:\Users\Gianmarco\Documents\sangiovanni\modello.xlsx`

## Criteri di assegnazione/maturazione buono pasto
N/A — San Giovanni riguarda solo indennità, non buoni pasto.

## Criteri di ricerca indennità da cedolino
- **5 categorie** (colonne B-F — stessi codici di [[Roma3]]):

| Colonna | Codici cedolino |
|---|---|
| B | `292C`, `291C` |
| C | `219C`, `218C`, `1861C`, `1862C` |
| D | `213C`, `1011C` |
| E | `239C`, `241C`, `233C`, `1012C` |
| F | `294C`, `293C` |

- **Giorni lavorati** (da cartellino): pattern `^\d{2}\s+(LU|MA|ME|GI|VE|SA|DO)` + timbratura `[EU]\d{2}[:.]\d{2}`
- **Ferie**: stringa `FER` nella riga cartellino
- **Offset competenza**: identico a Roma3 — RATA mese N → competenza mese N-1, salvo override esplicito "Rif MM/YY" nella riga
- Tracciamento per `(anno, mese)` tramite dizionario `vpm` per gestire competenze multiple sullo stesso cedolino

## Output desiderato
File riepilogativo annuale per lavoratore con le 5 indennità mese per mese + giorni/ferie da cartellino, base metodologica poi riusata per Roma3 e Lazio.

## Formato output
- File per lavoratore: `{LAVORATORE}.xlsx`, da template `modello.xlsx`
- Foglio unico: righe = mesi, colonne = indennità B-F + giorni lavorati + ferie (stessa struttura di [[Roma3]])

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata. Da chiarire con l'utente quale delle 3 varianti script è effettivamente quella "in uso" per eventuali rielaborazioni future.
