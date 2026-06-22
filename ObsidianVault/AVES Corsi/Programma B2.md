# Programma B2 — TB2 Manutentore Tecnico Avionico

Fonte: `C:\Users\Gianmarco\Documents\programmi\b2.pdf` (testo nativo, non scansione).
CourseType in `reference.json`: `id: "b2"`. 12 moduli: **1,2,3,4,5,6,7,8,9,10,13,14** (11/12 esclusi — coerente con la natura "ridotta" del programma Esercito). Totale teorico ~1440h + pratica ~320h (somma per modulo ≈ 1755h citato in [[Riferimenti Documentali]]).

**Stato**: `levelB2` (1/2/3 Part-66) scritto per 80/87 sottomoduli, commit `cc9780d`, pushato 2026-06-22. Vedi [[GitHub JSON DB Corsi]].

## Metodologia
- Estrazione testo con PyMuPDF (`fitz`, `get_text()`), dump grezzi in `Documents/programmi/dump_*.txt`.
- Trascrizione manuale leaf-by-leaf (codice, nome, Livello B2, Ore Teoria) + **cross-check aritmetico**: somma di tutte le foglie di un modulo deve combaciare esattamente col TOTALE stampato a fondo modulo. Verificato esatto su tutti i 12 moduli.
- **Convenzione "Pratica\*"**: header con asterisco → niente ore pratiche riga-per-riga, solo un totale forfettario a piè di modulo (M3=20h, M4=12h, M5=9h, M7=70h, M13=179h, M14=30h). Header "Pratica" senza asterisco (M6, M8, M9, M10) → valori reali riga-per-riga, spesso "/" (=0).
- **Convenzione "N/A"**: righe con N/A sia su Livello che su Teoria = argomento senza livello/ore assegnati in questo specifico syllabus Esercito. Trattato come NODATA, mai inventato un valore.
- **Convenzione "aggregate-max"**: quando una entry di `reference.json` raggruppa più sotto-voci del PDF, il livello assegnato = MAX tra i livelli delle sotto-voci (l'argomento ombrello richiede la competenza della sua parte più impegnativa).

## Scoperta — `reference.json` ha liste sottomoduli incomplete rispetto al PDF
I moduli sotto hanno hours-per-topic che sommano correttamente al totale di modulo, ma **non includono tutte le righe del PDF** — segno che la lista è stata scritta a mano riproducendo solo il totale, non la scomposizione reale:

| Modulo | Righe PDF mancanti in ref | Ore mancanti |
|--------|---------------------------|---------------|
| 1 (Mathematics) | "1.4 Statistics" in ref non ha alcuna fonte PDF | 10/70 |
| 3 (Electrical Fund.) | 3.13–3.18 | 29/90 |
| 4 (Electronic Fund.) | "4.4 Filters" non ha fonte nel PDF modulo 4 — il contenuto reale è in PDF modulo 3 "3.16 Filters" (cross-modulo) | — |
| 5 (Digital/EIS) | 5.8–5.15 | 72/150 |
| 6 (Materials/Hardware) | 6.9–6.11 | 23/120 |
| 9 (Human Factor) | 9.5–9.9 | 9/22 |
| 10 (Aviation Legislation) | 10.4–10.7 | 21/28 (**75% del modulo!**) |

**Deciso**: non restrutturare le liste in questa fase (rischio di impattare assunzioni UI/admin su numero righe) → deferred a Task #60. In questa fase: solo `levelB2` sulle entry esistenti via name-matching, gap documentati qui.

## Scoperta — Modulo 13: nomi e ore disallineati
I nomi dei 22 sottomoduli in `reference.json` seguono l'**ordine pedagogico standard EASA** (Theory of flight, Airframe structures, Air conditioning, Avionics, Electrical power...), ma le **ore sono state assegnate posizionalmente** dal PDF — che è invece in **ordine ATA/System-number** (Theory of flight, Airframe, Autoflight Sys22, Comm/Nav Sys23/34, Electrical Sys24...). Risultato: es. ref "13.7 Fire protection" ha teo=22h, ma 22h è in realtà l'ore di Flight Controls nel PDF (la vera Fire Protection PDF è 17h). Le ore di ref sono quindi **sistematicamente mal etichettate** dalla entry #3 in poi. `levelB2` è stato assegnato per **contenuto reale** (name-matching), non per posizione — quindi level e ore in alcune entry M13 sono internamente inconsistenti (level corretto, ore ereditate dal bug posizionale). Fix delle ore deferred a Task #60.

## Scoperta — Relocazioni cross-modulo (Esercito sposta argomenti EASA standard)
Il programma Esercito a volte sposta un argomento dal modulo EASA standard a un modulo diverso. Tre casi trovati (con match quasi letterale):
- ref **7.4 Aviation fasteners** → nessuna fonte in PDF modulo 7, ma PDF modulo 6 **"6.5 Fasteners"** (lvl max=2)
- ref **7.8 Maintenance documentation** → nessuna fonte in PDF modulo 7, ma frase quasi identica dentro PDF modulo 10 **"10.7(a) Applicable Requirements"**: *"Maintenance documentation: maintenance manuals, structural repair manual, illustrated parts catalogue, etc."* (lvl=2)
- ref **7.10 Electrostatic sensitive devices** → nessuna fonte in PDF modulo 7, ma PDF modulo 5 **"5.12 Electrostatic Sensitive Devices"** (lvl=2, match esatto)

## Sottomoduli esclusi (nessun `levelB2` scritto)
| Codice | Nome ref | Motivo |
|--------|----------|--------|
| 1.4 | Statistics | nessuna fonte PDF |
| 7.6 | Riveting | PDF esplicito N/A/N/A |
| 7.7 | Pipes and hoses | PDF esplicito N/A/N/A |
| 7.9 | Ground support equipment | nessun match in tutto il corpus |
| 13.18 | Emergency equipment | nessun match chiaro |
| 13.19 | Oxygen systems (duplicato di 13.15) | PDF posizionale = Water/Waste, N/A |
| 14.4 | Engine storage and preservation | nessuna fonte PDF (PDF M14 ha solo 3 topic: Turbine Engines, Engine Indicating, Starting/Ignition) |

## Tabelle foglia per modulo (PDF, verificate aritmeticamente)

**M1 Mathematics (TOTALE 70)**: 1.1 Arithmetic lvl2/14, 1.2a Algebra-evaluating lvl2/14, 1.2b Algebra-linear/log lvl1/7, 1.3a Geometry-construction lvl1/7, 1.3b Geometry-graphical lvl2/14, 1.3c Geometry-trig lvl2/14.

**M2 Physics (TOTALE 80)**: 2.1 Matter lvl1/3, 2.2.1 Statics lvl1/8, 2.2.2 Kinetics lvl1/8, 2.2.3a Dynamics-mass lvl1/6, 2.2.3b Dynamics-momentum lvl2/10, 2.2.4a Fluid-specific gravity lvl2/10, 2.2.4b Fluid-viscosity lvl1/8, 2.3a Thermo-temperature lvl2/3, 2.3b Thermo-heat capacity lvl2/7, 2.4 Optics lvl2/7, 2.5 Wave motion/sound lvl2/10.

**M3 Electrical Fund. (TOTALE 90 teo/20\* pra)**: 3.1 lvl1/2, 3.2 lvl2/5, 3.3 lvl2/5, 3.4 lvl1/2, 3.5 lvl2/5, 3.6 lvl2/5, 3.7a lvl2/5, 3.7b lvl1/2, 3.8 lvl2/5, 3.9 lvl2/5, 3.10a lvl2/5, 3.10b lvl2/5, 3.11 lvl2/5, 3.12 lvl2/5, 3.13 lvl2/5, 3.14 lvl2/5, 3.15 lvl2/5, 3.16 Filters lvl1/2, 3.17 lvl2/6, 3.18 lvl2/6.

**M4 Electronic Fund. (TOTALE 120 teo/12\* pra)**: 4.1.1a lvl2/14, 4.1.1b lvl2/20, 4.1.2a lvl2/14, 4.1.2b lvl2/20, 4.1.3a N/A, 4.1.3b lvl2/20, 4.2 PCB lvl2/12, 4.3a N/A, 4.3b Servo lvl2/20.

**M5 Digital/EIS (TOTALE 150 teo/9\* pra)**: 5.1 EIS lvl3/12, 5.2 Numbering lvl2/8, 5.3 Data conversion lvl2/8, 5.4 Data buses lvl2/8, 5.5a Logic lvl2/8, 5.5b Logic lvl2/8, 5.6a N/A, 5.6b Computer struct. lvl2/14, 5.7 Microprocessors lvl2/12, 5.8 lvl2/12, 5.9 lvl2/10, 5.10 lvl2/12, 5.11 lvl2/7, **5.12 Electrostatic Sensitive Devices lvl2/8** (→ fonte cross-modulo per ref 7.10), 5.13 lvl2/7, 5.14 lvl2/8, 5.15 lvl2/8.

**M6 Materials/Hardware (TOTALE 120, pratica reale non asterisco)**: 6.1a/b Ferrous lvl1/5+5, 6.2a/b Non-ferrous lvl1/6+5, 6.3.1a Composite lvl2/9, 6.3.1b/6.3.2/6.3.3 N/A, 6.4a Corrosion lvl1/5, 6.4b lvl2/7, **6.5.1-6.5.4 Fasteners** lvl2/9,lvl2/9,lvl2/9,lvl1/3 (max=2, → fonte cross-modulo per ref 7.4), 6.6a/b Pipes lvl2/9+lvl1/4, 6.7 Springs lvl1/3, 6.8 Bearings lvl2/9, 6.9 lvl2/9, 6.10 lvl1/5, 6.11 lvl2/9.

**M7 Maintenance Practices (TOTALE 170 teo/70\* pra)**: 7.1 Safety lvl3, 7.2 Workshop lvl3, 7.3 Tools lvl3, 7.5 EWIS lvl3, 7.6 Riveting N/A, 7.7 Pipes/hoses N/A, 7.9 Ground support — nessun match. (29 foglie totali, vedi dump file per dettaglio completo).

**M8 Basic Aerodynamics (TOTALE 50)**: 8.1 Atmosphere lvl2/12, 8.2 Aerodynamics lvl2/14, 8.3 Theory of Flight lvl2/12, 8.4 Flight Stability/Dynamics lvl2/12.

**M9 Human Factor (TOTALE 22)**: 9.1 General lvl2/3, 9.2 Performance/Limitations lvl2/3, 9.3 Social Psychology lvl1/4, 9.4 Factors Affecting Performance lvl2/3, 9.5 Physical Environment lvl1/1, 9.6 Tasks lvl1/2, 9.7 Communication lvl2/2, 9.8 Human Error lvl2/3, 9.9 Hazards lvl2/1.

**M10 Aviation Legislation (TOTALE 28)**: 10.1 Regulatory Framework lvl1/3, 10.2 Certifying Staff lvl2/2, 10.3 Approved Maint. Org. lvl2/3, 10.4 Air operations lvl2/3, 10.5a General lvl1/4, 10.5b Documents lvl1/2, [National Noise Certificate, riga ambigua: lvl1/teo=0 risolto per arrotondamento aritmetico], 10.6a Continuing AW lvl1/2, 10.6b lvl2/2, **10.7a Applicable Requirements lvl2/5** (→ fonte cross-modulo per ref 7.8, contiene la frase "Maintenance documentation..."), 10.7b lvl1/2.

**M13 Aircraft Aerodynamics/Structures/Systems (TOTALE 460 teo/179\* pra, 22 topic PDF in ordine ATA)**: 13.1 Theory of Flight lvl1/20 (3 parti), 13.2 Airframe Structures lvl2/11, 13.3 Autoflight Sys22 lvl3/30, 13.4 Comm/Nav Sys23-34 lvl3/50, 13.5 Electrical Power Sys24 lvl3/25, 13.6 Equipment/Furnishings Sys25 lvl3/10, 13.7 Flight Controls Sys27 lvl3/22, 13.8 Instruments Sys31 lvl3/60, 13.9 Lights Sys33 lvl3/10, 13.10 OnBoard Maintenance Sys45 lvl3/20, 13.11 Air Cond/Pressurisation Sys21 lvl3/42 (7 parti), 13.12 Fire Protection Sys26 lvl3/17, 13.13 Fuel Systems Sys28 lvl3/20, 13.14 Hydraulic Power Sys29 lvl3/20, 13.15 Ice/Rain Protection Sys30 lvl3/12, 13.16 Landing Gear Sys32 lvl3/18, 13.17 Oxygen Sys35 lvl3/10, 13.18 Pneumatic/Vacuum Sys36 lvl3/9, 13.19 Water/Waste Sys38 N/A/0, 13.20 Integrated Modular Avionics Sys42 lvl3/18, 13.21 Cabin Systems Sys44 lvl3/18, 13.22 Information Systems Sys46 lvl3/18.

**M14 Propulsion (TOTALE 80 teo/30\* pra)**: 14.1a Constructional arrangement lvl1/10, 14.1b FADEC lvl2/20, 14.2 Engine Indicating Systems lvl2/25, 14.3 Starting/Ignition Systems lvl2/25. (Solo 3 topic PDF; ref ne ha 4 — "Engine storage and preservation" senza fonte.)

---

# Programma B2mil — TB2 MIL Estensione Sistemi Militari

Fonte: `C:\Users\Gianmarco\Documents\programmi\b2mil.pdf` (titolo metadata "01_TB2_MIL_Ed_1.pdf", Ed. 01.00, 07/2024, doc.rif "M_D A512B1E REG2024 0013974 05-09-2024"). **PDF interamente vettoriale**: zero testo estraibile (`get_text()` vuoto su tutte le 17 pagine), font convertiti in curve (anti-copia) — niente immagini raster nemmeno. Estrazione fatta rendering pagina→PNG (`fitz get_pixmap`) + lettura visiva diretta.

Nota: la numerazione interna del documento parte da "Pag. 7 of 23" sulla prima pagina fisica del file (le pagine 1-6, presumibilmente copertina/indice/firme, non sono incluse in questo export). Nessun impatto sui dati.

CourseType in `reference.json`: `id: "b2mil"`, nome "TB2 MIL - Estensione B2 Sistemi Militari". 5 moduli: **50 (Principles of Armament), 51 (Weapons Systems), 53 (Surveillance and Electronic Warfare), 54 (Crew Safety), 55 (Military Communication Systems)**. Totale 90h teoria + 40h pratica = 130h (verificato anche da nota a margine PDF su "FASE B - PRACTICAL ELEMENT": 40 ore pratiche distribuite sui moduli 50/51/53/54/55).

**Stato**: già presente in reference.json da prima di questo task (con `levelB2` su tutti i 7 sottomoduli) — **ma 4/7 livelli e 2/7 ore erano sbagliati**. Corretto e verificato pagina-per-pagina, commit `c3ee5a2`, pushato 2026-06-22.

## Correzioni applicate (PDF → valore corretto)
| Codice | Campo | Prima (sbagliato) | Dopo (da PDF) |
|--------|-------|--------------------|----------------|
| 50.1 | levelB2 | 2 | **1** |
| 51.1 | levelB2 | 3 | 3 (già corretto) |
| 53.1 | levelB2 | 2 | **3** |
| 53.2 | theoryHours | 6 | **5** |
| 53.3 | theoryHours | 9 | **10** |
| 53.3 | levelB2 | 2 | **3** |
| 54.1 | levelB2 | 3 | **2** |
| 55.1 | levelB2 | 2 | **3** |

Totali di modulo (25h teoria/10h pratica per M53) restano invariati: lo scambio 6↔9 vs 5↔10 è uno spostamento interno tra 53.2/53.3, non un errore di somma.

## Scoperta — Modulo 54 "Crew Safety" classificato B1 anche dentro il programma B2
Sulla tabella PDF del modulo 54 l'intestazione di colonna è **"B1"** (non B2), con livello=2. Modulo 54 esiste anche come modulo del courseType `b1mil` (fonte: `b1mil.pdf`, non riverificato in questa sessione) con valori completamente diversi (teo=40/pra=15/levelB1=3 — quindi è una tabella indipendente, non lo stesso dato riusato). Interpretazione adottata: per i tecnici B2 che seguono comunque il modulo Crew Safety (ejection seat, escape hatch, survival kit — argomenti tipicamente B1/strutturali), il programma richiede solo il livello equivalente-B1 (2) anche all'interno del percorso B2mil — non è un errore di stampa del template, è intenzionale (stessa logica dei moduli EASA standard con colonne B1/B2 a livello diverso sullo stesso argomento). Il valore 2 è stato preso alla lettera dalla tabella, indipendentemente dall'etichetta di colonna.

## Verifica aritmetica
Teoria: 15(50.1) + 20(51.1) + 10+5+10(53.x) + 14(54.1) + 16(55.1) = 90 ✓
Pratica: 5 + 10 + 4+2+4 + 10 + 5 = 40 ✓
Totale 130h — combacia con [[Riferimenti Documentali]].

---

# Programma B2-da-B1.3 — Delta per chi ha già B1.3+estensione mil.

Fonte: `C:\Users\Gianmarco\Documents\programmi\01_BTC_MAML_B2_da_B1_3_AVES.pdf` (testo nativo, dump in `dump_b2dab13.txt`, 2390 righe/39 pagine). Stato: Approvato, Ed. 0.0/2025, doc.rif "M_D A535366 REG2025 0045761 31-10-2025". Redatto da Ten. Gianmarco Ardia/Ten. Biagio Palmieri (Capo Sezione Manutentori Aeromobili Militari — Capo Nucleo BTC), approvato Gen.D. Salvatore Annigliato.

**Cosa è**: NON un programma B2 completo — è il delta minimo che un tecnico già MAML B1.3 (elicottero turbina) **con estensione ai moduli militari M50/M51/M53/M54** (cioè BTC B1.3 o TB1 + estensione mil.) deve seguire per arrivare a B2. Copre solo le differenze peculiari tra B1.3 e B2 sui moduli in comune (4,5,7,13,14,51,53) + il modulo 55 interamente nuovo (B1.3 non lo prevede). I moduli 50 e 54 NON compaiono: il livello B2 richiesto è già coperto dall'estensione mil. B1.3 esistente.

CourseType in `reference.json`: nuova chiave top-level `deltaCourses` (sibling di `courseTypes`), `id: "b2_da_b1_3"`. Max 28 frequentatori teoria, max 15/istruttore pratica (147.A.100(f)/AMC 147.A.100(b)). **Totale 378h teoria + 63h pratica (41 task), 17 settimane** — verificato aritmeticamente: ogni TOTALE di modulo combacia, somma task pratici = ore pratiche di modulo, somma moduli = 378/63. Commit `5235c76`, pushato 2026-06-22.

## Perché uno schema diverso da B2/B2mil: niente `practicalHours` per-sottomodulo

A differenza di B2 e B2mil (dove ogni sottomodulo ha una sua riga pratica reale nel PDF), questo documento dà le ore pratiche **solo a livello di modulo**, derivate dalla somma di una tabella di task numerati (41 task, ognuno con capitolo ATA, codice sottomodulo di riferimento, descrizione, durata). Non esiste nel PDF nessuna riga "pratica per sottomodulo" da cui leggere un valore. Inventare una distribuzione per-sottomodulo avrebbe significato fabbricare dati su un programma di certificazione militare ufficiale — scelta scartata.

**Soluzione adottata**: ogni modulo ha `practicalHours` reale a livello di modulo + un array `practicalTasks` con i 41 task verbatim dal documento (numero, ATA, codice sottomodulo collegato, descrizione, modalità sempre "PERFORM", durata). I sottomoduli hanno solo `theoryHours` e `levelB2` (niente `practicalHours` per sottomodulo — più fedele al documento che inventare uno zero o una proporzione).

## Tabelle foglia per modulo (verificate aritmeticamente, zero discrepanze trovate)

**M4 Electronic Fundamentals (TOTALE 70 teo/12 pra, esame 20 domande/25min)**: 4.1.1 Diodes lvl2/20, 4.1.2a Transistors-symbols lvl2/6, 4.1.2b Transistors-construction lvl2/20, 4.1.3 Integrated Circuits lvl2/12, 4.2 PCB lvl2/4, 4.3 Servomechanisms lvl2/8.

**M5 Digital Techniques/EIS (TOTALE 70 teo/4 pra, esame 32/40min)**: 5.1 EIS lvl3/5, 5.2 Numbering Systems lvl2/4, 5.3 Data Conversion lvl2/4, 5.5 Logic Circuits lvl2/8, 5.6 Basic Computer Structure lvl2/7, 5.7 Microprocessors lvl2/12, 5.8 Integrated Circuits lvl2/12, 5.9 Multiplexing lvl2/10, 5.10 Fibre Optics lvl2/8.

**M7 Maintenance Practices (TOTALE 5 teo/3 pra, esame 4/5min)**: 7.4 Avionic General Test Equipment lvl3/5 (unico leaf, pratica 3h dichiarata diretta).

**M13 Aircraft Aerodynamics/Structures/Systems (TOTALE 210 teo/28 pra, esame 116/145min, 17 leaf)**: 13.1 Theory of Flight lvl1/6, 13.2 Structures lvl2/6, 13.3 Autoflight Sys22 lvl3/27, 13.4a Comm/Nav fondamenti lvl3/17, 13.4b Comm/Nav sistemi lvl2/27 (MLS/VLF-Omega = N/A, escluso), 13.6 Equipment/Furnishings Sys25 lvl3/10 (Cabin entertainment = N/A, escluso), 13.7 Flight Controls Sys27 lvl2/6, 13.8 Instruments Sys31 lvl3/45, 13.10 OnBoard Maintenance Sys45 lvl3/10, 13.11 Air Cond/Pressurisation lvl3/9 (4 parti, max), 13.13 Fuel Systems Sys28 lvl3/2 (2 parti, max), 13.15 Ice/Rain Protection lvl3/1, 13.16 Landing Gear lvl3/2, 13.17 Oxygen Sys35 lvl3/10, 13.20 Integrated Modular Avionics Sys42 lvl3/7, 13.21 Cabin Systems Sys44 lvl3/18, 13.22 Information Systems Sys46 lvl3/7.

**M14 Propulsion (TOTALE 4 teo/11 pra, esame 4/5min)**: 14.2 Engine Indicating Systems (Manifold pressure, Propeller speed) lvl2/4 — unico leaf teorico, ma i 7 task pratici (11h) spaziano anche su 14.1 e 14.3 (argomenti senza teoria propria in questo delta, già coperti da B1.3).

**M51 Weapons Stores System (TOTALE 1 teo/0 pra, esame 4/5min)**: 51.1 Weapons Stores System Sys94 lvl3/1.

**M53 Surveillance and Electronic Warfare (TOTALE 2 teo/0 pra, esame 4/5min)**: 53.1 Surveillance Sys93 lvl3/1, 53.3 Electronic Warfare Sys99 lvl3/1.

**M55 Military Communication Systems (TOTALE 16 teo/5 pra, esame 16/20min)**: 55.1 Military Communication Systems (Tactical Data Links 11/16/22, Tactical Comm Systems) lvl3/16 — interamente nuovo, B1.3 non lo prevede.

## Scoperte particolari
- **Task pratici non sempre mappano sui leaf teorici**: il task #8 (Modulo 5) referenzia codice "5.12", che non esiste nella lista teorica del Modulo 5 (ferma a 5.10) — è lo stesso codice "Electrostatic Sensitive Devices" già visto come fonte cross-modulo in [[Programma B2]] M5. Il Modulo 14 ha teoria solo su 14.2, ma i suoi 7 task pratici toccano 14.1 (1 task), 14.2 (5 task) e 14.3 (1 task).
- **Refuso di stampa risolto per via aritmetica**: il task pratico #39 (Modulo 55, "Istallazione pannello di comando impianto VHF/AM") stampa la durata come "100" invece di "1:00" — dedotto perché i 5 task del Modulo 55 devono somministrare esattamente le 5h del TOTALE pratico di modulo.
- **Nessun altro errore trovato**: a differenza di b2mil.pdf (7 correzioni), questo documento ha superato la riverifica aritmetica completa (ogni modulo + totali generali + tabella riassuntiva pag.38) senza alcuna discrepanza.

## "Combinazioni possibili" — perché non è un semplice calcolo
La richiesta originale chiedeva di generare *tutte* le combinazioni delta per chi ha già dei moduli alle spalle (es. B1.1→B2, B1.2→B1.4, Laurea→B1.3, ecc.). Decisione presa: **non calcolare ore delta per sottrazione aritmetica tra programmi diversi** (es. "ore B2 modulo X meno ore B1.1 modulo X") — i delta reali AVES nascono da una Training Needs Analysis dedicata che decide quali argomenti sono davvero nuovi e quali sono "differenze peculiari" (vedi nota pag.13 del documento: per i moduli 4,5,7,13,14,51,53 si trattano "le sole differenze peculiari tra B1.3 e B2", non l'intero modulo — un calcolo aritmetico non lo saprebbe distinguere).

Implementato in `reference.json` → `deltaCombinations`: matrice delle 6 categorie EASA/AMC (Laurea, B1.1, B1.2, B1.3, B1.4, B2), con la sola coppia **B1.3+estensione_mil(M50,51,53,54) → B2** marcata `documented` (= questo deltaCourse), e tutte le altre coppie esplicitamente `undocumented` con nota che richiedono una TNA dedicata prima di poter diventare un deltaCourse reale.

---
← [[Corsi EASA]] · [[Riferimenti Documentali]]
