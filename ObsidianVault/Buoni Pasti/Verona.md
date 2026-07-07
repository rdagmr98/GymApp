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

## Integrazione incrementale 2026-07-07 (`verona gianmarco.zip`)
Script separato: `C:\Users\Gianmarco\Documents\VERONA\integra_verona_gianmarco.py` — NON tocca il motore `analisi_verona.py` (la chiavetta USB `E:\verona` con i dati grezzi dei 99 lavoratori esistenti era scollegata, quindi rigenerazione completa non possibile). Integrazione incrementale: legge i totali anno-per-anno già presenti nel foglio `Riepilogo`, aggiunge i nuovi lavoratori, riscrive SOLO `Riepilogo` (i 99 fogli di dettaglio esistenti restano intatti).

**Risultato**: 10 lavoratori integrati su 11 nel pacchetto (1 escluso, vedi sotto). Totale ora **109 lavoratori, 105.688 buoni pasto** (da 94.981 su 99 lavoratori). Backup pre-modifica: `riepilogo_buoni_pasto_verona_BACKUP_pre_gianmarco.xlsx`.

Nuovi lavoratori integrati (totale buoni tra parentesi): BIFFARA ALESSANDRA (578), CIULLO ELISA (1999), FANTUCCHIO FABRIZIO (450), FILARDI LUCA (1841), FORAFO' SILVIA (637), KHADDADI YOSSRA (430), MACCHIELLA CARMEN (782), PASQUALI ALICE (781), RUFFO SIMONETTA (1063), SALERNO STEFANIA (2146).

Due discrepanze di grafia nella cartella zip risolte usando il nome estratto dal testo del PDF (fonte autoritativa, stesso criterio di `process_page()`): cartella "Bifarra" → nome vero **BIFFARA ALESSANDRA** (typo nel nome cartella); cartella "macchiella" → **MACCHIELLA CARMEN** (corrisponde già alla cartella, nessuna discrepanza reale).

**Escluso — CARDONE FABIOLA (formato dati incompatibile)**: 74 PDF trovati, tutti restituiscono 0 mesi elaborati. Causa diagnosticata (via ispezione diretta `pdfplumber`, non un bug): i suoi cartellini sono un formato completamente diverso da tutti gli altri lavoratori Verona — export web "GPI - Elenco timbrature" dal portale self-service "Angolo del dipendente", non il cartellino standard che `process_page()` sa leggere. Header diverso (niente pattern "RILEVAZIONE...Cognome...Nome"), struttura tabella diversa (codici turno tipo `B00 / RRR`, `B00 / T74`), orari inline ("E 06:50 U 14:16") invece che a colonne. Non risolvibile con una piccola patch al parser esistente — servirebbe un ramo di parsing dedicato per questo formato, non giustificato per 1 lavoratore su 110 senza richiesta esplicita. Struttura cartelle sua: `Cardone Fabiola/Cartellini CARDONE FABIOLA/{YYYY}/{M.YYYY}.pdf` (un livello più annidato degli altri, ma non è la causa del fallimento — `find_worker_pdfs` è ricorsivo e trova tutti i 74 file).

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-07-07: integrati 10 nuovi lavoratori da `verona gianmarco.zip` (109 tot, 105.688 buoni). 1 escluso (CARDONE FABIOLA, formato cartellino incompatibile "GPI - Elenco timbrature", da segnalare all'utente per ri-reperimento dati in formato standard). Dettagli sopra.
- 2026-06-20: Verona completato. Pipeline rifinito con dedup a doppio livello + fix falsi positivi conflitto (10 dei 12 "CONFLITTO DATI" erano falsi positivi da pagine di spillover). Run finale eseguito e confermato, Excel generato, fix committato e pushato.
