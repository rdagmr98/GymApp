# Centri Storici Italia — Hub

## Obiettivo
Creare un database completo di indirizzi in centro storico per tutti i comuni italiani, con parola chiave univoca per ogni via — da usare per identificare spedizioni con sovrattassa "centro storico".

## File Excel generati
| File | Righe | Note |
|------|-------|------|
| `centri_storici_v1_fixed.xlsx` | ~288k | Fix CAP + keyword su dati v1 |
| `centri_storici_v2/CENTRI_STORICI_ITALIA.xlsx` | TBD | Filtro poligoni OSM veri |

Percorso: `C:\Users\Gianmarco\Documents\`

## Struttura colonne Excel
| Colonna | Contenuto |
|---------|-----------|
| Regione | Es. Lazio |
| Provincia | Es. Roma |
| Sigla | Es. RM |
| CAP | Codice postale (da comuni-json ISTAT) |
| Comune | Es. Roma |
| Indirizzo | Via/Piazza/Corso completo |
| Parola Chiave | Parola distintiva per ricerca fuzzy |

## Script Python
- `fix_v1_quick.py` — Fix rapido sui dati v1
- `centri_storici_v2.py` — Raccolta da zero con poligoni OSM

Percorso: `C:\Users\Gianmarco\Documents\`

## Fonti dati
- **OSM Overpass API** — aree "centro storico" georeferenziate, strade dentro i poligoni
- **comuni-json** (matteocontrini) — CAP ufficiali per 7.898 comuni
- **ZIP v1** — `C:\Users\Gianmarco\Downloads\centri storici.zip` (dati grezzi precedenti)

## Problemi del v1
- ❌ CAP: 0% (100% mancante)
- ❌ Nessun filtro reale su centro storico — prendeva tutte le strade OSM del comune
- ❌ Includeva piste ciclabili, strade provinciali, svincoli, rotonde
- ❌ Parole chiave sbagliate ("sedime", "biforcazione", "acquafondata"...)

## Miglioramenti v2
- ✅ CAP da comuni-json ISTAT (99.9% copertura)
- ✅ Filtro su poligoni OSM tagged "centro storico"
- ✅ Esclusione strade non-indirizzo (regex esteso)
- ✅ Algoritmo keyword: rimuove prefissi, stop-words, numeri romani, santi, generici
- ✅ Deduplica per (comune, indirizzo)
- ✅ Ripresa automatica per regione

## Algoritmo parola chiave
1. Togli prefisso strada (via, viale, piazza, corso, vicolo...)
2. Togli stop words (di, del, della, in...)
3. Togli numeri romani e numeri
4. Dopo santi (San, Santa...) prendi il nome proprio che segue
5. Dall'elenco rimasto: prendi l'ultima parola non-generica con >2 lettere
6. Fallback: parola più lunga

**Esempi:**
- `Via Giuseppe Garibaldi` → `garibaldi`
- `Piazza Mons. Marcello Morgante` → `morgante`
- `Corso Vittorio Emanuele II` → `emanuele`
- `Via XX Settembre` → `settembre`
- `Viale Nicola D'Onofrio` → `d'onofrio`

## TODO
- [ ] Verificare copertura v2 vs v1 (quante strade in più/meno)
- [ ] Aggiungere gestione CAP multipli per grandi città (MI, RM, TO)
- [ ] Eventuale integrazione con liste ZTL ufficiali dei comuni
- [ ] Validare un campione di indirizzi su Google Maps

## Note tecniche
- Overpass API: 1-2 req/sec, timeout 120-180s per query
- Il v2 usa `punto_nel_poligono()` (ray-casting puro Python, no shapely)
- Ripresa da `centri_storici_v2/state.json`

---
*Aggiornato: 2026-06-13*
