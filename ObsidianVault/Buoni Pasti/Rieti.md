# Buoni Pasto Rieti

Elaborazione buoni pasto maturati per i lavoratori ASL Rieti, inclusa gestione turni notturni e regola di accoppiamento notti consecutive.

## Fonti dati
- Cartellini PDF per lavoratore
- Archivi raw aggiuntivi (PDF/7z per lavoratore, non script): `C:\Users\Gianmarco\Documents\ARCHIVIO RIETI\`, `ARCHIVIO RIETI PER GIANMARCO\`

## Script
- `C:\Users\Gianmarco\Documents\ELABORATI_RIETI\elabora_rieti.py` (28/03, versione precedente, logica turni semplificata, output da template)
- `C:\Users\Gianmarco\Documents\rieti\analisi_rieti.py` (20/05, **script attivo/definitivo**, più recente e completo: parsing turni notturni con marcatori split-row `-LF`/`-_J`, output "riepilogo + fogli anno" come Tivoli)

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
N/A — Rieti riguarda solo buoni pasto da cartellino.

## Output desiderato
Conteggio buoni maturati da cartellini (turni diurni + notturni con regola consecutivi) per vertenza contro ASL Rieti.

## Formato output
- File per lavoratore: `{LAVORATORE}.xlsx` — foglio "Riepilogo" (riga=Anno, colonne=12 mesi con buoni+€, colonna TOTALE buoni, colonna € da recuperare = Totale × 4.13) + un foglio per anno (righe giornaliere: Mese, Giorno, GG, Lavorato, Qualifica, Maturato, €; riga TOTALE MESE)
- File aggregato: `RIEPILOGO_BUONI_PASTO_RIETI.xlsx` (righe=lavoratori, colonne=anni, TOTALE/EUR)
- Log PDF non leggibili: `pdf_non_leggibili_rieti.log`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata.
