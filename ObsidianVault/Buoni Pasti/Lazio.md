# Buoni Pasto / Indennità Regione Lazio

Elaborazione indennità Regione Lazio con metodologia "Sangiovanni" (template Excel con formule per blocco anno).

## Lavoratore
- **COLETTI AMBRA** — unica lavoratrice trovata nella cartella `E:\REGIONE LAZIO\` (cedolini NoiPA-style)
- Codice fiscale CLTMBR91P50H501G, domicilio fiscale ROMA
- Categoria C1 Enti Locali, qualifica RRC1
- Ufficio: Agenzia Regionale di Protezione Civile — Amm.ne appartenenza: REGIONE LAZIO
- Nota: nel file di riferimento `Copia di annistampa.xlsx` appare invece BOLLITO VINCENZO (Polizia Locale Roma Capitale) — usato SOLO come esempio di metodologia/pattern indennità, non come dato reale (confermato dall'utente: "per i nuovi in regione lazio le indennità sono le stesse della polizia locale" → stesse 7 categorie concettuali, testo diverso)

## Fonti dati
- `E:\REGIONE LAZIO\cedolini 2020\` … `cedolini 2026\` — PDF NoiPA-style, 2 pagine (anagrafica+riepilogo / dettaglio competenze), 86 PDF totali
- Alcuni mesi hanno 2-3 cedolini distinti (NON duplicati — verificato MD5+netto: sono cedolino base + integrativo/conguaglio, importi diversi, entrambi sommati)
- Formato riga indennità: `<CODICE> <DESCRIZIONE>[-Qta.X-Imp.Y-Rif.MM/YYYY] <IMPORTO>` — il suffisso `-Rif.MM/YYYY` (o `-scad.MM/YYYY`) indica la VERA competenza se diversa dal mese del cedolino (offset variabile, non fisso come Sangiovanni — letto riga per riga)

## Mapping indennità → colonne modello
| Colonna | Significato | Codice/pattern Coletti | Esito |
|---|---|---|---|
| B | Ind. Di turno diurno | `AA06/E1GM` | dati reali |
| C | Ind rep turno | pattern PL (`REPERIB`, `REP.FEST`) | sempre 0 (non presente per Coletti) |
| D | IND turno fest/nott | `AA06/E1GP` | dati reali |
| E | IND Turno nott o Fest. | `AA06/E1GN`, `AA06/E1HN` | dati reali |
| F | ind di rischio HH | `AA06/E1GS` (CONDIZIONILAVORO_2) | dati reali, escluso da Sommatoria/Totale (come da modello) |
| G | Ind pronta disponibilità | pattern PL (`Dis.PL`, `ServizioEstPL`) | sempre 0 |
| H | IND servizio esterno | pattern PL (`ServizioEsternoPL`) | sempre 0 |

Esclusi deliberatamente: maggiorazioni orarie/notturne/festive (`AA06/E1C5..CA`), produttività (`AA02/E2HK/PC/SD/TK`), indennità di responsabilità/comparto (`393/*`, `712/713 CBS`), ritenute sindacali (`800/SFK`) — non sono le 7 categorie indennità tracciate.

## Script
- `C:\Users\Gianmarco\Documents\REGIONE LAZIO\analizza_lazio.py` — estrae da tutti i PDF, classifica per codice/pattern, rispetta l'override Rif./scad. per mese di competenza, genera l'Excel

## Struttura Excel generata (replica esatta del modello)
- Header dati personali: Nome/Cognome/Luogo lavoro (riga 1-2), Ferie fruite annue=28, Giorni lavorati=`(365-28)` (riga 3-4)
- Blocchi anno regolari da 16 righe (header+12 mesi+Somme annuali+Medie annue+1 vuota), uno per ogni anno con dati: **2019** (solo arretrati nov/dic via Rif.), 2020-2025 completi, **2026** parziale (gen-mag)
- Riga mese, colonna I: `=SUM(B:C:D:E:G:H)` (F sempre esclusa, come nel modello originale)
- Somme annuali: `=SUM(elenco celle mese)` per ognuna delle 7 colonne B,C,D,E,G,H,I
- Medie annue: `=(Somme/337*28)` — divisore fisso 337 giorni lavorati/anno (diverso da Sangiovanni che usa `/H{n}*22.5` variabile)
- Tabella riassuntiva K/L accanto al primo blocco: Anno/Importo per ogni anno (`=I{riga_medie_annue}`) + riga Totale (`=SUBTOTAL(109,...)`)

## Risultato finale (2026-06-20)
- Output: `COLETTI_AMBRA.xlsx`
- 86 PDF elaborati, 8 anni con dati (2019 parziale, 2020-2025 completi, 2026 parziale)
- Totali annuali (no colonna F) tra ~550 e ~3470 €/anno secondo l'anno
- Commit + push eseguito su main

## STATO SESSIONE
_Aggiornare dopo ogni elaborazione_
- 2026-06-20: Lazio completato. Worker reale identificato (Coletti Ambra, non Bollito). Mapping indennità derivato dai codici reali nei PDF. Script scritto, eseguito, verificato (controllo di sanità sui totali annuali), committato e pushato. File temp di debug cancellati (confermato dall'utente).
