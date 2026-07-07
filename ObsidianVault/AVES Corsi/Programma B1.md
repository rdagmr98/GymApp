# Programma B1 — TB1 Manutentore Tecnico di Linea

CourseType in `reference.json`: `id: "b1"`. Moduli 1-12 + 15-18 (16 totali). Totale **2074h** (teoria 1680 + pratica 394) — verificato e scritto in `reference.json` nel Task #56 (sessione precedente, levelB1 su tutti i sottomoduli). Dettaglio modulo-per-modulo non documentato in questa nota (vedi commit storici `corsi-data` per il diff del Task #56); questa nota si concentra sull'estensione B1mil, riverificata nel Task #61.

---

# Programma B1mil — TB1 MIL Estensione Sistemi Militari

Fonte: `C:\Users\Gianmarco\Documents\programmi\b1mil.pdf` (titolo metadata "TB1 MIL: Estensione del Basic Training ai sistemi specifici militari", Stato: Approvato, Numero Edizione 01.00, Data Edizione 06/2024). PDF con testo estraibile, rendering pagina→PNG per lettura tabelle. Numerazione interna parte da pag. 7 (le pagine 1-6, copertina/indice, non rese); documento totale 22 pagine stampate, 16 rese.

CourseType in `reference.json`: `id: "b1mil"`, nome "TB1 MIL - Estensione B1 Sistemi Militari". 4 moduli: **50 (Principles of Armament), 51 (Weapons Systems), 53 (Surveillance and Electronic Warfare), 54 (Crew Safety)**. Si aggiunge a B1 (estensione via `extensionTypeId`, fusa a runtime da `getEffectiveCourseType`), non lo sostituisce. Totale **138h** (teoria 98 + pratica 40).

**Stato**: già presente in reference.json da prima di questo task (con `levelB1` su tutti i sottomoduli ed `examQuestions`/`examMinutes` per modulo) — **ma 1/6 livelli era sbagliato e tutti i 25 task pratici della sez. "FASE B - PRACTICAL ELEMENT" mancavano**. Corretto e verificato pagina-per-pagina, commit `corsi-data` `a5bc8ba`, pushato 2026-06-22.

## Correzioni applicate (PDF → valore corretto)
| Codice | Campo | Prima (sbagliato) | Dopo (da PDF) |
|--------|-------|--------------------|----------------|
| 50.1 | levelB1 | 2 | **1** (PDF mostra livello 1 uniforme sui 3 blocchi di contenuto) |
| 51.1 | levelB1 | 3 | 3 (già corretto — max tra blocchi a livello 3 e 2) |
| 53.1 / 53.2 / 53.3 | levelB1 | 2 | 2 (già corretto) |
| 54.1 | levelB1 | 3 | 3 (già corretto) |
| tutti i moduli | examQuestions/examMinutes | — | già corretti (12/15, 28/35, 32/40, 20/25), nessuna modifica |

