---
tags: [siel, aves, access, motori, scadenze, bugfix, deep-dive]
aliases: [Motori SIEL, Bug motori situazione, cerca_motori, Scadenze situazione]
---
# SIEL — Logica Motori e Scadenze (report Situazione)

> Nodo tecnico di dettaglio del progetto [[SIEL]]. Spiega **come l'Access identifica i motori e calcola le scadenze** nel report *Situazione Velivoli*, perché il portable sbagliava ("mette il – sul motore" / "ore su motori inesistenti"), e il fix applicato. Ambito: [[AVES Corsi/AVES Hub|AVES]].

## TL;DR (la causa del bug)
Il report *Situazione* ha due sotto-report che davano problemi nel portable:
1. **Motori** — il portable usava il filtro sbagliato (`reale` = part_num/ser_num non nulli). Conseguenze: nascondeva **motori veri senza seriale** (→ "– sul motore" su elicotteri efficienti) e mostrava parti **senza codice** (es. il T53 a bordo del 347). In più riempiva le colonne motore mancanti con un **"–"** cosmetico.
2. **Scadenze** — semplicemente **non c'erano**. Il sotto-report scadenze, che è lo scopo stesso del report (gestire le scadenze LIC/LOF), era assente dal portable.

**Fix:** identificare i motori **come l'Access** (presenza del *codice* parte, non del seriale), padding colonna vuoto invece di "–", e **aggiunta della sezione SCADENZE** con le formule esatte dell'Access. La matematica di registrazione volo era **già corretta** (verifica round-trip insert→modifica→cancella = ritorno esatto).

---

## Modello dati rilevante
- **`parti`** — una riga per particolare montato su una sigla. PK `contatore`. Campi chiave: `sigla, id, tipo_vlv, part_num, ser_num, ore_vlv_imb, ore_particolare, ultimo_lic, scad_lic, ultimo_lof, scad_lof, applicabilita, cicli_tot`.
- **`codice`** — anagrafica nomi parte per coppia **(`id`, `tipo_vlv`)** → colonna `Parte` (es. "TURBOMOTORE"). È la tabella che dà il **nome** a un particolare.
- **`Elicotteri`** — `sigla, Ore_totali, Ore_iniziali, Ore_DUR, id_tipo…`. `tab_eli_query.Ore_complessive = somma_ore(Ore_totali, Ore_iniziali)`.
- **`id` del particolare** = posizione logica: **1 = Motore 1**, **2 = Motore 2**. Gli `id` ≥3 sono altri particolari (non motori).

### Mappa motore per `tipo_vlv` (tabella `codice`, id 1/2)
Il **nome** del motore dipende da `tipo_vlv`. Dove l'id 2 è `None`, il tipo è **monomotore**:

| tipo_vlv | id=1 (Motore 1) | id=2 (Motore 2) | Note |
|---|---|---|---|
| 1 | TURBOMOTORE | *(None)* | monomotore |
| 2 | SEZIONE POTENZA 1 | SEZIONE POTENZA 2 | bimotore (sezioni) |
| **3** | **TURBOMOTORE** | ***(None)*** | **monomotore → AB206C1** |
| 4 | *(nessun codice)* | *(nessun codice)* | **AB205 → motori sempre vuoti** |
| 5 | SEZIONE POTENZA 1 | SEZIONE POTENZA 2 | |
| **6** | **TURBO MOTORE** | *(solo id1)* | **T53L13** (sezione singola) |
| 7 / 8 / 14 | MOTORE 1 | MOTORE 2 | bimotore (A109T = tv7) |
| 9 | T/MOTORE 1 | T/MOTORE 2 | |
| 12 | T.MOTORE ALLISON | ELICA | |
| 16 | SEZIONE POTENZA 1 | SEZIONE POTENZA 2 | |

Tipi nel parco: `tv3 → AB206C1`, `tv4 → AB205`, `tv6 → T53L13`, `tv7 → A109T`.

> ⚠️ **Parco attivo (giugno 2026) = nessun bimotore.** Solo AB206C1 (×24, monomotore), AB205 (×3, senza codice motore), T53L13 (×3, sezione singola). Quindi **la colonna "Motore 2" è vuota su TUTTI gli elicotteri attivi**: è corretto, non è un bug. L'A109T (tv7, bimotore con MOTORE 1+2) non è nel parco attivo.

---

