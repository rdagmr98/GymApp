# Centri Storici Italia — Hub

## Obiettivo
Database completo di indirizzi in centro storico per tutti i comuni italiani, con parola chiave ASCII per ogni via — per identificare spedizioni con sovrattassa "centro storico".

## Stato corrente
| File | Righe | Comuni | Note |
|------|-------|--------|------|
| `CENTRI_STORICI_ITALIA_v4.xlsx` | 24.904 | ~107 | Solo capoluoghi |
| `CENTRI_STORICI_ITALIA_v5.xlsx` | 310.423 | 7126 | Tutti i comuni — strade centro, keyword vecchia singola |
| `CENTRI_STORICI_ITALIA_v6_larga.xlsx` | in costruzione | 7126 | **NUOVO** keyword multiple, 1 riga/strada (col. Parola Chiave 1/2/3) |
| `CENTRI_STORICI_ITALIA_v6_righe.xlsx` | in costruzione | 7126 | **NUOVO** keyword multiple, 1 riga per keyword (indirizzo ripetuto) |

Percorso: `C:\Users\Gianmarco\Documents\` · Run v6 in background (~6-7h, resume-safe via `state_v6.json`/`progress_v6.json`)

## Struttura colonne Excel
| Colonna | Contenuto |
|---------|-----------|
| Regione | Es. Lazio |
| Provincia | Es. Roma |
| Sigla | Es. RM |
| CAP | Codice postale (da comuni-json) |
| Comune | Es. Roma |
| Indirizzo | Via/Piazza/Corso completo |
| Parola Chiave | Parola distintiva ASCII (no accenti) per ricerca fuzzy |

## Script Python (in `C:\Users\Gianmarco\Documents\`)
| Script | Funzione |
|--------|----------|
| `centri_storici_v3.py` | Merge + fix + espansione 107 province → v4.xlsx |
| `centri_storici_all_comuni.py` | Tutti i 7904 comuni → v5.xlsx (con resume) |
| `keywords_v6.py` | **Ricalcolo keyword v6** con test unicità vs vie fuori centro → v6_larga + v6_righe |
| `valuta_copertura.py` | Analisi copertura per provincia |
| `check_accenti.py` | Verifica keyword ASCII (0 accenti) |
| `centri_storici_METODO.txt` | Documentazione completa metodologia |

## Come vengono trovate le strade

### Metodo 1 — ZTL (dati storici da v2)
- Overpass: `relation["boundary"="restricted_traffic_zone"]` per comune
- Se ZTL trovata: strade dentro il poligono = centro storico certo
- Dati in: `centri_storici_v2/*.xlsx`

### Metodo 2 — Radius fallback
- Centro del comune: coordinate hardcoded (capoluoghi) o Nominatim geocoding
- Overpass: `way["name"]["highway"](around:R, lat, lon)` con R = 500-1000m
- R dipende dalla popolazione: <10k→500m, 10-50k→700m, >50k→1000m
- Filtro regex: esclude autostrade, SP/SS numerate, piste ciclabili, ecc.

### Endpoint Overpass
`https://maps.mail.ru/osm/tools/overpass/api/interpreter`

## Algoritmo Parola Chiave v6 (`keywords_v6.py`)

Il matching è per **SOTTOSTRINGA** della keyword dentro l'indirizzo scritto dal cliente.
Quindi: keyword può avere spazi ("santa maria", "degli angeli") e una strada può avere **più keyword** (per beccarla anche se il cliente sbaglia a scrivere).

**VINCOLO CHIAVE:** la keyword NON deve essere contenuta in nessuna via FUORI dal centro storico ma nello **stesso comune** (non stesso CAP).
Es. Cuneo "Via Canonico Rossi" è fuori centro → "rossi" beccherebbe anche quella → si usa "AMEDEO ROSSI".
Es. "sette" beccherebbe "settembre" → troppo corta/comune, vietata.

**Passi `keywords(nome, rest_norm)`** → lista keyword (principale prima):
1. Split su `/` e ` - ` in segmenti (alias/incroci: "Via Segantini - Via Gola" → SEGANTINI + VIA GOLA)
2. Per segmento: togli prefisso, pulisci punteggiatura, gestisci apostrofo ("Sant'Anna" → SANT'ANNA senza spazio)
3. Principale: cresce da **destra** (ultima parola), allarga a 2-3 parole solo se la corta non è unica vs `rest`
4. Anchor extra: altri token distintivi (cognomi) che passano il test di unicità → keyword aggiuntive (max 3)
5. Blocco singola: STOP, SAINTS, COMMON (nomi freq.), NUM, ORD, GENERIC(+area/zona), **TITLES** (don/monsignor/senatore/conte/cavaliere...), numeri romani, len<4
6. `rest_norm` = tutte le vie del comune (Overpass area da Nominatim osm_id) MENO le vie del centro (indirizzi v5)

**Esempi v6:** AMEDEO ROSSI · SANTA MARIA · VENTI SETTEMBRE · QUATTRO MARTIRI · SANT'ANNA · BORGO NUOVO · DEGLI ANGELI · CAVOUR|BENSO · STAZIONE VECCHIA

### Normalizzazione finale keyword (`pulisci_keyword_v6.py`)
Post-processa il backup `.bak` e rigenera i 2 xlsx senza rifare il run.
- Accenti rimossi (ASCII puro).
- **Apostrofo tenuto** attaccato (SANT'ANNA, DELL'ORTO) — serve al matching sottostringa.
- **Trattino/slash tra due parole** → doppia keyword: col simbolo (PONTE-CETTI) + con spazio (PONTE CETTI). 700 strade interessate.
- Altra punteggiatura → spazio. `max keyword` per strada ora 5.

## Due formati di output v6
- `CENTRI_STORICI_ITALIA_v6_larga.xlsx` — 1 riga per strada, colonne "Parola Chiave 1 / 2 / 3..." (WIDE)
- `CENTRI_STORICI_ITALIA_v6_righe.xlsx` — colonne fisse, 1 riga per ogni keyword, indirizzo ripetuto (LONG)

Backup resume-safe: `keywords_v6_master.csv` + `state_v6.json` + `geo_cache_v6.json` + `progress_v6.json` (flush ogni 25 comuni).

## Dati di supporto
- **comuni-json** (matteocontrini/GitHub): 7904 comuni — nome, sigla, cap, popolazione, regione, provincia. NON ha lat/lon.
- **cap_cache.json** (`centri_storici_v2/`): 7898 comuni con cap/sigla/regione/provincia. Sigla presa da `c["sigla"]` (radice, non `c["provincia"]["sigla"]`).

## Dataset ZTL (zone a traffico limitato) — formato RIGHE

Stessa metodologia keyword v6 ma applicata alle **strade in ZTL** invece del centro storico.
Output: `ZTL_ITALIA_righe.xlsx` — 7 colonne fisse, 1 riga per keyword (LONG).

| Voce | Valore |
|------|--------|
| Comuni | 58 |
| Strade ZTL | 6.095 |
| Righe keyword | 7.009 |
| Max keyword/strada | 5 |
| Distribuzione kw | {1: 5390, 2: 553, 3: 102, 4: 43, 5: 7} |

**Fonte strade:** riuso dei file `centri_storici_v2/*.xlsx` non-fallback (strade ricavate dai
poligoni OSM `boundary=limited_traffic_zone` — il tag ZTL italiano corretto, **non**
`restricted_traffic_zone` che dà 0 risultati). Le keyword vecchie sono ignorate: si ricalcola
con `processa_comune` (test unicità vs strade FUORI ZTL nello stesso comune) + normalizzazione
finale identica al centro storico (apostrofo tenuto, doppia variante trattino/slash, alias numerici).

**Script:** `ztl_v6.py`. Resume-safe via `ztl_v6_master.csv(.bak)` + `geo_cache_ztl.json`.
`python ztl_v6.py` (ricalcolo se manca `.bak`) · `--no-skip` forza · `--solo-righe` solo rebuild xlsx.

**Pulizia dati v2** (il geocoding inverso `comune_da_tags` del v2 era difettoso):
- `FILE_FIX`: `bergamo.xlsx` aveva tutte le righe etichettate comune="Viale" (estratto da
  "Viale Libertà"; "Viale" è un comune reale in AT → passava il check) → forzate a **Bergamo**.
- Scarto cross-provincia: in ogni file si tiene solo la sigla **modale**; intrusi scartati
  (Milano/Gozzano in la_spezia, Tarsia in napoli, Firenze in verona) = 65 righe.
- `SPLIT` province ambigue risolte assegnando ogni strada al comune candidato che la contiene
  (match Overpass): Barletta-Andria-Trani → Barletta 56 / Andria 1 / Trani 0; Massa-Carrara →
  Carrara 1 / Massa 0; "Monza e della Brianza" → Monza (7 assegnate, 32 duplicati scartati).

**ATTENZIONE Milano:** in OSM la ZTL di Milano (`limited_traffic_zone`) ha solo ~26 strade,
mentre il file di esempio produzione (`Downloads/ztl milano.xlsx`) ne ha 685. OSM è incompleto
per Milano. Da integrare a mano se serve copertura completa Milano (Area C/B sono `low_emission_zone`,
tag diverso, non incluse).

## TODO
- [x] Completare v5 (tutti i comuni — 310.423 righe, 7126 comuni)
- [ ] Completare run v6 keyword multiple (background, ~8h) → v6_larga + v6_righe
- [ ] Validare campione keyword v6 (no falsi positivi su vie fuori centro)
- [ ] Gestire CAP multipli per grandi città (MI, RM, TO hanno CAP per quartiere)
- [x] Dataset ZTL formato righe (`ZTL_ITALIA_righe.xlsx`, 58 comuni, 7009 righe)
- [ ] Integrare Milano ZTL (OSM ha 26 strade vs 685 reali)

---
*Aggiornato: 2026-06-17*
