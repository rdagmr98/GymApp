---
tags: [siel]
---
# Registrazione Volo
Inserimento di una riga in `sit_giornaliera` (data, ore_giorno, cicli, posizione, nota, codice).
Quando si registra il volo, l'app aggiorna l'elicottero e **tutte** le sue parti:
- `Elicotteri.Ore_totali += ore_giorno`
- `Elicotteri.Ore_DUR += ore_giorno` **solo se** `ore_dur_appl` della parte
- `parti.cicli_tot += cicli` su ogni parte della sigla

Mai si toccano le ore dei particolari: le ore parte sono **derivate**, vedi [[Derivazione Ore Parte]].

**Modifica volo** = applica il DELTA (nuovo − vecchio). **Cancella** = applica l'inverso.
Round-trip insert→modifica→delete riporta tutto **esatto** (self-test PASS) → i conti del volo sono corretti; i problemi "sui motori" erano di sola visualizzazione ([[Logica Motori e Scadenze]]).

← [[SIEL]] · [[Ore Centesimali]] → [[Derivazione Ore Parte]] · [[Scadenze LIC LOF]]