## Ground truth — query Access (lette via DAO COM sola lettura da `Desktop\SIEL.accdb`)

### `cerca_motori` (identificazione motori)
```sql
SELECT parti.part_num, parti.ser_num, parti.sigla, codice.Parte,
       parti.ore_vlv_imb, parti.ore_particolare, parti.ore_dur_appl, parti.ore_dur,
       tab_eli_query.Ore_complessive, parti.id,
       somma_ore(sottrai_ore([ore_complessive],[ore_vlv_imb]),[ore_particolare]) AS ore_mot
FROM (parti INNER JOIN codice
        ON (parti.id = codice.id) AND (parti.tipo_vlv = codice.tipo_vlv))
     INNER JOIN tab_eli_query ON parti.sigla = tab_eli_query.sigla
WHERE (((parti.id)=1 Or (parti.id)=2))
ORDER BY parti.id;
```
Il sotto-report del report *situazione* ci si lega così (record source auto-generato):
```sql
-- ~sq_dsituazione~sq_dsottoreport motori
PARAMETERS __sigla Value;
SELECT DISTINCTROW * FROM cerca_motori AS situazione WHERE ([__sigla] = sigla);
```
**Chiavi di lettura:**
- Filtro = `id=1 OR id=2`. **Niente** filtro su `part_num`/`ser_num`.
- L'**INNER JOIN su `codice`** è ciò che decide se un motore "esiste": serve una riga `codice (id, tipo_vlv)`.
- `ore_mot = somma_ore(sottrai_ore(Ore_complessive, ore_vlv_imb), ore_particolare)` — **ore attuali del motore derivate**, non memorizzate.

### `ore_disp` / scadenze — `scadenze per report situazione giorn`
Il sotto-report scadenze si lega a:
```sql
-- ~sq_dsituazione~sq_dsottoreport scadenze
PARAMETERS __sigla Value;
SELECT DISTINCTROW * FROM [scadenze per report situazione giorn] AS situazione WHERE ([__sigla] = sigla);
```
Logica (INNER JOIN `codice`, `part_num` **e** `ser_num` Is Not Null):
- **`gg_disp`** = `(ultimo_lic + scad_lic) − Date()` → **giorni alla scadenza LIC** (calendariale).
- **`ore_disp`** = `sottrai_ore(scad_lof, somma_ore(sottrai_ore(Ore_complessive, ore_vlv_imb), sottrai_ore(ore_particolare, ultimo_lof)))`
  = `scad_lof − (ore_attuali − ultimo_lof)` → **ore alla scadenza LOF**.
- **Filtro di visibilità** (`Xscadenze per report situazione giorn`): mostra la parte se
  **`gg_disp < 60` OR `ore_disp < 25` OR `applicabilita = True`**.

---

## Perché il portable sbagliava (analisi causa-radice)

### 1. Filtro motori sbagliato → "– sul motore" e parti fantasma
Il portable filtrava i motori con il criterio **`reale`** = *part_num e ser_num non nulli*. Ma l'Access filtra sulla **presenza del codice** (INNER JOIN), non del seriale. Due effetti opposti, entrambi sbagliati:
- **Motore vero senza seriale** (dato incompleto) → `reale` lo **nasconde** → su un elicottero efficiente la colonna motore mostrava **"–"**. ← il sintomo segnalato.
- **Parte con seriale ma senza codice** (es. sigla **347**, AB205: parte `T53L13B / 30146-D`, `id=1`, **nessuna riga `codice (4,1)`**) → `reale` la **mostrava**, ma l'Access la **scarta** (INNER JOIN fallisce). ← motore di troppo rispetto all'Access.

### 2. Il "motore inesistente" (phantom M2 dell'AB206)
Caso speculare e sottile. Per l'AB206C1 (tv3) la tabella `codice` ha:

| codice | id=1 | id=2 |
|---|---|---|
| tv=3 | `TURBOMOTORE` | **`Parte = NULL`** |

La riga `codice (3,2)` **esiste** (con nome nullo). Quindi `cerca_motori` (INNER JOIN sulla coppia) la **matcha** e l'Access **mostra un "Motore 2" senza nome con ore ≈ ore_complessive** (~6000h): è letteralmente il *"mette ore su motori inesistenti"*. L'AB206 è monomotore → quel M2 non esiste fisicamente.
→ **Scelta di fedeltà:** mostrare il M2 fantasma sarebbe "esattamente come l'Access" ma è il bug che l'utente rifiuta. Si replica la **matematica** dell'Access su tutti i motori **reali** (ore identiche) e si **sopprime solo** la riga fantasma a nome nullo. Filtro finale = **`codice.Parte IS NOT NULL`**: superset di tutti i motori reali, esclude solo i fantasma a nome nullo.

