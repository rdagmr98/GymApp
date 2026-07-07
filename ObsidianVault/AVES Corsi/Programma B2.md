# Programma B2 — TB2 Manutentore Tecnico Avionico

Fonte: `C:\Users\Gianmarco\Documents\programmi\b2.pdf` (testo nativo, non scansione).
CourseType in `reference.json`: `id: "b2"`. 12 moduli: **1,2,3,4,5,6,7,8,9,10,13,14** (11/12 esclusi — coerente con la natura "ridotta" del programma Esercito). Totale teorico ~1440h + pratica ~320h (somma per modulo ≈ 1755h citato in [[Riferimenti Documentali]]).

**Stato**: `level` (1/2/3 Part-66) scritto per 80/87 sottomoduli, commit `cc9780d`, pushato 2026-06-22. **Task pratici completati 2026-06-22/23** (Task #66-70) su tutti i moduli a pratica aggregata — M3, M4, M5, M7, M13, M14 — 84 task inseriti (id 207-290), fonte aggiuntiva `TB2_AVES_RIDOTTO.PDF` (fornito dall'utente dopo che b2.pdf si era rivelato insufficiente per task/id/ore). Moduli 7 e 13 **interamente ristrutturati** (sottomoduli, ore teoria, livelli) secondo la tabella ufficiale AVES — superano la vecchia estrazione da b2.pdf per questi 2 moduli, risolvendo anche il bug "ore disallineate" del Modulo 13 (vedi sotto). Vedi [[GitHub JSON DB Corsi]].

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

**Aggiornamento 2026-06-22/23**: i task pratici inseriti su M3/M4/M5 (commit `c6dd36e`, Task #66-67) **non hanno chiuso questo gap** — è stata corretta solo la distribuzione delle ore pratiche tra i sottomoduli *esistenti*, le righe PDF mancanti (3.13–3.18, 5.8–5.11/5.13–5.15) restano assenti da `reference.json`. Eccezione puntuale: il nuovo stub `5.12` (vedi tabella foglia M5 sotto) copre solo le 3h pratiche del task, non le 8h teoria della riga PDF omonima — quella riga resta nel gap.

## Scoperta — Modulo 13: nomi e ore disallineati
I nomi dei 22 sottomoduli in `reference.json` seguono l'**ordine pedagogico standard EASA** (Theory of flight, Airframe structures, Air conditioning, Avionics, Electrical power...), ma le **ore sono state assegnate posizionalmente** dal PDF — che è invece in **ordine ATA/System-number** (Theory of flight, Airframe, Autoflight Sys22, Comm/Nav Sys23/34, Electrical Sys24...). Risultato: es. ref "13.7 Fire protection" ha teo=22h, ma 22h è in realtà l'ore di Flight Controls nel PDF (la vera Fire Protection PDF è 17h). Le ore di ref sono quindi **sistematicamente mal etichettate** dalla entry #3 in poi. `levelB2` è stato assegnato per **contenuto reale** (name-matching), non per posizione — quindi level e ore in alcune entry M13 sono internamente inconsistenti (level corretto, ore ereditate dal bug posizionale). Fix delle ore deferred a Task #60.

**RISOLTO 2026-06-23** (commit `cdb180e`, Task #69): Modulo 13 interamente ristrutturato da `TB2_AVES_RIDOTTO.PDF` — 22 sottomoduli rinominati in ordine ATA/System-number coerente con le proprie ore (verificato direttamente in `reference.json`: 13.7 = "Flight Controls (System 27)" 22h ✓, 13.12 = "Fire Protection (System 26)" 17h ✓ — esattamente i valori che questa nota già indicava come "veri" da PDF). `practicalHours` di modulo corretto da 174 a **179** (somma reale dei 41 task pratici inseriti, id 250-290). Vedi tabella foglia aggiornata e task pratici più sotto.

## Scoperta — Relocazioni cross-modulo (Esercito sposta argomenti EASA standard)
Il programma Esercito a volte sposta un argomento dal modulo EASA standard a un modulo diverso. Tre casi trovati (con match quasi letterale):
- ref **7.4 Aviation fasteners** → nessuna fonte in PDF modulo 7, ma PDF modulo 6 **"6.5 Fasteners"** (lvl max=2)
- ref **7.8 Maintenance documentation** → nessuna fonte in PDF modulo 7, ma frase quasi identica dentro PDF modulo 10 **"10.7(a) Applicable Requirements"**: *"Maintenance documentation: maintenance manuals, structural repair manual, illustrated parts catalogue, etc."* (lvl=2)
- ref **7.10 Electrostatic sensitive devices** → nessuna fonte in PDF modulo 7, ma PDF modulo 5 **"5.12 Electrostatic Sensitive Devices"** (lvl=2, match esatto)

**SUPERATO 2026-06-23** (commit `37208d4`, Task #68): il Modulo 7 è stato interamente ristrutturato da `TB2_AVES_RIDOTTO.PDF` (29 foglie b2.pdf incomplete → 21 sottomoduli ufficiali 7.1-7.21). I vecchi codici ref "7.4 Aviation fasteners" e "7.10 Electrostatic sensitive devices" **non esistono più**: il nuovo 7.4 è "Avionic General Test Equipment" (13h/3h), il nuovo 7.10 è "Springs" (0h/0h) — topic set interamente diverso, conforme alla tabella ufficiale. La relocazione 7.10→5.12 resta parzialmente valida: il Modulo 5 ha ora un sottomodulo reale `5.12 "Electrostatic sensitive devices"` (stub: 0h teoria/3h pratica, creato solo per il task pratico — la teoria 8h della riga PDF omonima resta nel gap, vedi sopra). Le altre due relocazioni (7.4→6.5 Fasteners, 7.8→10.7a Maintenance documentation) sono **superate**: si riferivano a codici del vecchio modulo 7 (b2.pdf) che non esistono più nel nuovo modulo 7 (tabella ufficiale AVES).

## Sottomoduli esclusi (nessun `level` scritto)
| Codice | Nome ref | Motivo | Aggiornamento 2026-06-23 |
|--------|----------|--------|--------------------------|
| 1.4 | Statistics | nessuna fonte PDF | invariato |
| 7.6 (ora 7.8) | Riveting | PDF esplicito N/A/N/A | confermato, stesso N/A nella nuova tabella ufficiale (codice spostato a 7.8) |
| 7.7 (ora 7.9) | Pipes and hoses | PDF esplicito N/A/N/A | confermato, stesso N/A nella nuova tabella ufficiale (codice spostato a 7.9) |
| 7.9 | Ground support equipment | nessun match in tutto il corpus | **non più presente**: il nuovo Modulo 7 (21 sottomoduli ufficiali) non include questo topic |
| 13.18 | Emergency equipment | nessun match chiaro | **superato**: il nuovo 13.18 è "Pneumatic/Vacuum (System 36)" 9h/0h lvl3 — topic diverso |
| 13.19 | Oxygen systems (duplicato di 13.15) | PDF posizionale = Water/Waste, N/A | **risolto**: il nuovo 13.19 è infatti "Water/Waste (System 38)" 0h/0h — confermata la previsione di questa riga |
| 14.4 | Engine storage and preservation | nessuna fonte PDF (PDF M14 ha solo 3 topic: Turbine Engines, Engine Indicating, Starting/Ignition) | invariato |

## Tabelle foglia per modulo (PDF, verificate aritmeticamente)

**M1 Mathematics (TOTALE 70)**: 1.1 Arithmetic lvl2/14, 1.2a Algebra-evaluating lvl2/14, 1.2b Algebra-linear/log lvl1/7, 1.3a Geometry-construction lvl1/7, 1.3b Geometry-graphical lvl2/14, 1.3c Geometry-trig lvl2/14.

**M2 Physics (TOTALE 80)**: 2.1 Matter lvl1/3, 2.2.1 Statics lvl1/8, 2.2.2 Kinetics lvl1/8, 2.2.3a Dynamics-mass lvl1/6, 2.2.3b Dynamics-momentum lvl2/10, 2.2.4a Fluid-specific gravity lvl2/10, 2.2.4b Fluid-viscosity lvl1/8, 2.3a Thermo-temperature lvl2/3, 2.3b Thermo-heat capacity lvl2/7, 2.4 Optics lvl2/7, 2.5 Wave motion/sound lvl2/10.

**M3 Electrical Fund. (TOTALE 90 teo/20 pra)**: 3.1 lvl1/2, 3.2 lvl2/5, 3.3 lvl2/5, 3.4 lvl1/2, 3.5 lvl2/5, 3.6 lvl2/5, 3.7a lvl2/5, 3.7b lvl1/2, 3.8 lvl2/5, 3.9 lvl2/5, 3.10a lvl2/5, 3.10b lvl2/5, 3.11 lvl2/5, 3.12 lvl2/5, 3.13 lvl2/5, 3.14 lvl2/5, 3.15 lvl2/5, 3.16 Filters lvl1/2, 3.17 lvl2/6, 3.18 lvl2/6. *(righe PDF — il gap 3.13–3.18 verso `reference.json` resta aperto, vedi sopra)*
Task pratici 2026-06-22 (id 207-214, commit `c6dd36e`, fonte `TB2_AVES_RIDOTTO.PDF` FASE B): 3.5 DC sources (8h: id207 Ni-Cd cella 3h, id208 efficienza batteria 3h, id209 collegamento parallelo 2h), 3.6 DC circuits (2h: id210 Kirchhoff), 3.7 Resistance/resistor (5h: id211 Wheatstone 3h, id212 partitori 2h), 3.8 Power (2h: id213 effetto Joule), 3.12 DC motor/generator (3h: id214 starter generator). Somma task = 20h ✓ = practicalHours modulo.

**M4 Electronic Fund. (TOTALE 120 teo/12 pra)**: 4.1.1a lvl2/14, 4.1.1b lvl2/20, 4.1.2a lvl2/14, 4.1.2b lvl2/20, 4.1.3a N/A, 4.1.3b lvl2/20, 4.2 PCB lvl2/12, 4.3a N/A, 4.3b Servo lvl2/20.
Task pratici 2026-06-22 (id 215-220, commit `c6dd36e`): 4.1 Semiconductors (8h: id215 diodi 2h, id216 ponte raddrizzatore 2h, id217 regolatori tensione 2h, id218 raddrizzatori onda 2h), 4.3 Servomechanisms (4h: id219 trasmettitori induttanza 2h, id220 trasmettitori capacità 2h). Somma task = 12h ✓ = practicalHours modulo.

**M5 Digital/EIS (TOTALE 150 teo/9 pra)**: 5.1 EIS lvl3/12, 5.2 Numbering lvl2/8, 5.3 Data conversion lvl2/8, 5.4 Data buses lvl2/8, 5.5a Logic lvl2/8, 5.5b Logic lvl2/8, 5.6a N/A, 5.6b Computer struct. lvl2/14, 5.7 Microprocessors lvl2/12, 5.8 lvl2/12, 5.9 lvl2/10, 5.10 lvl2/12, 5.11 lvl2/7, **5.12 Electrostatic Sensitive Devices lvl2/8** (riga PDF — gap 5.8–5.11/5.13–5.15 verso `reference.json` resta aperto, vedi sopra), 5.13 lvl2/7, 5.14 lvl2/8, 5.15 lvl2/8.
Task pratici 2026-06-22 (id 221-222, commit `c6dd36e`): 5.1 Electronic instrument systems (6h: id221 verifica disposizione strumenti cabina). **Nuovo sottomodulo `5.12` in `reference.json`** "Electrostatic sensitive devices" — stub `theoryHours:0/practicalHours:3`, *non* la riga PDF omonima (che ha 8h teoria, ancora mancante): creato solo per ospitare id222 (3h, azioni prevenzione scariche elettrostatiche). Somma task = 9h ✓ = practicalHours modulo.

**M6 Materials/Hardware (TOTALE 120, pratica reale non asterisco)**: 6.1a/b Ferrous lvl1/5+5, 6.2a/b Non-ferrous lvl1/6+5, 6.3.1a Composite lvl2/9, 6.3.1b/6.3.2/6.3.3 N/A, 6.4a Corrosion lvl1/5, 6.4b lvl2/7, **6.5.1-6.5.4 Fasteners** lvl2/9,lvl2/9,lvl2/9,lvl1/3 (max=2, → fonte cross-modulo per ref 7.4), 6.6a/b Pipes lvl2/9+lvl1/4, 6.7 Springs lvl1/3, 6.8 Bearings lvl2/9, 6.9 lvl2/9, 6.10 lvl1/5, 6.11 lvl2/9.

**M7 Maintenance Practices — RISTRUTTURATO 2026-06-23** (commit `37208d4`, Task #68, fonte `TB2_AVES_RIDOTTO.PDF` tabella ufficiale AVES, sostituisce l'estrazione b2.pdf a 29 foglie incomplete): 21 sottomoduli, **TOTALE 170 teo/70 pra**. 7.1 Safety Precautions lvl3/12 (pra3: id231 dimostrazione sicurezza), 7.2 Workshop Practices lvl3/13 (pra6: id232 cura utensili 3h, id233 utensili ordinari 3h), 7.3 Tools lvl3/13 (pra12: id234 kit pin connettori 4h, id235 multimetro 4h, id236 misure volt/amp/resistenza 4h), 7.4 Avionic General Test Equipment lvl3/13 (pra3: id237 tester Pitot), 7.5 Engineering Drawings/Diagrams/Standards lvl2/8 (pra7: id238 IPC 3h, id239 schema elettrico 4h), 7.6 Fits and Clearances lvl1/5 (pra2: id240 trapani), 7.7 EWIS lvl3/13 (pra17: id241 ricerca guasti 4h, id242 inserim./estraz. pin 4h, id243 riparazione connettore 6h, id244 schemi elettrici 3h), 7.8 Riveting 0/0 (N/A), 7.9 Pipes and Hoses 0/0 (N/A), 7.10 Springs 0/0 (N/A), 7.11 Bearings 0/0 (N/A), 7.12 Transmissions 0/0 (N/A), 7.13 Control Cables 0/0 (N/A), 7.14 Material Handling 0/0 (N/A), 7.15 Welding/Brazing/Soldering/Bonding lvl2/7 (pra3: id245 saldature elettriche), 7.16 Aircraft Weight and Balance lvl2/7 (pra0), 7.17 Aircraft Handling and Storage lvl2/12 (pra11: id246 rifornimento sicurezza 3h, id247 assistenza rifornimento 2h, id248 marshalling NATO-Stanag 3117 6h), 7.18 Disassembly/Inspection/Repair/Assembly Techniques lvl3/38 (pra0), 7.19 Abnormal Events lvl2/7 (pra0), 7.20 Maintenance Procedures lvl2/12 (pra6: id249 modulo DP5069), 7.21 Armament Safety lvl2/10 (pra0). Verifica: Σteoria=170 ✓, Σpratica=70 ✓, 19 task (id231-249) ✓.

**M8 Basic Aerodynamics (TOTALE 50)**: 8.1 Atmosphere lvl2/12, 8.2 Aerodynamics lvl2/14, 8.3 Theory of Flight lvl2/12, 8.4 Flight Stability/Dynamics lvl2/12.

**M9 Human Factor (TOTALE 22)**: 9.1 General lvl2/3, 9.2 Performance/Limitations lvl2/3, 9.3 Social Psychology lvl1/4, 9.4 Factors Affecting Performance lvl2/3, 9.5 Physical Environment lvl1/1, 9.6 Tasks lvl1/2, 9.7 Communication lvl2/2, 9.8 Human Error lvl2/3, 9.9 Hazards lvl2/1.

**M10 Aviation Legislation (TOTALE 28)**: 10.1 Regulatory Framework lvl1/3, 10.2 Certifying Staff lvl2/2, 10.3 Approved Maint. Org. lvl2/3, 10.4 Air operations lvl2/3, 10.5a General lvl1/4, 10.5b Documents lvl1/2, [National Noise Certificate, riga ambigua: lvl1/teo=0 risolto per arrotondamento aritmetico], 10.6a Continuing AW lvl1/2, 10.6b lvl2/2, **10.7a Applicable Requirements lvl2/5** (→ fonte cross-modulo per ref 7.8, contiene la frase "Maintenance documentation..."), 10.7b lvl1/2.

**M13 Aircraft Aerodynamics/Structures/Systems — RISTRUTTURATO 2026-06-23** (commit `cdb180e`, Task #69, fonte `TB2_AVES_RIDOTTO.PDF` tabella ufficiale AVES, risolve il bug "nomi/ore disallineati" — vedi sopra): 22 sottomoduli, **TOTALE 460 teo/179 pra**. 13.1 Theory of Flight lvl1/20 (pra0), 13.2 Structures-General Concept lvl2/11 (pra0), 13.3 Autoflight Sys22 lvl3/30 (pra8: id250-253 Helipilot — API 2h, selettore/pannelli 2h, giroscopio verticale 2h, sensore velocità aria 2h), 13.4 Comm/Nav Sys23-34 lvl3/50 (pra10: id254-256 HF 4h, VHF 3h, ADF 3h), 13.5 Electrical Power Sys24 lvl3/25 (pra38: id257-265, 9 task da 2-5h: breaker, batterie install/verifica, tensione DC/AC, centralina DC, alim. esterna, starter generator, inverter), 13.6 Equipment/Furnishings Sys25 lvl3/10 (pra0), 13.7 Flight Controls Sys27 lvl3/22 (pra0), 13.8 Instruments Sys31 lvl3/60 (pra55: id266-276, 11 task da 5h ciascuno: altimetro, vel.verticale, vel.anemometrica, temp.olio trasm., bulbo termoresistivo, quantità carburante, HSI, ADI, giroscopi direzionali, flux valve, pannello avvisi), 13.9 Lights Sys33 lvl3/10 (pra25: id277-281 cockpit 3h, interne 5h, esterne 5h, faro atterraggio 6h, faro ricerca 6h), 13.10 OnBoard Maintenance Sys45 lvl3/20 (pra0), 13.11 Air Cond/Pressurisation Sys21 lvl3/42 (pra3: id282 riscaldamento/ventilazione), 13.12 Fire Protection Sys26 lvl3/17 (pra8: id283 componenti antincendio 5h, id284 sensore rilevazione 3h), 13.13 Fuel Systems Sys28 lvl3/20 (pra10: id285 carburante bassa pressione 5h, id286 pannello selezione quantità 5h), 13.14 Hydraulic Power Sys29 lvl3/20 (pra11: id287 componenti idraulico 5h, id288 trasmettitore pressione 6h), 13.15 Ice/Rain Protection Sys30 lvl3/12 (pra11: id289 motore tergicristalli 6h, id290 pannello controllo tergicristalli 5h), 13.16 Landing Gear Sys32 lvl3/18 (pra0), 13.17 Oxygen Sys35 lvl3/10 (pra0), 13.18 Pneumatic/Vacuum Sys36 lvl3/9 (pra0), 13.19 Water/Waste Sys38 0/0 (N/A — confermata previsione "Sottomoduli esclusi"), 13.20 Integrated Modular Avionics Sys42 lvl3/18 (pra0), 13.21 Cabin Systems Sys44 lvl3/18 (pra0), 13.22 Information Systems Sys46 lvl3/18 (pra0). Verifica: Σteoria=460 ✓, Σpratica=179 ✓ (corretto da 174), 41 task (id250-290) ✓.

**M14 Propulsion (TOTALE 80 teo/30 pra)**: tabella PDF originaria — 14.1a Constructional arrangement lvl1/10, 14.1b FADEC lvl2/20, 14.2 Engine Indicating Systems lvl2/25, 14.3 Starting/Ignition Systems lvl2/25 (Solo 3 topic PDF; ref ne raggruppa diversamente in 4 sottomoduli, vedi task sotto — "Engine storage and preservation" resta senza fonte).
Task pratici 2026-06-22 (id 223-230, commit `c6dd36e`) sui 4 sottomoduli reali di `reference.json` (nomi propri, non quelli del PDF sopra): 14.1 Turbine engine fundamentals lvl1/20teo (pra6: id223 componenti motore turbina 3h, id224 trim BEEPER 3h), 14.2 Engine systems and components lvl2/30teo (pra21: id225 Chip Detector 3h, id226 termocoppia 3h, id227 temp.olio motore 5h, id228 EGT 5h, id229 termocoppia 5h), 14.3 Engine monitoring and ground operation lvl2/15teo (pra3: id230 candele), 14.4 Engine storage and preservation 15teo/0pra (nessun task, invariato). Somma task = 30h ✓ = practicalHours modulo.

---

# Programma B2mil — TB2 MIL Estensione Sistemi Militari

Fonte: `C:\Users\Gianmarco\Documents\programmi\b2mil.pdf` (titolo metadata "01_TB2_MIL_Ed_1.pdf", Ed. 01.00, 07/2024, doc.rif "M_D A512B1E REG2024 0013974 05-09-2024"). **PDF interamente vettoriale**: zero testo estraibile (`get_text()` vuoto su tutte le 17 pagine), font convertiti in curve (anti-copia) — niente immagini raster nemmeno. Estrazione fatta rendering pagina→PNG (`fitz get_pixmap`) + lettura visiva diretta.

Nota: la numerazione interna del documento parte da "Pag. 7 of 23" sulla prima pagina fisica del file (le pagine 1-6, presumibilmente copertina/indice/firme, non sono incluse in questo export). Nessun impatto sui dati.

CourseType in `reference.json`: `id: "b2mil"`, nome "TB2 MIL - Estensione B2 Sistemi Militari". 5 moduli: **50 (Principles of Armament), 51 (Weapons Systems), 53 (Surveillance and Electronic Warfare), 54 (Crew Safety), 55 (Military Communication Systems)**. Totale 90h teoria + 40h pratica = 130h (verificato anche da nota a margine PDF su "FASE B - PRACTICAL ELEMENT": 40 ore pratiche distribuite sui moduli 50/51/53/54/55).

**Stato**: già presente in reference.json da prima di questo task (con `levelB2` su tutti i 7 sottomoduli) — **ma 4/7 livelli e 2/7 ore erano sbagliati**. Corretto e verificato pagina-per-pagina, commit `c3ee5a2`, pushato 2026-06-22. **Completo**: 0/7 sottomoduli avevano `practicalTasks` — aggiunti tutti i 28, vedi sezione dedicata sotto. Programma B2mil ora interamente verificato (moduli, livelli, ore, task pratici).

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
Sulla tabella PDF del modulo 54 l'intestazione di colonna è **"B1"** (non B2), con livello=2. Modulo 54 esiste anche come modulo del courseType `b1mil` (fonte: `b1mil.pdf`, riverificato nel Task #61 — vedi [[Programma B1]]) con valori completamente diversi (teo=40/pra=15/levelB1=3 — quindi è una tabella indipendente, non lo stesso dato riusato). Interpretazione adottata: per i tecnici B2 che seguono comunque il modulo Crew Safety (ejection seat, escape hatch, survival kit — argomenti tipicamente B1/strutturali), il programma richiede solo il livello equivalente-B1 (2) anche all'interno del percorso B2mil — non è un errore di stampa del template, è intenzionale (stessa logica dei moduli EASA standard con colonne B1/B2 a livello diverso sullo stesso argomento). Il valore 2 è stato preso alla lettera dalla tabella, indipendentemente dall'etichetta di colonna.

## Verifica aritmetica
Teoria: 15(50.1) + 20(51.1) + 10+5+10(53.x) + 14(54.1) + 16(55.1) = 90 ✓
Pratica: 5 + 10 + 4+2+4 + 10 + 5 = 40 ✓
Totale 130h — combacia con [[Riferimenti Documentali]].

## Schema `levelB2`→`level` (Task #50, commit corsi `574c244` + corsi-data `0681c49`)
Il campo `levelB2` citato sopra (e nella tabella "Correzioni applicate") è stato successivamente rinominato in `level` su tutti i courseType: i moduli 1-10 condivisi tra B1/B2 erano duplicati come entry indipendenti in `b1.modules` e `b2.modules`, ciascuna con solo il proprio campo (`levelB1` o `levelB2`) popolato — **mai entrambi insieme su 323/323 sottomoduli verificati**, quindi i due campi erano ridondanti. Stesso discorso per `levelB1`/`levelB2` in b1mil/b2mil. Nessun valore perso nella migrazione, solo il nome del campo è cambiato.

## Task pratici inseriti da b2mil.pdf (28 task, id 179-206, commit corsi-data `99eb3bc`)
A differenza del tentativo precedente (PyMuPDF/`get_text()` vuoto → rendering pagina→PNG), una rilettura diretta del PDF con lo strumento Read di Claude ha estratto il testo nativamente su tutte le 23 pagine senza bisogno di rendering — compresa la tabella *FASE B - Practical Element* (§8, pag. 19-23) con i 28 task pratici sui moduli 50/51/53/54/55.

| Modulo | Sottomodulo | N. task | Ore task | Pratica modulo |
|--------|-------------|---------|----------|------------------|
| 50 | 50.1 | 5 | 5 | 5 ✓ |
| 51 | 51.1 | 6 | 10 | 10 ✓ |
| 53 | 53.1+53.2+53.3 | 2+1+1=4 | 4+2+4=10 | 10 ✓ |
| 54 | 54.1 | 8 | 10 | 10 ✓ |
| 55 | 55.1 | 5 | 5 | 5 ✓ |

Totale: 28 task, 40h pratica — combacia esattamente con il totale dichiarato a pag. 13 ("N° Task Pratici Max 28", "Ore Addestramento Pratico Max 40"). Id task assegnati in continuità dal max precedente (178, ultimo id usato da [[Programma B1]] task #61) → 179-206. Due refusi del PDF corretti in trascrizione (non dati, solo ortografia): "Disasseblaggio" → "Disassemblaggio" (modulo 50), "Istallazione" → "Installazione" (modulo 55, incoerente con lo stesso termine scritto correttamente nel modulo 51 dello stesso documento).

---

# Programma B2-da-B1.3 — Delta per chi ha già B1.3+estensione mil.

Fonte: `C:\Users\Gianmarco\Documents\programmi\01_BTC_MAML_B2_da_B1_3_AVES.pdf` (testo nativo, dump in `dump_b2dab13.txt`, 2390 righe/39 pagine). Stato: Approvato, Ed. 0.0/2025, doc.rif "M_D A535366 REG2025 0045761 31-10-2025". Redatto da Ten. Gianmarco Ardia/Ten. Biagio Palmieri (Capo Sezione Manutentori Aeromobili Militari — Capo Nucleo BTC), approvato Gen.D. Salvatore Annigliato.

**Cosa è**: NON un programma B2 completo — è il delta minimo che un tecnico già MAML B1.3 (elicottero turbina) **con estensione ai moduli militari M50/M51/M53/M54** (cioè BTC B1.3 o TB1 + estensione mil.) deve seguire per arrivare a B2. Copre solo le differenze peculiari tra B1.3 e B2 sui moduli in comune (4,5,7,13,14,51,53) + il modulo 55 interamente nuovo (B1.3 non lo prevede). I moduli 50 e 54 NON compaiono: il livello B2 richiesto è già coperto dall'estensione mil. B1.3 esistente.

CourseType in `reference.json`: **integrato come 5° elemento di `courseTypes`** (Task #60, sessione 20, commit corsi-data `793d5ad`), `id: "b2_da_b1_3"`, `category: "B2"`. Inizialmente scritto (sessione 19, commit `5235c76`) come chiave top-level separata `deltaCourses` — poi scoperto che nessun modello Dart la consumava (vedi sezione "Integrazione finale" sotto). Max 28 frequentatori teoria, max 15/istruttore pratica (147.A.100(f)/AMC 147.A.100(b), metadato ora solo qui, non più nel JSON). **Totale 378h teoria + 63h pratica (41 task), 17 settimane** — verificato aritmeticamente: ogni TOTALE di modulo combacia, somma task pratici = ore pratiche di modulo, somma moduli = 378/63.

## Perché uno schema diverso da B2/B2mil: niente `practicalHours` per-sottomodulo

A differenza di B2 e B2mil (dove ogni sottomodulo ha una sua riga pratica reale nel PDF), questo documento dà le ore pratiche **solo a livello di modulo**, derivate dalla somma di una tabella di task numerati (41 task, ognuno con capitolo ATA, codice sottomodulo di riferimento, descrizione, durata). Non esiste nel PDF nessuna riga "pratica per sottomodulo" da cui leggere un valore. Inventare una distribuzione per-sottomodulo avrebbe significato fabbricare dati su un programma di certificazione militare ufficiale — scelta scartata.

**Soluzione adottata in fase di estrazione (sessione 19)**: ogni modulo aveva `practicalHours` reale a livello di modulo + un array `practicalTasks` con i 41 task verbatim dal documento (numero, ATA, codice sottomodulo collegato, descrizione, modalità sempre "PERFORM", durata). I sottomoduli avevano solo `theoryHours` e `levelB2` (niente `practicalHours` per sottomodulo — più fedele al documento che inventare uno zero o una proporzione). Questa forma "a livello di modulo" non corrisponde però al modello Dart `PracticalTask` (vive in `SubmoduleInfo`, non in `ModuleInfo`) — vedi sezione "Integrazione finale" sotto per la trasformazione applicata in sessione 20.

## Integrazione finale in `courseTypes` (Task #60, sessione 20, commit corsi-data `793d5ad`)

Il delta course è stato spostato da chiave top-level `deltaCourses` a **5° elemento di `courseTypes`** (`id: "b2_da_b1_3"`, `category: "B2"`), conforme a `CourseTypeInfo`. I 41 `practicalTasks` sono stati riancorati dal livello modulo al livello sottomodulo foglia, nella forma `{id, name, plannedHours}` richiesta da `SubmoduleInfo.practicalTasks` (id = descrizione + suffisso `(ATA n)` se presente, plannedHours = durata task in ore).

**Mappa codice-task → sottomodulo foglia**: 4.1→**4.1.1** (task #1-4), 4.3→**4.3** (#5-6), 5.1→**5.1** (#7), 5.12→**5.12 nuovo stub** (#8), 7.4→**7.4** (#9), 13.3→**13.3** (#10-13), 13.4→**13.4.b** (#14-16), 13.8→**13.8** (#17-27), 13.11→**13.11** (#28), 13.15→**13.15** (#29), 14.1→**14.1 nuovo stub** (#30), 14.2→**14.2** (#31-35), 14.3→**14.3 nuovo stub** (#36), 55.1→**55.1** (#37-41).

**3 nuovi sottomoduli stub** creati per codici task senza foglia teorica esistente in questo delta: `5.12` "Electrostatic Sensitive Devices", `14.1` "Constructional arrangement", `14.3` "Starting/Ignition Systems" (tutti con `theoryHours:0`, nessun `levelB2`, solo a contenere i task pratici corrispondenti). ID task assegnati 113-153 (max precedente nel file: 112).

**Rimossi `deltaCourses` e `deltaCombinations`**: erano metadati puramente documentali senza campo Dart corrispondente — sarebbero stati persi al primo save dall'app. Il loro contenuto resta preservato qui in Obsidian (vedi sezione sotto per `deltaCombinations`).

Verificato dopo la trasformazione: 378h teoria/63h pratica/41 task invariati per modulo e nei totali, zero collisioni id su tutto il file, JSON valido, **zero modifiche necessarie al codice Dart** (`getCourseTypes()`, `CourseTypesTab`, `ReferenceService`, `ScheduleService` sono generici sulla lista `courseTypes`; l'unica logica hardcoded b1/b2 — il bottone "+MIL" in `courses_tab.dart:249,497` — è correttamente scoperta e non interferisce con il 5° tipo corso).

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

**Storico (rimosso da `reference.json` in sessione 20, preservato solo qui)**: era implementato come `deltaCombinations`, matrice delle 6 categorie EASA/AMC (Laurea, B1.1, B1.2, B1.3, B1.4, B2), con la sola coppia **B1.3+estensione_mil(M50,51,53,54) → B2** marcata `documented` (= questo deltaCourse, ora `courseTypes[4]`), e tutte le altre coppie esplicitamente `undocumented` con nota che richiedono una TNA dedicata prima di poter diventare un deltaCourse reale. Rimosso perché nessun modello Dart la consumava — il concetto di "combinazioni non documentate" resta valido come nota metodologica, solo non più come dato JSON.

---

# Programma MAML — BTC MAML Cat. B Manutentore di Aeromobili Militari

Fonte: `C:\Users\Gianmarco\Documents\programmi\BTC VFI AVES.pdf` (dump testo in `Documents/programmi/btc_vfi_dump.txt`).

CourseType in `reference.json`: **integrato come nuovo elemento di `courseTypes`** (Task #64/#65, commit corsi-data `12f4139`, pushato 2026-06-23), posizionato tra `b2mil` e `b1` (ordine effettivo del file: b1mil, b2mil, **maml**, b1, b2, b2_da_b1_3). `id: "maml"`, `code: "BTCMAML"`, `name: "BTC MAML Cat. B - Manutentore di Aeromobili Militari"`, `category: "B1"` (vincolo del dropdown UI — categoria EASA più vicina disponibile in app; il corso reale è una certificazione mista B1+B2mil). `maxAttendees: 28`. Schedule (`schedule.mondayThursday`/`friday`/`hoursPerWeek`) verificato **identico campo-per-campo** a `b1mil` (6 slot lun-gio 09:00-16:30, 3 slot ven 08:20-11:40, 27h/settimana).

**11 moduli**: 7, 9, 10, 11, 12, 13, 50, 51, 53, 54, 55. **Totale 275h teoria + 45h pratica, 33 task pratici (id 291-323)** — verificato direttamente in `reference.json`.

## Interpretazione "combo massimale"
Dal messaggio di commit: il corso MAML rappresenta la combinazione massimale **B1.1+B1.2+B2 → B1+B2MIL** — il percorso che porta un tecnico già qualificato su più categorie EASA standard (B1.1 aeroplani turbina + B1.2 aeroplani pistone + B2 avionica) a una singola certificazione integrata B1 con estensione militare B2MIL. Coerente con il contenuto: moduli quasi-vuoti teoricamente (M7: solo 11h, M13: solo 2h — già coperti altrove dal percorso EASA pregresso) insieme a moduli pieni (M12 Helicopter 89h, M50/51/53/54/55 — i moduli militari, unici a portare anche ore pratiche).

## Tabelle foglia per modulo (verificate aritmeticamente in `reference.json`)

**M7 Maintenance Practices (TOTALE 11 teo/0 pra, esame 4 domande/5min)**: 7.5 Engineering Drawings, Diagrams and Standards, Specification S1000D lvl2/10, 7.21 Armament Safety lvl2/1.

**M9 Human Factors (TOTALE 22 teo/0 pra, esame 21/45min)**: 9.1 General lvl2/3, 9.2 Human Performance and Limitations lvl2/3, 9.3 Social Psychology lvl1/4, 9.4 Factors Affecting Performance lvl2/3, 9.5 Physical Environment lvl1/1, 9.6 Tasks lvl1/2, 9.7 Communication lvl2/2, 9.8 Human Error lvl2/3, 9.9 Hazards in the Workplace lvl2/1.

**M10 Aviation Legislation (TOTALE 28 teo/0 pra, esame 41/70min)**: 10.1 Regulatory Framework lvl1/3, 10.2 Certifying Staff-Maintenance lvl2/2, 10.3 Approved Maintenance Organisations lvl2/3, 10.4 Air operations lvl2/3, 10.5 Certification of aircraft/parts/appliances lvl1/6, 10.6 Continuing airworthiness lvl2/4, 10.7 Applicable Requirements lvl2/7.

**M11 Turbine Aeroplane Aerodynamics/Structures/Systems (TOTALE 7 teo/0 pra, esame 4/5min)**: 11A.1 Theory of Flight lvl2/2, 11A.3 Airframe Structures-Aeroplanes lvl2/1, 11A.4 Air Conditioning and Cabin Pressurisation lvl2/1, 11A.10 Fuel Systems lvl3/1, 11A.13 Landing Gear lvl1/1, 11A.14 Lights lvl3/1.

**M12 Helicopter Aerodynamics/Structures/Systems (TOTALE 89 teo/0 pra, esame 32/40min)**: 12.1 Theory of Flight-Rotary Wing Aerodynamics lvl2/20, 12.2 Flight Control Systems lvl3/16, 12.3 Blade Tracking and Vibration Analysis lvl3/24, 12.4 Transmission lvl3/25, 12.7 Instruments/Avionic Systems lvl2/1, 12.9 Equipment and Furnishings lvl2/2, 12.14 Landing Gear lvl3/1.

**M13 Aircraft Aerodynamics/Structures/Systems (TOTALE 2 teo/0 pra, esame 4/5min)**: 13.4 Communication/Navigation (TACAN, GLS, TLS) lvl2/2 — unico sottomodulo (courseType `maml`, distinto dal Modulo 13 di [[Programma B2]] sopra).

**M50 Principles of Armament (TOTALE 15 teo/5 pra, esame 12/15min)**: 50.1 Essential principles of Armament lvl1/15teo, pra5 (5 task id291-295: assemblaggio razzi 1h, disassemblaggio razzi 1h, caricamento magazzino Flares/Chaff 1h, scaricamento magazzino Flares/Chaff 1h, stray voltage test 1h).

**M51 Weapons Systems (TOTALE 20 teo/10 pra, esame 32/40min)**: 51.1 Weapons stores system (System 94) lvl3/20teo, pra10 (6 task id296-301).

**M53 Surveillance and Electronic Warfare (TOTALE 25 teo/10 pra, esame 48/60min)**: 53.1 Surveillance (System 93) lvl3/10teo, pra4 (id302-305), 53.2 Image recording (System 97) lvl2/5teo, pra2 (1 task, id306), 53.3 Electronic warfare (System 99) lvl3/10teo, pra4 (2 task, id307-308).

**M54 Crew Safety (TOTALE 40 teo/15 pra, esame 20/25min)**: 54.1 Crew escape and safety (System 95) lvl3/40teo, pra15 (10 task id309-318).

**M55 Military Communication Systems (TOTALE 16 teo/5 pra, esame 16/20min)**: 55.1 Military Communication Systems lvl3/16teo, pra5 (5 task id319-323).

## Task pratici (33 totali, id 291-323, commit `12f4139`)
| Modulo | Sottomodulo | N. task | Ore task | Pratica modulo |
|--------|-------------|---------|----------|------------------|
| 50 | 50.1 | 5 | 5 | 5 ✓ |
| 51 | 51.1 | 6 | 10 | 10 ✓ |
| 53 | 53.1+53.2+53.3 | 4+1+2=7 | 4+2+4=10 | 10 ✓ |
| 54 | 54.1 | 10 | 15 | 15 ✓ |
| 55 | 55.1 | 5 | 5 | 5 ✓ |

## Verifica aritmetica
Teoria: 11(M7) + 22(M9) + 28(M10) + 7(M11) + 89(M12) + 2(M13) + 15(M50) + 20(M51) + 25(M53) + 40(M54) + 16(M55) = 275 ✓
Pratica: 5(M50) + 10(M51) + 10(M53) + 15(M54) + 5(M55) = 45 ✓ (nessuna pratica sui moduli 7/9/10/11/12/13 in questo courseType)
Task: 5+6+7+10+5 = 33 ✓, id min=291/max=323, zero duplicati.

---
← [[Corsi EASA]] · [[Riferimenti Documentali]]
