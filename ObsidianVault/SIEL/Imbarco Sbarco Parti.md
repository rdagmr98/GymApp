---
tags: [siel]
---
# Imbarco / Sbarco Parti
**Imbarco** = montare un componente su un velivolo: si crea una riga in `parti` con `sigla`, codice `(id, tipo_vlv)` da [[Tabella codice]], `part_num`, `ser_num`, `ore_vlv_imb` (ore velivolo al montaggio), `ore_particolare` (ore già fatte dalla parte), `data_imbarco`, `scad_lof`/`scad_lic`.
Da lì le ore della parte scorrono per [[Derivazione Ore Parte]] e maturano le [[Scadenze LIC LOF]].

**Sbarco** = smontaggio: nel gestionale si stampa il verbale con le ore allo sbarco; la parte poi si rimuove/sostituisce.

Maschere/report Access coperti nel portable ([[Maschere e Report Access]]):
- data entry imbarco = modale "Aggiungi parte" / pagina Parti;
- **Verbale imbarco** e **Verbale sbarco** = `/report/imbarco/<contatore>`, `/report/sbarco/<contatore>`;
- **Elenco parti velivolo** (ex *stampa parti II*) = `/report/parti/<sigla>`.

← [[SIEL]] · [[Scadenze LIC LOF]] → [[Tabella codice]] · [[Maschere e Report Access]]
