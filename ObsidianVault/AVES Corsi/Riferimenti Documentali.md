# File di Riferimento — Corsi EASA

Questi file sono la fonte primaria di verità. **Consultarli sempre** quando i dati dell'app sembrano diversi da quelli reali, quando si modificano ore/moduli, o quando si verificano assenze/recuperi.

---

## Programmi Ufficiali AER.P-66

| File | Path | Contenuto |
|------|------|-----------|
| `b1.pdf` | `C:\Users\Gianmarco\Documents\programmi\b1.pdf` | Programma ufficiale B1: M1-M12, M15-M17 + M18 (11B), 2044h totali. Fonte per ore T/P di ogni sottomodulo. |
| `b2.pdf` | `C:\Users\Gianmarco\Documents\programmi\b2.pdf` | Programma ufficiale B2: M1-M10, M13-M14, 1755h. |
| `b1mil.pdf` | `C:\Users\Gianmarco\Documents\programmi\b1mil.pdf` | Moduli militari B1: M50, M51, M53, M54 (138h). Si aggiunge a B1, non lo sostituisce. |
| `b2mil.pdf` | `C:\Users\Gianmarco\Documents\programmi\b2mil.pdf` | Moduli militari B2: M50, M51, M53, M54, M55 (130h). |
| `b1_pages/` | `C:\Users\Gianmarco\Documents\programmi\b1_pages\` | PNG pagina per pagina del b1.pdf (per OCR). |

**Quando consultare**: se le ore di un modulo/sottomodulo sembrano sbagliate in `reference.json`, il programma ufficiale PDF è la fonte. Font trick per OCR: codici in Times New Roman con "3.2" = in realtà "3.1".

---

## Controlloistruttori.xlsx

**Path**: `C:\Users\Gianmarco\Documents\Controlloistruttori.xlsx`

Il file Excel principale del corso. Contiene TUTTO il tracciamento reale.

| Foglio | Contenuto |
|--------|-----------|
| `3btc` | Registrazione lezioni BTC3 (foglio di fonte, colonne per data/ora/modulo/assenti) |
| `assenze 3btc` | Assenze BTC3. R5-R12 = assenze nette OLTRE soglia (0 = OK). R41-R48 = ore unrecovered raw. R14-R22 = snapshot storico 4/6/25. R26-R37 = recuperi registrati. |
| `2btc` | Registrazione lezioni BTC2 |
| `assenze 2btc` | Stessa struttura del 3btc |
| `1btc` | Registrazione lezioni BTC1 |
| `assenze 1btc` | Stessa struttura |
| `currency per modulo` | Ore currency istruttori per modulo |
| `istruttori nell'anno` | Ore insegnamento annuali per istruttore |
| `istruttori nell'anno teoria` | Solo ore di teoria per istruttore |
| `istruttori nell'anno pratica` | Solo ore di pratica per istruttore |
| `currency 2 anni` | Aggiornamento professionale (35h/2 anni) |
| `istruttori` | Anagrafica istruttori |

**Struttura foglio assenze**: la formula in R5-R12 calcola `(assenze_digitali + snapshot) / ore_modulo > 10%`. Se sì: ore eccedenti - C47. C47 = `assenze_digitali_correnti + recuperi_manuali`. Se la cella mostra 0, il frequentatore è nei limiti. Verificare R41-R48 per le ore raw non recuperate.

**Quando consultare**:
- Verifica assenze/recuperi frequentatori → foglio `assenze Xbtc`
- Verifica ore insegnamento istruttori → fogli `istruttori nell'anno`, `currency per modulo`
- Importazione dati in app → fonte primaria per absences e recoveries

---

## ANNESSO MTOE-P-3-1.docx

**Path**: `C:\Users\Gianmarco\Documents\ANNESSO MTOE-P-3-1.docx`

Contiene le griglie AMC (Abilitazioni Materie Corso):
- **Tabella T2**: teoria — 210 coppie (codice sottomodulo → qualifica abilitata)
- **Tabella T3**: pratica — 69 coppie

**Font trick critico**: i codici sottomodulo in font Times New Roman che mostrano "3.2" sono in realtà "3.1" (la codifica usa 2 al posto di 1). Si applica a tutti i pattern `X.2` → `X.1`, incluso `13.2x` → `13.1x` e `53.2` → `53.1`. I codici in Calibri sono letterali.

**28 qualifiche**:
- Laurea (Ing. elettronico/meccanico), B1.1 (Turbina), B1.2 (Pistone), B1.3 (Aliante), B1.4 (Elicottero turbina), B2 (Avionica), Altro

**Verificato**: griglie in `amc.json` (corsi-data) = annesso, zero discrepanze.

**Quando consultare**:
- Modifica qualifiche istruttore → verificare T2/T3 nell'annesso
- Discrepanze su chi può insegnare un sottomodulo → T2 per teoria, T3 per pratica

---

## BTC — Schede e Programmi Settimanali

**Path**: `C:\Users\Gianmarco\Documents\BTC\`

| File | Contenuto |
|------|-----------|
| `00_ProgSettimanale_TOTALE_V3.xlsx` | Programma settimanale completo BTC (pianificazione fisica) |
| `00_ProgSettimanale_TOTALE_V3 - sintesi.xlsx` | Versione sintetica del programma settimanale |
| `Scheda di sintesi B1.xlsx` | Scheda ore B1 per modulo |
| `Scheda di sintesi B2.xlsx` | Scheda ore B2 per modulo |
| `01_PROGRAMMA_BASICO_TB1_TB2_12_luglio_2022.pdf` | Programma basico TB1/TB2 (luglio 2022) |
| `02 - SYLLABUS_EI_B1_Combinato_(T+P)_Rev.1.pdf` | Syllabus B1 combinato T+P |
| `03 - LOGBOOK_EI_B1_Combinato_(T+P)_Rev.1.pdf` | Logbook B1 |

**Quando consultare**: confronto pianificazione app vs pianificazione reale → `ProgSettimanale_TOTALE_V3.xlsx`.

---

## Normativa

| File | Path | Contenuto |
|------|------|-----------|
| `Direttiva_Norme_Svolgimento_Corsi_AVES_Ed._2022.pdf` | `C:\Users\Gianmarco\Documents\corso formatori\` | Regole formali del corso AVES: presenze, recuperi, valutazione |
| `AER_EP_P_66_Em1_Ed_100620191.pdf` | `C:\Users\Gianmarco\Documents\corso formatori\` | Regolamento EASA Part-66 |
| `AEREP.P147_Ed_09042018.pdf` | `C:\Users\Gianmarco\Documents\corso formatori\` | Regolamento AER-EP.P-147 |

---

## Voti 3BTC

**Path**: `C:\Users\Gianmarco\Documents\voti graduatoria 3btc.xlsx`
Graduatoria voti BTC3 — fonte per verifica voti inseriti in app.

---

← [[Corsi EASA]] · [[Corso Attivo 3BTC]] · [[Currency Istruttori]] · [[Tipi Corso]]
