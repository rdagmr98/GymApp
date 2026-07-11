---
tags: [caae, materiale-didattico, programmi, ground-truth]
---
# Programmi Ufficiali — Argomenti per Sottomodulo

> Nota di **ground truth per contenuti**: da qui si prendono moduli, sottomoduli e argomenti da trattare per scrivere il [[CAAE/Materiale Didattico]]. Fonte: PDF ufficiali dei programmi in `C:\Users\Gianmarco\Documents\programmi\`, mai `reference.json` (database dell'app "corsi", progetto separato, con gap noti — vedi sotto) e mai analogia/assunzione generica.

## Perché questa nota esiste

Il 2026-07-10 è stato generato un sottomodulo **"1.4 Statistica"** per il corso TB2 (Modulo 1, Mathematics) senza alcuna fonte reale — dedotto per assunzione generica invece che dal programma ufficiale. L'utente (Training Manager, co-redattore ufficiale dei programmi) lo ha scoperto e corretto duramente:

> *"ma poi 1.4 dove cazzo l'hai trovato per i b2?? attieniti ai programmi che ti ho dato! da lì devi prendere i moduli, sottomoduli e argomenti da trattare!"*

Il sottomodulo è stato rimosso interamente (PDF, `CONTENT`/`IT_NAMES`/`TOPICS`/`LEVELS` in `build.py`, contenuto in `mod01.py`, figure). Questa nota cataloga, direttamente dal dump del PDF ufficiale, gli argomenti reali per sottomodulo — così un errore dello stesso tipo si vede a colpo d'occhio prima di scrivere contenuto nuovo. Regola gemella in memoria persistente Claude: `feedback_program_ground_truth`.

**Per le tabelle ore/livello arithmetically-verified complete di tutti i moduli** (non solo 1-3) vedi [[AVES Corsi/Programma B2]] — quella nota resta la fonte per l'integrità dati dell'app "corsi" (reference.json). Questa nota **non duplica** quelle tabelle: aggiunge il livello di dettaglio "argomenti da trattare" per sottomodulo che serve a scrivere i contenuti didattici, non a validare reference.json.

## Fonte

`C:\Users\Gianmarco\Documents\programmi\dump_m1_m6.txt` — dump testuale (PyMuPDF) del programma ufficiale **TB2: Manutentore Tecnico Avionico** (corso b2), Moduli 1-6, pagine 14-34. Copre per ora Moduli 1-3 in dettaglio in questa nota (i moduli 4-6 sono già nel dump, da trascrivere qui quando si arriva a scrivere quel contenuto). Scope da estendere man mano (altri corsi: b1, b1mil, b2mil, maml, b2-da-b1.3 hanno dump/PDF propri — vedi [[AVES Corsi/Riferimenti Documentali]]).

---

## MODULO 1 — MATHEMATICS (TOTALE 70h teoria / 0h pratica)

| Sottomodulo | Livello | Teoria | Argomenti da trattare |
|---|---|---|---|
| 1.1 Arithmetic | 2 | 14h | Termini e segni aritmetici, metodi di moltiplicazione e divisione, frazioni e decimali, fattori e multipli, pesi/misure/fattori di conversione, rapporti e proporzioni, medie e percentuali, aree e volumi, quadrati, cubi, radici quadrate e cubiche |
| 1.2(a) Algebra | 2 | 14h | Valutazione di espressioni algebriche semplici, addizione/sottrazione/moltiplicazione/divisione, uso delle parentesi, frazioni algebriche semplici |
| 1.2(b) Algebra | 1 | 7h | Equazioni lineari e loro soluzioni; indici e potenze (anche negativi/frazionari); sistemi di numerazione binario e altri; sistemi di equazioni simultanee ed equazioni di secondo grado a un'incognita; logaritmi |
| 1.3(a) Geometry | 1 | 7h | Costruzioni geometriche semplici |
| 1.3(b) Geometry | 2 | 14h | Rappresentazione grafica; natura e utilizzo dei grafici, grafici di equazioni/funzioni |
| 1.3(c) Geometry | 2 | 14h | Trigonometria semplice: relazioni trigonometriche, uso delle tavole, coordinate rettangolari e polari |

**Nessuna "1.4"** — il programma ufficiale si ferma a 1.3(c). Somma di verifica: 14+14+7+7+14+14 = 70 = TOTALE dichiarato. Nessun gap, sicuro procedere. Stato Materiale Didattico: **1.1/1.2/1.3 completati e verificati** (TB1+TB2, 6 PDF).

---

## MODULO 2 — PHYSICS (corso-dipendente: TB1 90h / TB2 80h teoria, 0h pratica)

**Divergenza reale fra corsi (non un errore di dati)**: TB1 (Manutentore Tecnico Meccanico) e TB2 (Manutentore Tecnico Avionico) hanno programmi ufficiali diversi per il Modulo 2, verificato su fonte primaria per entrambi. Concordano su 7 sottomoduli (2.1, 2.2.3(b), 2.2.4(a), 2.3(a), 2.3(b), 2.4, 2.5, stessi livelli/ore). Divergono sui restanti 4, tutti dentro l'ombrello 2.2 Mechanics: TB1 li richiede a **livello 2/10h ciascuno** (Statics, Kinetics, Dynamics-Mass, Fluid dynamics-viscosità), TB2 solo a **livello 1** con ore ridotte (8h/8h/6h/8h). Per il Materiale Didattico si applica il pattern già usato per 53.x/54.1: un solo `content_2_X` per codice reference.json, scritto alla profondità massima richiesta da uno dei due corsi (quindi 2.2 va scritto a livello 2 ovunque), copertina che mostra livello/ore del corso specifico.

### TB2 — Manutentore Tecnico Avionico (TOTALE 80h teoria / 0h pratica)

Fonte: `dump_m1_m6.txt` (confermato 100% TB2-specifico: 21× "TB2", 0× "TB1"/"Meccanic", header pag. 14 "TB2: Manutentore Tecnico Avionico").

| Sottomodulo | Livello | Teoria | Argomenti da trattare |
|---|---|---|---|
| 2.1 Matter | 1 | 3h | Natura della materia: elementi chimici, struttura di atomi e molecole; composti chimici; stati solido/liquido/gassoso; cambiamenti di stato |
| 2.2.1 Mechanics — Statics | 1 | 8h | Forze, momenti e coppie (rappresentazione vettoriale); baricentro; sforzo/deformazione/elasticità: trazione, compressione, taglio, torsione; natura e proprietà di solidi/fluidi/gas; pressione e galleggiamento nei liquidi (barometri) |
| 2.2.2 Mechanics — Kinetics | 1 | 8h | Moto rettilineo uniforme, moto uniformemente accelerato (caduta dei gravi); moto rotatorio (forze centrifughe/centripete); moto periodico (pendolo); vibrazioni, armoniche e risonanza; rapporto di velocità, vantaggio meccanico, efficienza |
| 2.2.3(a) Mechanics — Dynamics (Mass) | 1 | 6h | Forza, inerzia, lavoro, potenza, energia (potenziale/cinetica/totale), calore, efficienza |
| 2.2.3(b) Mechanics — Dynamics | 2 | 10h | Quantità di moto e sua conservazione; impulso; principi giroscopici; attrito (natura, effetti, coefficiente, resistenza al rotolamento) |
| 2.2.4(a) Mechanics — Fluid dynamics | 2 | 10h | Peso specifico e densità |
| 2.2.4(b) Mechanics — Fluid dynamics | 1 | 8h | Viscosità, resistenza dei fluidi, effetti aerodinamici (streamlining); comprimibilità dei fluidi; pressione statica/dinamica/totale: teorema di Bernoulli, effetto Venturi |
| 2.3(a) Thermodynamics | 2 | 3h | Temperatura: termometri e scale Celsius/Fahrenheit/Kelvin; definizione di calore |
| 2.3(b) Thermodynamics | 2 | 7h | Capacità termica, calore specifico; trasmissione del calore (convezione/irraggiamento/conduzione); dilatazione volumetrica; 1° e 2° principio della termodinamica; leggi dei gas ideali, calore specifico a V e P costante, lavoro di espansione; trasformazioni isoterme/adiabatiche, cicli motore, refrigeratori e pompe di calore; calori latenti di fusione/evaporazione, calore di combustione |
| 2.4 Optics (Light) | 2 | 7h | Natura e velocità della luce; leggi di riflessione e rifrazione (superfici piane, specchi sferici, lenti); fibre ottiche |
| 2.5 Wave Motion and Sound | 2 | 10h | Moto ondulatorio: onde meccaniche, onde sinusoidali, interferenza, onde stazionarie; suono: velocità, produzione, intensità, tono, timbro, effetto Doppler |

Somma di verifica: 3+8+8+6+10+10+8+3+7+7+10 = 80 = TOTALE dichiarato.

### TB1 — Manutentore Tecnico Meccanico (TOTALE 90h teoria / 0h pratica)

Fonte: `b1.pdf` pagg. 18-20/86 (footer "TB1 Manutentore Tecnico Meccanico | Stato: Approvato | Numero Edizione: 01.00 | Data Edizione: 05/2022"). **b1.pdf è un PDF scansionato** (0 caratteri estraibili via PyMuPDF su tutte le 80 pagine) — nessun dump testuale possibile, lettura diretta delle immagini rasterizzate `Documents\programmi\b1_pages\page_12.png`/`page_13.png`/`page_14.png` (già preparate).

| Sottomodulo | Livello | Teoria | Argomenti da trattare |
|---|---|---|---|
| 2.1 Matter | 1 | 3h | (identico a TB2) |
| 2.2.1 Mechanics — Statics | **2** | **10h** | (stessi argomenti di TB2, richiesti a livello superiore) |
| 2.2.2 Mechanics — Kinetics | **2** | **10h** | (stessi argomenti di TB2, richiesti a livello superiore) |
| 2.2.3(a) Mechanics — Dynamics (Mass) | **2** | **10h** | (stessi argomenti di TB2, richiesti a livello superiore) |
| 2.2.3(b) Mechanics — Dynamics | 2 | 10h | (identico a TB2) |
| 2.2.4(a) Mechanics — Fluid dynamics | 2 | 10h | (identico a TB2) |
| 2.2.4(b) Mechanics — Fluid dynamics | **2** | **10h** | (stessi argomenti di TB2, richiesti a livello superiore) |
| 2.3(a) Thermodynamics | 2 | 3h | (identico a TB2) |
| 2.3(b) Thermodynamics | 2 | 7h | (identico a TB2) |
| 2.4 Optics (Light) | 2 | 7h | (identico a TB2) |
| 2.5 Wave Motion and Sound | 2 | 10h | (identico a TB2) |

Somma di verifica: 3+10+10+10+10+10+10+3+7+7+10 = 90 = TOTALE dichiarato.

### Nota su reference.json (Modulo 2)

reference.json (app "corsi") per **TB1** riporta 90h totali con lo stesso bucketing per codice della tabella sopra (2.1=3h, 2.2=60h, 2.3=10h, 2.4=7h, 2.5=10h) — **esatto, verificato riga per riga contro b1.pdf**. Per **TB2** riporta invece 2.1=10h, 2.2=20h, 2.3=15h, 2.4=10h, 2.5=25h: il totale (80h) combacia con la somma verificata **per coincidenza**, ma il bucketing per singolo codice è sbagliato (vero: 2.1=3h, 2.2=50h, 2.3=10h, 2.4=7h, 2.5=10h). Da correggere in copertina via override mirato in `build.py` (stesso pattern di `LEVELS`/`TOPICS`), non in reference.json (fuori scope, progetto separato).

Stato Materiale Didattico (aggiornato 2026-07-11): **2.1 Matter e 2.2 Mechanics scritti e verificati a livello di struttura/sorgente** (2.2 al livello 2 più alto richiesto, come da pattern sopra) — build PDF + QA visivo ancora da fare (task #54). **2.3/2.4/2.5 non ancora iniziati.** Vedi [[CAAE/Materiale Didattico]] sezione "Fase 3 — Modulo 2".

---

## MODULO 3 — ELECTRICAL FUNDAMENTALS (TOTALE 90h teoria / 20h* pratica aggregata)

| Sottomodulo | Livello | Teoria | Argomenti da trattare |
|---|---|---|---|
| 3.1 Electron Theory | 1 | 2h | Struttura e distribuzione delle cariche elettriche in atomi/molecole/ioni/composti; struttura molecolare di conduttori, semiconduttori, isolanti |
| 3.2 Static Electricity and Conduction | 2 | 5h | Elettricità statica e distribuzione delle cariche elettrostatiche; leggi di attrazione/repulsione; unità di carica, legge di Coulomb; conduzione in solidi/liquidi/gas/vuoto |
| 3.3 Electrical Terminology | 2 | 5h | Differenza di potenziale, f.e.m., tensione, corrente, resistenza, conduttanza, carica, verso convenzionale della corrente, flusso di elettroni |
| 3.4 Generation of Electricity | 1 | 2h | Produzione di elettricità: luce, calore, attrito, pressione, azione chimica, magnetismo, moto |
| 3.5 DC Sources of Electricity | 2 | 5h | Celle primarie/secondarie, piombo-acido, Ni-Cd, Li-ion, alcaline; celle in serie/parallelo; resistenza interna; termocoppie; fotocellule |
| 3.6 DC Circuits | 2 | 5h | Legge di Ohm, leggi di Kirchhoff (tensioni/correnti); calcoli di resistenza/tensione/corrente; resistenza interna di un alimentatore |
| 3.7(a) Resistance/Resistor | 2 | 5h | Resistenza e fattori influenti; resistenza specifica; codice colori, valori/tolleranze, potenza nominale; resistori in serie/parallelo/misti; potenziometri, reostati, ponte di Wheatstone |
| 3.7(b) Resistance/Resistor | 1 | 2h | Coefficiente di temperatura positivo/negativo; resistori fissi (stabilità/tolleranza/limiti) e variabili, termistori, resistori tensione-dipendenti; costruzione di potenziometri/reostati/ponte di Wheatstone |
| 3.8 Power | 2 | 5h | Potenza, lavoro, energia (cinetica/potenziale); dissipazione su resistore; formula della potenza; calcoli |
| 3.9 Capacitance/Capacitor | 2 | 5h | Funzionamento del condensatore; fattori che influenzano la capacità (area/distanza/n. armature/dielettrico/tensione); tipi costruttivi, codice colori; calcoli serie/parallelo; carica/scarica esponenziale, costanti di tempo; collaudo |
| 3.10(a) Magnetism | 2 | 5h | Teoria del magnetismo; proprietà del magnete; ago in campo magnetico terrestre; magnetizzazione/smagnetizzazione; schermatura; tipi di materiali; elettromagneti; regole della mano |
| 3.10(b) Magnetism | 2 | 5h | Forza magnetomotrice, intensità di campo, densità di flusso, permeabilità, ciclo di isteresi, ritentività, forza coercitiva, riluttanza, saturazione, correnti parassite; cura/conservazione magneti |
| 3.11 Inductance/Inductor | 2 | 5h | Legge di Faraday; induzione in conduttore in moto; fattori su tensione indotta (campo/flusso/spire); induzione mutua; legge di Lenz e polarità; f.e.m. autoindotta; saturazione; usi degli induttori |
| 3.12 DC Motor/Generator Theory | 2 | 5h | Teoria base motori/generatori DC; costruzione generatore DC; fattori su uscita/direzione corrente; fattori su potenza/coppia/velocità/rotazione dei motori DC; motori serie/shunt/composti; starter-generator |
| **3.13 AC Theory** | 2 | 5h | Forma d'onda sinusoidale: fase, periodo, frequenza, ciclo; valori istantaneo/medio/RMS/picco/picco-picco e calcoli su tensione/corrente/potenza; onde triangolari/quadre; principi mono/trifase |
| **3.14 R/C/L Circuits** | 2 | 5h | Relazione di fase tensione-corrente in circuiti L/C/R (serie/parallelo/misti); dissipazione di potenza; impedenza, angolo di fase, fattore di potenza; potenza vera/apparente/reattiva |
| **3.15 Transformers** | 2 | 5h | Costruzione e funzionamento dei trasformatori; perdite; comportamento a carico/a vuoto; trasferimento di potenza, efficienza, polarità; calcoli tensioni/correnti di linea/fase; potenza trifase; rapporto spire; autotrasformatori |
| **3.16 Filters** | 1 | 2h | Funzionamento, applicazione e uso di filtri passa-basso, passa-alto, passa-banda, elimina-banda |
| **3.17 AC Generators** | 2 | 6h | Rotazione di spira in campo magnetico e forma d'onda prodotta; generatori AC ad armatura rotante e a campo rotante; alternatori mono/bi/trifase; collegamenti trifase stella/triangolo; generatori a magneti permanenti |
| **3.18 AC Motors** | 2 | 6h | Costruzione, funzionamento e caratteristiche di motori AC sincroni e a induzione (mono/polifase); controllo velocità e direzione; campo rotante: condensatore, induttore, poli schermati/sdoppiati |

`*` 20h di pratica sono aggregate sull'intero modulo (non ripartite per sottomodulo), svolte secondo l'"Aircraft Maintenance Engineer's Basic Practical Logbook".

### Gap in reference.json — RISOLTO, 3.13-3.18 sono contenuto ufficiale

Somma 3.1-3.12 (quello che `reference.json` copre) = 2+5+5+2+5+5+5+2+5+5+5+5+5+5 = **61h**.
Somma 3.13-3.18 (**evidenziati in grassetto sopra**, assenti da reference.json) = 5+5+5+2+6+6 = **29h**.
Totale 61+29 = 90h = TOTALE dichiarato dal programma → somma verificata, **29h è la cifra corretta** (non 31h, cross-verificato anche in [[AVES Corsi/Programma B2]] dal 2026-06-22/23).

**Decisione presa (2026-07-11)**: il syllabus combinato `C:\Users\Gianmarco\Documents\BTC\btc\02 - SYLLABUS_EI_B1_Combinato_(T+P)_Rev.1 (2).pdf` conferma 3.13-3.18 come contenuto ufficiale reale (90h teoria + 20h* pratica sul Modulo 3 completo) — non un'invenzione priva di fonte. Il gap è solo di `reference.json` (database dell'app "corsi"), non del programma. **Si scrive il Modulo 3 per intero, 3.1-3.18**, nessuna decisione ulteriore da chiedere. `Documents\BTC\btc\` è una fonte di ground-truth aggiuntiva, alla pari del dump in `Documents\programmi\`, da consultare per i corsi/moduli dove serve incrociare i due PDF.

---

## Moduli successivi

Non ancora trascritti in dettaglio qui (dump disponibile in `dump_m1_m6.txt` per moduli 4-6; altri moduli in `dump_m13_m7.txt`, `dump_m8_m14.txt`, `dump_9_10.txt`, `dump_ridotto_full.txt`, `btc_vfi_dump.txt` — vedi [[AVES Corsi/Riferimenti Documentali]] per l'elenco completo). Aggiungere la tabella argomenti qui man mano che si scrive quel contenuto nel Materiale Didattico, **sempre dal dump/PDF ufficiale del corso specifico**, mai da reference.json.
