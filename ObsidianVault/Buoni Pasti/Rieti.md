# Buoni Pasto Rieti

Elaborazione buoni pasto maturati per i lavoratori ASL Rieti, inclusa gestione turni notturni e regola di accoppiamento notti consecutive.

## Fonti dati
- Cartellini PDF per lavoratore
- Archivi raw aggiuntivi (PDF/7z per lavoratore, non script): `C:\Users\Gianmarco\Documents\ARCHIVIO RIETI\`, `ARCHIVIO RIETI PER GIANMARCO\`

## Script
Rieti ha **due pipeline distinte e complementari**, non due versioni della stessa cosa:
- `C:\Users\Gianmarco\Documents\rieti\analisi_rieti.py` (20/05) — **solo buoni pasto**: parsing turni notturni con marcatori split-row `-LF`/`-_J`, output "riepilogo + fogli anno" come Tivoli. Vedi criteri sotto.
- `C:\Users\Gianmarco\Documents\ELABORATI_RIETI\elabora_rieti.py` — **indennità da cedolino + giorni da cartellino**, metodologia [[San Giovanni]] applicata a Rieti (stesso template `sangiovanni\modello.xlsx`, stessa `MAPPATURA_IND` B-F). Input: `Documents\ARCHIVIO RIETI\{COGNOME NOME}\` (ricerca ricorsiva, apre anche PDF dentro ZIP/7z annidati). Output: `Documents\ELABORATI_RIETI\{COGNOME_NOME}.xlsx`. Usato per la richiesta "nuovo formato con formule corrette e specchio riassuntivo in alto a destra" (zip `ASL RIETI COMPLETARE.zip`, 2026-07-07).

## Criteri di assegnazione/maturazione buono pasto
- **Soglia minima**: `THRESHOLD = 380` minuti (6h20m)
- **Turni giornalieri semplici** (entrata/uscita stessa riga):
  - durata < 380 min → sotto soglia, nessun buono
  - durata > 480 min (8h) **e** inizio < 12:00 **e** fine tra 12:00-22:00 → esclusa come turno "lungo" anomalo (evita doppio conteggio pausa pranzo su turni diurni lunghi)
  - altrimenti → +1 buono
- **Turni notturni** (entrata/uscita su righe separate, marcatori `-LF` inizio notte / `-_J` continuazione da giorno precedente): durata = `(24h - entrata) + uscita`; se ≥ 380 min → +1 buono, altrimenti 0
- **Notti consecutive**: raggruppate in post-processing; in un gruppo di n notti consecutive contano solo le posizioni dispari (1ª, 3ª, 5ª...) — es. 2 notti consecutive → 1 sola conta (stessa logica "ogni 2 notti = 1 buono" di Verona)
- **Valore buono**: `BUONO_EURO = 4.13`

## Criteri di ricerca indennità da cedolino
Via `elabora_rieti.py` — stessa metodologia di [[San Giovanni]] (5 categorie, colonne B-F, stessi codici cedolino NoiPA — vedi tabella nella nota San Giovanni). Giorni lavorati/ferie letti dal cartellino con la stessa logica San Giovanni/Roma3.

## Output desiderato
Conteggio buoni maturati da cartellini (turni diurni + notturni con regola consecutivi) per vertenza contro ASL Rieti.

## Formato output
- File per lavoratore: `{LAVORATORE}.xlsx` — foglio "Riepilogo" (riga=Anno, colonne=12 mesi con buoni+€, colonna TOTALE buoni, colonna € da recuperare = Totale × 4.13) + un foglio per anno (righe giornaliere: Mese, Giorno, GG, Lavorato, Qualifica, Maturato, €; riga TOTALE MESE)
- File aggregato: `RIEPILOGO_BUONI_PASTO_RIETI.xlsx` (righe=lavoratori, colonne=anni, TOTALE/EUR)
- Log PDF non leggibili: `pdf_non_leggibili_rieti.log`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-07-07 (2/2): **rielaborazione dei 9 lavoratori completata e verificata**. Tutti OK (conteggi ced/cart coerenti, log `LOG_ELABORAZIONE_RIETI.txt`). File `.xlsx` usano formule Excel non calcolate (celle "Somme annuali"/"Medie annue" vuote finché non aperte in Excel) — totali verificati sommando manualmente le colonne indennità (B-F) per riga mensile via openpyxl. Risultato: CASSANELLI STEFANIA 0→18.834,59 EUR, PETRACCHIOLA VALENTINA 0→23.142,02 EUR; LA MESA DEBORA totale invariato (90.120,25 EUR) nonostante conteggio cartellini cambiato (69→68) — coerente col fatto che il suo caso specifico di bug toccava solo cartellini (colonne giorni lavorati/ferie, non EUR), non cedolini (fonte delle indennità). **Nuovo totale generale: 1.461.530,41 EUR su 62 lavoratori** (prima 1.336.739,94 EUR, +124.790,47 EUR). Nuova top 3: DE SANTIS KATIUSCIA (94.165,04), LA MESA DEBORA (90.120,25), DEL VESCOVO ALESSANDRO (60.513,87). GENNARO GIUSEPPE confermato ancora a 0,00 EUR (caso a parte, vedi sotto). Commit `4256885`, push su main.
- 2026-07-07 (1/2): **bug di parsing trovato e corretto in `elabora_rieti.py`** (indennità). Causa: `_processa_zip()` apriva solo `.pdf` dentro uno zip e saltava silenziosamente (nessun avviso) le entry `.zip`/`.7z` annidate — asimmetrico rispetto a `_processa_7z()` che già gestiva correttamente la ricorsione. Cartelle come `stefania cassanelli.zip` (contiene `cedolini (8..13).zip`) e `Cedolini Petracchiola.zip` (contiene `cedolini 2020..2025.zip`) hanno esattamente questa forma zip-dentro-zip: tutto il contenuto reale veniva scartato senza errore, con indennità totale 0,00 EUR. Scansione completa dei 62 lavoratori: **9 su 62 (14,5%) colpiti** — CAMAGNA ANTONIETTA, CASSANELLI STEFANIA, DEL VESCOVO ALESSANDRO, LA MESA DEBORA, LELLI PATRIZIA, LUCIANI MADDALENA, MANCINI ROBERTA, MARTINES VINCENZO, PETRACCHIOLA VALENTINA. Fix: `_processa_zip()` reso ricorsivo (parametro `depth`, cap a 3 come `_processa_7z`), gestisce entry `.zip` (ricorsione diretta via `io.BytesIO`) e `.7z` (via file temporaneo + `_processa_7z`). Caso a parte: **GENNARO GIUSEPPE** resta a 0,00 EUR per fonte dati realmente corrotta (4 stub JSON di errore API salvati con estensione `.zip`, non un bug di parsing) — richiede ri-reperimento cedolini dall'utente, non risolvibile via codice.
- 2026-06-20: documentazione criteri/formato consolidata.
