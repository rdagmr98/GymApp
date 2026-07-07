---
tags: [siel]
---
# Scadenze LIC LOF
Scopo principale del gestionale: sapere quando un componente va in **revisione/sostituzione**.
- **LIC** = limite a calendario (giorni). **LOF** = limite a ore di volo.

Formule (query `Xscadenze per report situazione giorn`, replicate in `get_scadenze_situazione`):
```
gg_disp  = (ultimo_lic + scad_lic) − oggi          # giorni alla LIC
ore_disp = scad_lof − (ore_attuali − ultimo_lof)   # ore alla LOF
```
`ore_attuali` deriva da [[Derivazione Ore Parte]].

Una parte compare nel report scadenze se: `gg_disp < 60` **∨** `ore_disp < 25` **∨** `applicabilita = True`.
Nel report: righe **rosse** = scaduta (valore < 0), **gialle** = vicina.

← [[SIEL]] · [[Registrazione Volo]] → [[cerca_motori]] · [[Imbarco Sbarco Parti]] · [[Logica Motori e Scadenze]]
