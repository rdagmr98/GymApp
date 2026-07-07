# Pipeline Buoni Pasti — Hub Principale
Hub per il sistema di calcolo buoni pasto e cartellini lavoratori. Leggi questo file all'inizio di ogni sessione buoni pasto.

![[Grafi/Buoni Pasti Pipeline]]

---

## Script principali (Tivoli)

| Script | Scopo |
|--------|-------|
| `analizza_tivoli02072026.py` | Driver corrente (2 nuovi lavoratori, carry-forward semplificato) |
| `analizza_tivoli01072026.py` | Versione precedente (unifica due archivi + supporto 7z) |
| `analizza_tivoli23062026.py` | Versione precedente (secondo archivio, 31 lavoratori) |
| `analisi_tivoli.py` | Motore di parsing base |

**Path**: `C:\Users\Gianmarco\Documents\tivoli\` (corretto 2026-06-20 — non in root come riportato prima)

→ Dettagli completi: [[Tivoli]]

---

## Flusso pipeline

```
ZIP Input → estrai cartellini individuali
Storico XLSX (9 Workers) → dati di riferimento
                ↓
detect_format() → parse_new_format() | parse_old_rev()
                ↓
Calcolo buoni pasto per worker
                ↓
Excel Worker (per lavoratore) + Cartellini PDF + RIEPILOGO XLSX
                ↓
ZIP Definitivo → consegna
```

---

## 9 Workers
→ [[9 Workers]] — lista lavoratori con dati di riferimento

---

## Altri progetti buoni pasto

**Solo buoni pasto** (soglia minuti su cartellino, no indennità):
- [[Verona]] — ASL Verona, 99 lavoratori, soglia 385 min, criteri durata/orario turno diversi da Tivoli
- [[Cittadella]] — Ospedale Cittadella, soglia 375 min (identica a Tivoli)
- [[Rieti]] — ASL Rieti, soglia 380 min, notti consecutive (ogni 2 = 1 buono)
- [[Padova]] — vertenza UIL FPL, NON soglia fissa: regole notturni consecutivi + festivi/domeniche (≥385 min)

**Solo indennità da cedolino** (metodologia "Sangiovanni", no buoni pasto):
- [[San Giovanni]] — origine della metodologia, 5 categorie indennità (B-F), template `modello.xlsx` riusato dagli altri
- [[Roma3]] — ASL Roma 3 Ostia, stesse 5 categorie e template di San Giovanni
- [[Lazio]] — Regione Lazio, Coletti Ambra, stessa metodologia ma **7 categorie** (B-H, 2 in più di San Giovanni/Roma3), indennità da codici reali cedolini NoiPA (pattern concettuale da `annistampa.xlsx`)
- [[Rieti]] (`elabora_rieti.py`) — stesse 5 categorie e template di San Giovanni, **oltre** alla pipeline separata di soli buoni pasto già elencata sopra (Rieti è l'unica sede con entrambe le pipeline)

**Da chiarire**:
- **"Enti Locali"** — menzionata dall'utente insieme alle altre sedi, ma nessuna cartella/script con questo nome esiste (verificato su Documents, Python, Desktop, root). Ipotesi non confermata: potrebbe essere la categoria CCNL "Enti Locali" (vs Sanità/Regione) — coerente col fatto che Coletti Ambra (Lazio) ha "Categoria C1 Enti Locali" nel cedolino — non una sede separata. Da chiedere all'utente.

---

## Formati supportati
- **Nuovo formato**: `parse_new_format()` — struttura post-2025
- **Vecchio formato**: `parse_old_rev()` — struttura legacy

---

## Output generati
- Excel per singolo lavoratore (1 file × worker)
- Cartellini PDF con riepilogo ore/presenze
- RIEPILOGO.xlsx — foglio aggregato tutti i lavoratori
- ZIP finale con tutti i file

---

## Dipendenze Python
```
pandas, openpyxl, fpdf2 / reportlab, zipfile
```

---

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-23: Tivoli — integrati 9 nuovi lavoratori (Rosati, Salvati Simona, Scalabrino, Tanoni, Bugara, Gennari, Lombardi, Panunzi, Marraccini — quest'ultima del tutto nuova all'archivio). Totale ora 31 lavoratori, 122.966,62 EUR da recuperare. Dettagli in [[Tivoli]].
- 2026-06-20: documentate tutte le sedi lavorate finora — criteri di assegnazione/maturazione buoni pasto, criteri di ricerca indennità, output desiderato e formato output per ciascuna: [[Tivoli]], [[Cittadella]], [[Rieti]], [[Padova]] (solo buoni pasto) + [[San Giovanni]], [[Roma3]], [[Lazio]] (solo indennità). "Enti Locali" resta non identificata come sede — ipotesi: categoria CCNL, non sede separata.
- 2026-06-20: risolta ambiguità script San Giovanni — confermato `sangiovanniprogrammaversionegianmarco.py` come script attivo tramite prova sui file di output reali (cartella ELABORATI con decine di lavoratori), non solo timestamp. Dettagli in [[San Giovanni]].
- 2026-07-01: unificazione due archivi Tivoli (191+31 → 213 lavoratori, 870.380,98 EUR). Silvestri Paola, Papa Antonella aggiornate; Iachini Sandra nuova.
- 2026-07-02: Tivoli — 2 nuovi lavoratori (TILIA EMANUELA, ABBATI MARIA), risolta ambiguità identità TILIA vs ATTILIA EMANUELA via verifica matricola/CF sui documenti sorgente. Totale ora 215 lavoratori, 883.423,52 EUR.
- Sequenza completata: Tivoli (4 nuovi, 20/06) → Verona (99) → Lazio (Coletti Ambra) → Tivoli (9 nuovi, 23/06) → Tivoli (unificazione+3, 01/07) → Tivoli (2 nuovi, 02/07)
- Script attivo Tivoli: `analizza_tivoli02072026.py`
