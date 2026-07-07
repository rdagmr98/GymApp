---
tags: [siel]
---
# cerca_motori
Query Access che alimenta la colonna Motori del report Situazione. Logica esatta:
`SELECT … FROM (parti INNER JOIN codice ON parti.id=codice.id AND parti.tipo_vlv=codice.tipo_vlv) INNER JOIN tab_eli_query … WHERE id=1 OR id=2`.

Punti chiave:
- filtra **solo** `id = 1` o `id = 2` (le posizioni motore), **non** per part_num/ser_num;
- richiede l'**INNER JOIN con [[Tabella codice|codice]]** → la parte deve avere un codice;
- ore motore = `somma_ore(sottrai_ore(ore_complessive, ore_vlv_imb), ore_particolare)` ([[Derivazione Ore Parte]]).

Trappola del **Motore 2 fantasma**: per l'AB206 (monomotore, tv3) la riga `codice (id=2)` esiste ma con `Parte = NULL` → l'Access letterale mostra un motore 2 a ~ore cellula. Il portable lo sopprime con `Parte IS NOT NULL`.
Dettaglio completo e bugfix: [[Logica Motori e Scadenze]].

← [[SIEL]] · [[Derivazione Ore Parte]] → [[Tabella codice]] · [[Parco Elicotteri]] · [[Logica Motori e Scadenze]]
