# Indennità ASL Roma 3 Ostia

Estrazione indennità accessorie da cedolino + giorni/ferie da cartellino per i lavoratori ASL Roma 3 Ostia. Metodologia "Sangiovanni" (stesso template e stesse 5 categorie di [[San Giovanni]] — condividono `modello.xlsx`).

## Fonti dati
- Cedolini PDF per lavoratore: `C:\Users\Gianmarco\Documents\ASL ROMA 3 OSTIA\<LAVORATORE>\...`
- Cartellini PDF (giorni lavorati + ferie) nella stessa cartella per lavoratore
- Log elaborazione: `LOG_ELABORAZIONE_ROMA3.txt` (35 lavoratori processati, segnala formati cartellino non riconosciuti per alcuni, es. FERLITO CLAUDIA)

## Script
- `C:\Users\Gianmarco\Python\elabora_roma3.py` — script attivo/definitivo (più recente e completo di `aslroma3ostia.py`, che resta come versione precedente più semplice senza parsing ZIP/7z ricorsivo)
- `PATH_INPUT = C:\Users\Gianmarco\Documents\ASL ROMA 3 OSTIA`
- `PATH_OUTPUT = C:\Users\Gianmarco\Documents\ELABORATI_ROMA3`
- `MODELLO_EXCEL = C:\Users\Gianmarco\Documents\sangiovanni\modello.xlsx` (template condiviso con San Giovanni)

## Criteri di assegnazione/maturazione buono pasto
N/A — Roma3 riguarda solo indennità accessorie, non buoni pasto.

## Criteri di ricerca indennità da cedolino
- **5 categorie** (colonne B-F, identiche a [[San Giovanni]]):

| Colonna | Codici cedolino |
|---|---|
| B | `292C`, `291C` |
| C | `219C`, `218C`, `1861C`, `1862C` |
| D | `213C`, `1011C` |
| E | `239C`, `241C`, `233C`, `1012C` |
| F | `294C`, `293C` |

- **Giorni lavorati** (da cartellino): righe con pattern `^\d{2}\s+(LU|MA|ME|GI|VE|SA|DO)` + timbratura `[EU]\d{2}[:.]\d{2}`
- **Ferie**: pattern `DFER` nel cartellino
- **Offset competenza**: RATA (mese pagamento) → competenza = mese precedente (es. RATA gennaio 2021 → competenza dicembre 2020), salvo riga con suffisso "Rif MM/YY" che indica competenza esplicita diversa
- **Esclusioni**: tredicesima ignorata; importi > `MAX_INDENNITA = 2500.0` EUR segnalati come anomalia da verificare manualmente

## Output desiderato
File riepilogativo annuale per lavoratore con le 5 indennità mese per mese + giorni lavorati/ferie da cartellino, per supportare vertenza retributiva.

## Formato output
- File per lavoratore: `{LAVORATORE}.xlsx`, basato su copia di `modello.xlsx` per ogni anno
- Foglio: righe = mesi (1-12) + riga TOTALE ANNO; colonne: Mese, Indennità B-F (importi EUR), Giorni lavorati, Ferie
- Log mancanti/anomalie: `LOG_ELABORAZIONE_ROMA3.txt`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata. 35 lavoratori già elaborati in precedenza (vedi log), alcuni con cartellino in formato non riconosciuto da verificare.
