# Buoni Pasto Cittadella

Elaborazione buoni pasto maturati vs riconosciuti per i lavoratori dell'Ospedale di Cittadella.

## Fonti dati
- Cartellini PDF per lavoratore, formato "STAMPA CARTELLINO" (2 pagine standard, o multi-pagina se combinati — elaborati pagina per pagina e accumulati per worker/mese/anno)

## Script
- `C:\Users\Gianmarco\Documents\CITTADELLA\analisi_buoni_pasto.py` — unico script, motore + output
- `CITTADELLA\2nuovi\` — stessa metodologia applicata a lavoratori aggiunti successivamente, non una logica diversa

## Criteri di assegnazione/maturazione buono pasto
- **Soglia minima**: `MIN_MINUTES = 375` (6h15m), identica a Tivoli
- Giorno qualifica se **entrambe** le condizioni sono vere:
  1. almeno una timbratura reale rilevata (pattern E/U, es. `E08:16[11]`)
  2. ore lavorate (dopo pulizia timbrature) > 375 minuti
- Sabato/domenica evidenziati graficamente nell'Excel ma non sono criterio di maturazione a sé
- **Buoni erogati**: letti da pagina 2 del cartellino via regex `Buoni Pasto(\d+)`, fallback su pagina 1 se non trovato
- Valore buono non esplicitato nel codice (verosimilmente 4.13 EUR, coerente con Tivoli/Rieti — da confermare se serve per calcolo EUR)

## Criteri di ricerca indennità da cedolino
N/A — Cittadella riguarda solo buoni pasto.

## Output desiderato
Conteggio giorni con turno > 6h15m vs buoni effettivamente riconosciuti, per evidenziare discrepanze/mancate liquidazioni.

## Formato output
- File aggregato: `riepilogo_buoni_pasto.xlsx`, foglio "Riepilogo" (righe=lavoratori, colonne=anni, TOTALE per anno, rosso se debito)
- Un foglio di dettaglio per lavoratore (nome troncato a 31 char): intestazione "Dettaglio Buoni Pasto — {lavoratore}", sezioni per mese (▶ {mese_anno}), righe giornaliere (GG, Giorno, Ore Teor., Ore Lav., "> 6h15?", Timb.?), riga riepilogo mese (Giorni > 6h15 | Buoni riconosciuti | Δ), riga totale complessivo finale

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata.
