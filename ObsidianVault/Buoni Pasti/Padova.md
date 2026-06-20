# Buoni Pasto Padova (vertenza UIL FPL)

Conteggio buoni pasto maturati secondo logica di vertenza (notturni consecutivi + festivi), non da semplice soglia oraria giornaliera come Tivoli/Cittadella/Rieti.

## Fonti dati
- Cartellini in `C:\Users\Gianmarco\Downloads\padova2\` (`PERCORSO_RADICE`) — **non su unità E:** nonostante una nota precedente facesse riferimento a `E:\UIL FPL PADOVA\...`: il path reale nello script attivo è su C:, da verificare con l'utente se quel riferimento E: riguarda solo l'archivio sorgente originale (chiavetta) o è obsoleto

## Script
- 4 varianti in `C:\Users\Gianmarco\Python\`: `padovaprova.py` (16/02, bozza), `padova.py` (06/03), `padova1.py` (10/03), `padova2.py` (17/03, più recente)
- **Script attivo**: `padova2.py`

## Criteri di assegnazione/maturazione buono pasto
- **Non è una soglia fissa di minuti** come le altre sedi — regole specifiche per la vertenza:
  - **Smontante primo giorno** (prima riga del periodo con 1 sola timbratura): +0.5 buoni
  - **Turni notturni consecutivi**: giorno con 1 sola timbratura (uscita notturna) si abbina al giorno successivo con 2 timbrature (chiusura notte + inizio notte seguente) → la coppia conta insieme, non doppia
  - **Festivi/domeniche**: +1.0 buono se durata turno ≥ 385 minuti (6h25m). Festivi fissi: `1/1, 6/1, 25/4, 1/5, 2/6, 13/6, 15/8, 1/11, 8/12, 25/12, 26/12` + Pasquetta calcolata dinamicamente (algoritmo di Pasqua +1 giorno) + ogni domenica
  - Giorni normali (non festivi, non notturni accoppiati): nessun buono
- **Buoni erogati**: non trattati — questa è vertenza sul calcolo dei maturati, non un confronto maturato/erogato

## Criteri di ricerca indennità da cedolino
N/A — Padova riguarda solo buoni pasto.

## Output desiderato
Conteggio buoni maturati secondo le regole di vertenza UIL FPL (notturni + festivi), con dettaglio testuale del motivo di ogni buono assegnato, per reclamo retributivo.

## Formato output
- File: `RIEPILOGO_VERTENZA_BUONIu2.xlsx`, 2 fogli:
  - **RIEPILOGO_ANNUALE**: pivot — righe=Lavoratore, colonne=Anno, valori=somma Buoni
  - **DETTAGLIO_MENSILE**: righe=record mensili, colonne=Lavoratore, Anno, Mese, Buoni, Dettaglio (testo descrittivo per ogni buono, es. "G15:+1.0 Festivo (durata 410 min)")
- Cartella debug per-lavoratore/periodo: `DEBUG_OPERAZIONIu2`

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: documentazione criteri/formato consolidata. Path E: in note precedenti da verificare/correggere — lo script attivo legge da C:\Users\Gianmarco\Downloads\padova2.
