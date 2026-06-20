# Buoni Pasto Verona

Elaborazione buoni pasto maturati per i lavoratori ASL Verona (Az. Osp. Universitaria Integrata).

## Fonti dati
- 7 lavoratori noti con PDF cumulativi: `C:\Users\Gianmarco\Documents\VERONA\cartellini\*.pdf` (un file per lavoratore, tutti i mesi in un unico PDF multi-pagina)
- 96 lavoratori da chiavetta USB: `E:\verona\<NNN nome cognome>\...\cartellino-MM-YYYY.pdf` (un PDF per mese, nomi cartella e sottocartelle non uniformi — alcuni usano nomi mese in italiano es. `DICEMBRE 2020.pdf` invece di `cartellino-12-2020.pdf`)

## Script
- `C:\Users\Gianmarco\Documents\VERONA\analisi_verona.py` — motore di parsing: regole su durata/orario turno (`MIN_DURATION = 380 min`, `EXIT_1445 = 885 min`), calcola solo `buoni` maturati (no erogati/delta/Euro)
- `C:\Users\Gianmarco\Documents\VERONA\analizza_verona20062026.py` — driver: unisce i 7 noti + le 96 cartelle USB, dedup, genera `riepilogo_buoni_pasto_verona.xlsx`

## Bug scoperti e risolti (sessione 2026-06-19/20)
1. **Duplicati byte-identici** (stesso file esportato 2 volte, es. `_2.pdf`): dedup MD5 raw in `find_worker_pdfs()`.
2. **Duplicati semantici** (stesso mese ristampato in giorni diversi → "Elaborato il" diverso → MD5 diverso, ma dati giorno-per-giorno identici): dedup per firma `(day, dow, turno, worked, qualifies, entry, exit, duration_hm, note)` per chiave `(worker, year, month)`.
3. **Falso positivo "CONFLITTO"**: un singolo PDF può generare 2 entry per lo stesso mese (pagina dati reali + pagina di spillover/continuazione indennità con `details=[]`, `buoni=0`). La firma vuota differisce sempre da quella con dati → veniva segnalato come conflitto vero anche se non lo è. Fix: le entry con `details` vuoto non vengono mai confrontate come conflitto, solo scartate (contributo 0 comunque).
4. **Conflitti veri** (due PDF diversi, stesso mese, dati effettivamente diversi — es. uno snapshot preso a metà giornata prima che le timbrature fossero complete): risolti automaticamente tenendo la versione con più `buoni` (più giorni con turno realmente registrato). Confermato manualmente per i 2 casi reali trovati (FULLONE FRANCESCA e MINI' FRANCESCA, marzo 2026) confrontando il campo "Elaborato il" nel PDF.

## Cartelle senza dati (da verificare con l'utente)
- `127 andolfo maria`, `139 buscemi massimo uls9`, `156 niselli daniele`, `83 Marconi Elisa` — nessun cartellino PDF valido trovato nella cartella USB.

## Risultato finale (confermato 2026-06-20)
- **Lavoratori totali: 99**
- **Totale buoni pasto maturati: 94981**
- Cartelle senza dati: 4 (`127 andolfo maria`, `139 buscemi massimo uls9`, `156 niselli daniele`, `83 Marconi Elisa`) — nessun cartellino PDF valido trovato, da verificare con l'utente
- Conflitti dati reali risolti: 2 — FULLONE FRANCESCA 2026/3 (tenuto 8 buoni ≥ 7) e MINI' FRANCESCA 2026/3 (tenuto 10 buoni ≥ 9), entrambi confermati via campo "Elaborato il" nel PDF
- Duplicati residui innocui: 2 (Antolini Michael 2024/3, Rossi Fabio 2020/5 — pattern spillover noto, contributo 0)
- Output: `riepilogo_buoni_pasto_verona.xlsx`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: Verona completato. Pipeline rifinito con dedup a doppio livello + fix falsi positivi conflitto (10 dei 12 "CONFLITTO DATI" erano falsi positivi da pagine di spillover). Run finale eseguito e confermato, Excel generato, fix committato e pushato.
- Prossimo step: Regione Lazio, metodologia "Sangiovanni" con indennità da `Copia di annistampa.xlsx`.