## Task pratici aggiunti (25, id 154-178)
Tabella "FASE B - PRACTICAL ELEMENT" del PDF (pag. 19-22), numerazione N continua 1-25 su tutto il documento (non riparte per modulo). ID globali assegnati come `153 + N` (153 = max precedente, dopo l'integrazione del delta B2-da-B1.3 nel Task #60). Colonna "Modalità" (PERFORM/ASSIST) documentata qui solo a titolo storico-PDF: il modello Dart `PracticalTask` non ha un campo modalità (solo `id`, `name`, `plannedHours`), quindi non è scritta in `reference.json`.

| Sottomodulo | N (PDF) | ID | Task | Modalità | Ore |
|---|---|---|---|---|---|
| 50.1 | 1 | 154 | Assemblaggio razzi | PERFORM | 1 |
| 50.1 | 2 | 155 | Disasseblaggio razzi | PERFORM | 1 |
| 50.1 | 3 | 156 | Caricamento magazzino Flares/Chaff | PERFORM | 1 |
| 50.1 | 4 | 157 | Scaricamento magazzino Flares/Chaff | PERFORM | 1 |
| 50.1 | 5 | 158 | Stray voltage test | ASSIST | 1 |
| 51.1 | 6 | 159 | Installazione supporto universale per sistema d'arma | ASSIST | 2 |
| 51.1 | 7 | 160 | Installazione "kit installazione" sistema d'arma | ASSIST | 3 |
| 51.1 | 8 | 161 | Rimozione "kit installazione" sistema d'arma | ASSIST | 2 |
| 51.1 | 9 | 162 | Rimozione supporto universale per sistema d'arma | ASSIST | 1 |
| 51.1 | 10 | 163 | Allineamento congegno di puntamento e sistema d'arma | PERFORM | 1 |
| 51.1 | 11 | 164 | Messa in fase dell'assieme arma | PERFORM | 1 |
| 53.1 | 12 | 165 | Rimuovere e installare il pannello di comando del "WEATHER RADAR" | ASSIST | 2 |
| 53.1 | 13 | 166 | Rimuovere e installare sistema IFF e criptocomputer | ASSIST | 2 |
| 53.2 | 14 | 167 | Rimuovere e installare il pannello del Sistema di videoregistrazione (VCTR) | ASSIST | 2 |
| 53.3 | 15 | 168 | Rimuovere e installare lanciatori chaff e flare del sistema di autoprotezione | ASSIST | 4 |
| 54.1 | 16 | 169 | Rimuovere porte piloti tramite lo sgancio di emergenza | PERFORM | 1 |
| 54.1 | 17 | 170 | Rimontare porte piloti dotate di sgancio di emergenza | PERFORM | 2 |
| 54.1 | 18 | 171 | Effettuare frenatura alla maniglia di sgancio per una porta dotata di sgancio di emergenza | PERFORM | 1 |
| 54.1 | 19 | 172 | Rimuovere i trasparenti delle porte di carico scorrevole tramite lo sgancio di emergenza | PERFORM | 1 |
| 54.1 | 20 | 173 | Rimontare i trasparenti delle porte di carico scorrevole dotate di sgancio di emergenza | PERFORM | 2 |
| 54.1 | 21 | 174 | Identificazione alloggiamenti del cordone esplosivo | PERFORM | 1 |
| 54.1 | 22 | 175 | Identificazione della miccia detonante | PERFORM | 1 |
| 54.1 | 23 | 176 | Identificazione della guaina di trasferimento | PERFORM | 1 (PDF: 1:30, arrotondato — vedi nota sotto) |
| 54.1 | 24 | 177 | Identificazione della connessione a sei vie del Sistema esplosivo di uscita | PERFORM | 2 (PDF: 1:30, arrotondato) |
| 54.1 | 25 | 178 | Prova funzionale dei galleggianti di emergenza | ASSIST | 3 |

**Nota ore frazionarie (task 23/24)**: il PDF indica 1:30 per entrambi. `PracticalTask.plannedHours` nel modello Dart è `int` (verificato: nessun precedente frazionario in tutto `reference.json`, range osservato 1-6h interi). Arrotondati a 1h/2h rispettivamente per mantenere invariata la somma del sottomodulo (15h, già corretta in `reference.json` prima di questo task) — scelta arbitraria su quale dei due arrotondare in su/giù, ma la somma del sottomodulo torna esatta.

## Scoperta — task_id legacy stringa in `schedules.json` ("1 m"-"25 m")
165 record storici di lezioni pratiche già pianificate (tutti sul corso `extension_type_id: "b1mil"`, id corso `d3d468d5-eb15-43af-985f-58dd4b4e02e4`) referenziavano i task pratici di b1mil con `task_id` stringa nel formato `"N m"` (N=1-25) invece di un intero. Dato che le `practicalTasks` di b1mil erano sempre state vuote (0 task) finché non scritte in questo task, quelle lookup (`taskName()`, `taskRemaining`) tornavano sempre `null` — comportamento già previsto e commentato nel codice (`schedule_models.dart`/`reference_service.dart`: "String per task MIL legacy... non c'è corrispondenza, si torna null"), quindi non un crash, ma un gap noto e mai chiuso.

Causa identificata: i nomi/id "N m" sono un residuo di un import precedente alla modellazione `practicalTasks` di b1mil — verificato leggendo `schedule_tab.dart` (il task-picker è un `DropdownButtonFormField<dynamic>` popolato solo da `selSub.practicalTasks`, nessun path di inserimento stringa libera) che nessuna UI corrente può produrre questo formato. Cross-validati i 165 record con il loro stesso campo `submodule_code` (es. N=1-5→"50.1p", N=6-11→"51.1p", N=12-13→"53.1p", N=14→"53.2p", N=15→"53.3P", N=16-25→"54.1p"): corrispondenza esatta col raggruppamento ricavato dal PDF — forte conferma indipendente sia della transcrizione PDF sia dello schema di migrazione.

**Fix**: migrazione one-time (non uno shim di compatibilità) `"N m"` → intero `153+N`, eseguita su tutti i 165 record in `schedules.json`. Nessuna modifica di codice Dart necessaria.

### Nota tecnica — conflitto con scritture live durante il push
Tra l'inizio di questo task e il push, l'app live ha scritto 6 commit reali su `corsi-data` (utenti/presenze/pianificazione), incluso uno che riscriveva `db/schedules.json` per intero in un formato diverso (compatto, senza spazi — verosimilmente `jsonEncode` Dart) rispetto al formato con spazi con cui avevo letto il file all'inizio (verosimilmente scritto in precedenza da uno script Python). File JSON a riga singola → qualsiasi sovrascrittura concorrente produce un conflitto Git testuale "tutto in una riga", anche se i dati toccati non si sovrappongono. Risolto rifacendo la trasformazione (migrazione dei 165 `task_id`) sopra il contenuto più recente di `origin/main` (non quello stantio), confermando che i record legacy erano ancora esattamente 165 e nessuno era stato toccato dalle scritture live nel frattempo; scritto il file risolto nello stesso formato compatto usato dall'app live. Rebase + push completati senza perdita di dati né da una parte né dall'altra.

## Verifica aritmetica
Teoria: 15(50.1) + 20(51.1) + 9+5+9(53.x) + 40(54.1) = 98 ✓
Pratica: 5 + 10 + 4+2+4 + 15 = 40 ✓
Totale 138h — combacia con [[Tipi Corso]] e [[Riferimenti Documentali]].
Task pratici: 5+6+2+1+1+10 = 25 ✓ (somma ore: 5+10+4+2+4+15 = 40 ✓, coerente con pratica totale)

## Relazione con Modulo 54 nel programma B2mil
Il modulo 54 "Crew Safety" esiste anche nel courseType `b2mil` con valori **completamente diversi** (teo=14/pra=10/levelB2=2, colonna PDF etichettata "B1" — vedi [[Programma B2]] sez. B2mil) rispetto a qui (teo=40/pra=15/levelB1=3). Confermato: sono due tabelle PDF indipendenti, non lo stesso dato riusato — nessuna discrepanza, solo lo stesso numero di modulo riusato su percorsi diversi con contenuti/ore/livelli propri.

---

← [[AVES Hub]] · vedi anche [[Programma B2]] · [[Riferimenti Documentali]] · [[Tipi Corso]]