| Sigla / tipo | Access `cerca_motori` letterale | Vecchio `reale` | **Fix `Parte NOT NULL`** |
|---|---|---|---|
| AB206C1 (×24) | M1 reale + **M2 fantasma ~6000h** | M1 reale | **M1 reale, M2 vuoto** ✅ |
| AB205 347 | (scarta: no codice) | **mostra T53L13B** ❌ | **vuoto** ✅ (come Access) |
| AB205 296/349 | vuoto | vuoto | vuoto ✅ |
| T53L13 (×3) | M1 (TURBO MOTORE) | M1 | M1 ✅ |

### 3. Padding "–" cosmetico
Le colonne motore mancanti erano riempite con `<td>–</td>`. Su un monomotore la colonna M2 mostrava "–", letto come "manca il dato". → sostituito con cella **vuota** (`<td></td>`) + `title` tooltip con nome+part_num sui motori presenti.

### 4. Sezione SCADENZE assente
Il report *Situazione* esiste **per gestire le scadenze**, ma il portable non aveva il sotto-report scadenze. → aggiunta sezione **SCADENZE** che replica `Xscadenze per report situazione giorn` (formule sopra), con righe **rosse** se scadute (`gg_disp<0` o `ore_disp<0`) e **gialle** se vicine (`gg_disp<30` o `ore_disp<10`).

---

## Verifica matematica (la registrazione volo era già corretta)
Self-test sul sqlite del portable (python embedded), round-trip su un particolare:
**INSERT** volo `+1:30`, `+2 cicli` → `Ore_totali` e `cicli_tot` salgono su **tutte** le parti della sigla, **ore dei particolari invariate** → **MODIFICA** a `0:30`,`+1` applica il **delta** (nuovo−vecchio) → **DELETE** applica l'**inverso** → ritorno **ESATTO** ai valori di partenza (motori, `Ore_totali`, `Ore_DUR`). **PASS.**
→ Il "non fa i conti giusti" **non** era nei calcoli del volo, ma nella **visualizzazione** (filtro motori + scadenze mancanti).
PK di `sit_giornaliera` = **`progressivo`** (non `contatore`) — `add_sit_giorn` lo restituisce; delete/update lavorano per `progressivo`.

## Fix applicato (3 file in `Documents/SIEL_Portable`)
- **`db.py`** — aggiunta `get_scadenze_situazione(sigla)` + query `_SQL_SCADENZE_SIT` (replica `Xscadenze per report situazione giorn`: `gg_disp`, `ore_disp`, `prossima_lic`, filtro `<60 gg / <25 ore / applicabilita`). CASE-guard per non far collassare a 0 i valori con date/ore vuote.
- **`app.py`** (`report_situazione`) — motori = `[p for p in get_parti(sigla) if str(p.id) in ('1','2') and p.Parte]`; `scadenze = db.get_scadenze_situazione(sigla)`.
- **`templates/report_situazione.html`** — padding motore vuoto (no "–") + `title`; nuova sezione **SCADENZE** (rosso/giallo per urgenza).

Render di prova (Flask test client): **HTTP 200**. Motori: AB205 (296/347/349) vuoti, AB206C1 con solo M1 (es. 532=3650:00, 603=5205:30), T53L13 con M1 (2960=3704:00). Sezione SCADENZE presente.

> ⚠️ Il portable è un **ripiego** per PC senza Access. Soluzione primaria = `Desktop\SIEL.accdb` (vedi [[SIEL]]). La cartella `SIEL_Portable` è **gitignorata** (dati militari, mai committati).

## Collegamenti
- Hub progetto: [[SIEL]]
- Query motori: [[cerca_motori]] · Ore derivate: [[Derivazione Ore Parte]] · Scadenze: [[Scadenze LIC LOF]]
- Anagrafica: [[Tabella codice]] · Flotta: [[Parco Elicotteri]] · Implementazione: [[SIEL Portable]]
- Ambito militare: [[AVES Corsi/AVES Hub]]
- Memoria: `project_siel.md`
