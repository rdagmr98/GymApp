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
| Comuni | 85 (84 OSM + Milano) |
| Strade ZTL | 7.022 |
| Righe keyword | 7.969 |
| Max keyword/strada | 5 |
| Distribuzione kw | {1: 6264, 2: 608, 3: 113, 4: 35, 5: 2} |

**Fonte strade — query OSM NAZIONALE (`ztl_full.py`, NON più i file v2).** Interroga tutte le
**225 zone** italiane con tag `boundary=limited_traffic_zone` (128 way + 97 relation) — il tag ZTL
italiano corretto (`restricted_traffic_zone` dà 0 risultati in Italia). Per ogni zona:
1. **Comune** = reverse-geocoding Nominatim del centroide (zoom 14) → normalizzato vs
   `cap_cache.json` (più affidabile del `comune_da_tags` v2 difettoso). Mappa `COMUNE_ALIAS` per
   varianti nome ("Reggio Emilia"→`reggio nell'emilia`, "Montecatini Terme"→`montecatini-terme`) e
   frazioni→comune padre (Polpet→Ponte nelle Alpi, Monti di Licciana→Licciana Nardi, Gorfigliano→Minucciano).
2. **Strade nella zona** = strategia ibrida robusta su tutti i tipi OSM:
   - `map_to_area` → `way[highway][name](area)` per i poligoni (way chiuse + relation `type=boundary`);
   - se vuoto, fallback **membri-strada** `<type>(<id>);>;out geom;` filtrando way con `highway`+`name`
     (copre `type=enforcement` e `type=site`, i cui membri SONO già le strade della ZTL).

Le keyword si ricalcolano con `processa_comune` (test unicità vs strade FUORI ZTL nello stesso
comune) + normalizzazione finale identica al centro storico (apostrofo tenuto, doppia variante
trattino/slash, alias numerici).

**Milano integrato dal file produzione.** OSM ha solo ~26 strade ZTL per Milano (incompleto),
quindi si usano le **683 keyword** del file `Downloads/ztl milano.xlsx` (685 righe, dedotte con
`clean_kw`); Milano è escluso dalla pipeline OSM. (Area C/B = `low_emission_zone`, tag diverso, escluse.)

**Copertura:** 225 zone → 0 senza comune, ~11 zone vuote scartate (geometrie senza strade nominate),
84 comuni OSM + Milano. Include ora **Roma** (718 strade), Cagliari/Sassari/Alghero/Olbia,
Bolzano/Merano/Bressanone/Trento, Udine, Lecce, tutto il Garda. Il vecchio `ztl_v6.py`
(58 comuni dai file v2) è **superato**.

**Script:** `ztl_full.py`. Resume-safe via cache: `ztl_list.json` (225 zone),
`ztl_reverse_cache.json` (centroide→comune), `ztl_zone_streets.json` (zona→strade),
`geo_cache_ztl.json`, `ztl_full_master.csv(.bak)`.
`python ztl_full.py` (ricalcola se manca `.bak`) · `--no-skip` forza · `--solo-righe` solo rebuild xlsx.

## TODO
- [x] Completare v5 (tutti i comuni — 310.423 righe, 7126 comuni)
- [ ] Completare run v6 keyword multiple (background, ~8h) → v6_larga + v6_righe
- [ ] Validare campione keyword v6 (no falsi positivi su vie fuori centro)
- [ ] Gestire CAP multipli per grandi città (MI, RM, TO hanno CAP per quartiere)
- [x] Dataset ZTL formato righe (`ZTL_ITALIA_righe.xlsx`, 85 comuni, 7969 righe — query OSM nazionale)
- [x] Integrare Milano ZTL (683 keyword dal file produzione)

---
*Aggiornato: 2026-06-17 — ZTL esteso a tutti i comuni italiani (query OSM nazionale) + Milano*
