# Pipeline Buoni Pasti — Hub Principale
Hub per il sistema di calcolo buoni pasto e cartellini lavoratori. Leggi questo file all'inizio di ogni sessione buoni pasto.

![[Grafi/Buoni Pasti Pipeline]]

---

## Script principali

| Script | Scopo |
|--------|-------|
| `analizza_tivoli12062026.py` | Versione corrente per elaborazione tivoli 12/06/2026 |
| `analisi_tivoli.py` | Script base storico |

**Path**: `C:\Users\Gianmarco\`

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
- [[Verona]] — ASL Verona, 99 lavoratori, criteri durata/orario turno diversi da Tivoli
- [[Lazio]] — Regione Lazio, Coletti Ambra, metodologia "Sangiovanni", indennità da codici reali cedolini NoiPA (pattern concettuale da `annistampa.xlsx`)

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
- Ultima elaborazione: Regione Lazio (Coletti Ambra) — vedi [[Lazio]]
- Sequenza completata: Tivoli (4 nuovi lavoratori) → Verona (99 lavoratori) → Lazio (Coletti Ambra)
- Script attivo: `analizza_tivoli12062026.py` (Tivoli) — altri script per progetto in [[Verona]] e [[Lazio]]
