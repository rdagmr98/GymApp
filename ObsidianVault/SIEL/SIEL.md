---
tags: [progetto, siel, aves, access]
---
# SIEL — Sistema Informativo Elicotteri

Gestionale manutenzione/ore di volo elicotteri AVES (Aviazione dell'Esercito).
Origine: file **Access** del reparto. Ambito: [[AVES Corsi/AVES Hub|AVES]].

## ✅ SOLUZIONE DEFINITIVA (2026-06-18) — usare l'Access vero
Il file che funziona ESATTAMENTE come l'originale è **`Desktop\SIEL.accdb`** (copia pulita di `Documents/siel_convertito/siel.accdb`).
- È l'applicazione Access originale **convertita in formato moderno** (.accdb, apribile con Office/Access 2016 in `Office16`).
- Contiene TUTTO: **31 maschere, 19 report, 38 query, 6 moduli VBA**, references OK.
- **Tabelle locali** (nessun collegamento di rete) con i dati: 22.862 voli, 32 elicotteri, 7.822 parti. 4820 parti con scadenze.
- Fedeltà 100% perché **è** l'Access originale, non una riscrittura.

### 🔧 Perché "non funzionava" (inserire voli / scadenze) — RISOLTO
Causa: aprendo l'`.accdb` da una cartella **non attendibile**, Office **disabilita tutte le macro/VBA** → i pulsanti delle maschere (inserisci volo, ecc.) non fanno niente. Non era un bug del file.
Fix applicato su questo PC: cartella `Desktop` resa **posizione attendibile** (registro `HKCU\...\Office\16.0\Access\Security\Trusted Locations`). Verificato: `CurrentProject.IsTrusted=True`, VBA compila, maschera inserimento + report scadenze presenti, dati integri.

### 🔧 Per usarlo sui PC di lavoro (anche da chiavetta) — fatto helper
Sul Desktop c'è **`ABILITA SIEL su questo PC.bat`**: doppio click su qualunque PC →
1. sblocca il *Mark-of-the-Web* sugli `.accdb` (file copiati da rete/USB/mail),
2. rende attendibile la cartella del .bat per ogni Office installato (14/15/16).
Workflow work-PC: copiare INSIEME `SIEL.accdb` + il .bat, lanciare il .bat una volta, aprire l'accdb. Testato: scrive `Path` pulito, `AllowSubfolders=1`.

### 🔁 Ricontrollo 2026-06-18 (segnalazione "pulsanti morti") — la copia Desktop è SANA
Riaperto il caso "l'Access si apre ma se premo i pulsanti non succede nulla". Diagnostica live su `Desktop\SIEL.accdb`:
- **Registro**: `Desktop\` è posizione attendibile (2 voci: `Location100` + `LocationSIEL`, `AllowSubfolders=1`); nessun MOTW sul file; nessuna group-policy di blocco; Office 16 presente.
- **COM DAO (sola lettura)**: tutte le tabelle **locali** (nessun link `\\naspcs4`), dati integri (32 eli, 22862 voli, 7822 parti); `StartupForm=Maschera1`, `StartupShowDBWindow=False`, `AllowFullMenus=False` → app bloccata: **senza macro è del tutto inusabile** (= il sintomo).
- **COM Access**: **`IsTrusted=True`** e **VBA compila** (`RunCommand` acCmdCompileAndSaveAllModules OK → nessun riferimento rotto).
→ **Conclusione**: aperta **dal Desktop** l'app è a posto. Se i pulsanti sono morti, si sta aprendo **un'altra copia** in cartella NON attendibile (es. `Documents\siel_convertito\siel.accdb`) oppure un **PC di lavoro** dove il `.bat` non è stato eseguito. Fix: aprire SEMPRE `Desktop\SIEL.accdb`, o lanciare `ABILITA SIEL su questo PC.bat` nella cartella da cui si apre.
Nota tecnica: `AccessVBOM=1` + `-ExecutionPolicy Bypass` bloccati dal classifier (PC sensibile); diagnosi fatta con COM minimale senza quei due.

### 🔍 Perché "faceva casino con i motori quando modifico i dati" — RISOLTO
**Non era un bug della logica.** Self-test sul sqlite portable (python embedded): INSERT volo +1:30/cicli+2 → MODIFICA 0:30/cicli1 (applica il delta) → DELETE → torna **esatto** ai valori di partenza (motore 347 = 5325:00, Ore_DUR incluse). **PASS.** La derivazione ore motore e l'aggiornamento Ore_totali/Ore_DUR/cicli sono corretti.
Causa vera del casino: c'erano **7 server Flask accesi insieme** (4 orfani dev `siel_app` via `.venv`, 1 da `F:\` USB ora scollegata, 2 dalla cache `SIEL_runtime`), ognuno col **suo** database su porte diverse → aprendo l'uno o l'altro i numeri (ore/motori) non coincidevano. **Tutti chiusi**, stato pulito. Regola: **una sola istanza alla volta**.
Nota: nei sqlite c'è rumore float (`1589.449951171875` ≈ `1589.45`) ma `_parse` lo normalizza; le operazioni lo ripuliscono.

### Disallineamento dati da sapere
Unico volo presente nei Flask ma non nell'`.accdb`: **sigla 532, 17/06/2026, 0:30, pos E, cicli 0** (era in `siel_app/siel.sqlite`; l'accdb arriva al 12/06). Va **reinserito dalla maschera Access** (così il VBA ricalcola), NON a mano in tabella.

## Stato cartelle / file (mappa anti-confusione, 2026-06-18)
| Cosa | Path | Stato |
|---|---|---|
| **Access da usare** | `Desktop\SIEL.accdb` | ✅ ATTIVO (primario) |
| Helper attendibilità | `Desktop\ABILITA SIEL su questo PC.bat` | ✅ per i PC di lavoro |
| Leggimi | `Desktop\LEGGIMI - SIEL (quale usare).txt` | ✅ |
| Sorgente accdb | `Documents/siel_convertito/siel.accdb` | originale convertito |
| **Portable (ripiego no-Access)** | `Documents/SIEL_Portable` | ✅ tenuto come fallback |
| Flask dev duplicato | ~~`Documents/siel_app`~~ | 🗑️ archiviato → `_SIEL_ARCHIVE_NON_USARE\siel_app_dev_duplicato` |
| Front-end .mdb (rete) | `Documents/siel modificabile/Siel.mdb` | solo storico |
| Backend .mdb vecchio | `…/SIEL_BD.MDB` | non apribile nuovo Office |
| **Web app (live)** | `C:\Users\Gianmarco\siel` → Pages + repo `siel-data` | ✅ DEPLOYED — manca solo push dati privati |

## 🔧 Report Situazione — fix motori + scadenze nel portable (2026-06-20)
Segnalazione: *"se aggiungo un volo e guardo la situazione di un elicottero efficiente mi mette il **–** sul motore; è passato da mettere ore su motori inesistenti a non mettere nulla"*. **Non** era un errore di calcolo (round-trip volo = ritorno esatto, vedi sotto) ma di **visualizzazione** nel report *Situazione* del portable. Dettaglio completo (query Access, tabella codice, formule): **[[Logica Motori e Scadenze]]**.
- **Causa motori**: il portable filtrava i motori per *seriale* (`reale` = part_num/ser_num); l'Access filtra per **presenza del codice** (`cerca_motori`, INNER JOIN `codice` su `id`+`tipo_vlv`). → motori veri **senza seriale** nascosti ("–"), e parti **senza codice** mostrate (es. T53 a bordo del 347).
- **"Motore inesistente"**: per l'AB206 (monomotore) la riga `codice (tv3,id2)` esiste ma a **nome NULL** → l'Access letterale mostra un *Motore 2* fantasma ≈ ore cellula (~6000h). Fix: filtro **`Parte IS NOT NULL`** = tutti i motori reali, niente fantasma.
- **Parco attivo = nessun bimotore** → colonna *Motore 2* vuota su tutti gli eli attivi è **corretta** (AB206C1 ×24 monomotore, AB205 ×3 senza codice, T53L13 ×3 sezione singola).
- **"–" cosmetico** sulle colonne mancanti → cella **vuota** + tooltip nome/part_num.
- **Scadenze**: il sotto-report scadenze (lo **scopo** del report) **mancava** → aggiunto, replica `Xscadenze per report situazione giorn`: `gg_disp = (ultimo_lic+scad_lic)−oggi`, `ore_disp = scad_lof−(ore_attuali−ultimo_lof)`, visibile se `gg<60 ∨ ore<25 ∨ applicabilita`. Righe rosse=scaduto, gialle=vicino.
- **File**: `db.py` (`get_scadenze_situazione`), `app.py` (`report_situazione`), `templates/report_situazione.html`. Verifica render Flask = HTTP 200. Cartella gitignorata (dati militari).
- **Conferma calcoli**: self-test INSERT(+1:30,+2 cicli)→MODIFICA(0:30,+1, delta)→DELETE(inverso) = ritorno **esatto** (Ore_totali/Ore_DUR/cicli/motori). I conti del volo erano già giusti.

## ✅ Parità report completata (2026-06-20)
Richiesta utente: *"ci devono essere tutte le funzionalità del file Access, non solo i dati"*. L'Access ha 31 maschere + 19 report; il portable copriva tutto tranne **3 report**. Aggiunti nel portable (`SIEL_Portable`, cartella gitignorata):
- **Elenco Parti Velivolo** (ex *stampa parti II*) → `/report/parti/<sigla>` — pulsante "Stampa elenco" nella pagina Parti + card nel Menu Stampe.
- **Verbale Imbarco componente** → `/report/imbarco/<contatore>` — pulsante "Imb" per riga parte.
- **Verbale Sbarco componente** → `/report/sbarco/<contatore>` — pulsante "Sb" per riga parte (con campi data/ore/motivo sbarco da compilare).
File: `app.py` (3 route), `templates/report_parti.html`, `templates/cert_componente.html`, link in `parti.html` + `stampe.html`. Smoke-test render = **HTTP 200** su tutte e 3. → parità funzionale completa. Mappa: [[Maschere e Report Access]], [[Imbarco Sbarco Parti]].

## Logica Access (riferimento — implementata nel VBA dell'.accdb e replicata nel portable)
- **Ore centesimali**: `1.30 = 1h30m`. `somma_ore`/`sottrai_ore`/`format_ore`.
- **Ore attuali parte (derivata, NON memorizzata)**:
  `ore_attuali = somma_ore(sottrai_ore(somma_ore(Ore_totali, Ore_iniziali), ore_vlv_imb), ore_particolare)`.
- **Inserimento volo**: `Ore_totali += ore_giorno`; `Ore_DUR += ore_giorno` se `ore_dur_appl`; `cicli_tot += cicli` su tutte le parti della sigla. Mai le ore dei particolari.
- **Modifica volo** = applica il DELTA (nuovo−vecchio). **Cancella** = applica l'inverso.
- **Parti phantom** (monomotore): `part_num`/`ser_num` vuoti ⇒ nascoste nei report ma cicli comunque incrementati.

## Web app — ✅ LIVE (2026-06-18)
Static GitHub Pages: repo **pubblico** `rdagmr98/siel` (solo guscio codice, **zero dati**) + repo **PRIVATO** `siel-data` (un JSON per tabella), PAT in localStorage (mai nel codice). **Online: https://rdagmr98.github.io/siel/** (index + js/app.js → 200).
- Completato `app.js` (SPA hash-router, ~912 righe): **23 route** = tutte le maschere/report dell'Access — dashboard, situazione giornaliera/mensile, gestione eli (ins/canc), parti, codici (ins/mod), stampe (situazione, mensile, giornaliero a intervallo, prospetto manutenzione, matricole, codici per tipo, lic/lof), utilità ente + indirizzi. Commit `fe23495`; deploy via workflow `pages.yml` (run OK).
- **Smoke test (Node) PASS**: 23/23 route renderizzano senza eccezioni; round-trip volo insert(+1:30, +2 cicli) → modifica(0:30, +1) → delete riporta motori, `Ore_totali`, `Ore_DUR` e cicli **ESATTAMENTE** ai valori di partenza → la logica motori è fedele all'Access (stessa preoccupazione "fa casino coi motori" → coperta).
- ⚠️ **Manca un solo passo per i dati reali**: il repo privato `siel-data` ha la **default branch VUOTA**. I JSON sono già esportati in locale (`C:\Users\Gianmarco\siel-data`, commit `a5a1a6c`, tutte le tabelle) ma **non ancora pushati** (`origin/main [gone]`). Finché non si pusha, l'app online carica vuoto. Il push = dati militari reali su GitHub (repo privato) ⇒ **richiede OK esplicito** prima di procedere.
- Per il lavoro quotidiano resta primario l'`.accdb`; la web app serve per accesso web/mobile. Dati militari ⇒ SEMPRE repo privati, mai pubblici.

## Mappa note (cluster SIEL)
**Logica / dominio**
- [[Ore Centesimali]] — convenzione 1.30 = 1h30
- [[Registrazione Volo]] — come il volo aggiorna ore e cicli
- [[Derivazione Ore Parte]] — ore parte derivate, non memorizzate
- [[cerca_motori]] — query motori del report Situazione
- [[Scadenze LIC LOF]] — limiti calendario/ore, logica revisioni
- [[Tabella codice]] — anagrafica componenti per tipo
- [[Parco Elicotteri]] — flotta attiva e schema motori
- [[Imbarco Sbarco Parti]] — montaggio/smontaggio componenti + verbali
- [[Logica Motori e Scadenze]] — deep-dive + bugfix motori

**Implementazioni**
- [[Access accdb]] — soluzione primaria (l'Access vero)
- [[Maschere e Report Access]] — parità funzionale (31 maschere, 19 report)
- [[SIEL Portable]] — Flask + SQLite (ripiego USB)
- [[SIEL Web App]] — SPA GitHub Pages

## Collegamenti
- Memoria: `project_siel.md`
- Ambito militare: [[AVES Corsi/AVES Hub]]
