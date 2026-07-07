---
tags: [siel]
---
# Derivazione Ore Parte
Le ore attuali di un componente **non sono memorizzate**: si calcolano al volo dalle ore del velivolo.

```
ore_complessive = somma_ore(Ore_totali, Ore_iniziali)
ore_attuali     = somma_ore(
                     sottrai_ore(ore_complessive, ore_vlv_imb),
                     ore_particolare)
```

Cioè: ore del velivolo − ore che il velivolo aveva quando la parte è stata imbarcata (`ore_vlv_imb`) + ore che la parte aveva già al momento dell'imbarco (`ore_particolare`).
Così basta aggiornare `Ore_totali` col volo e tutte le parti "scorrono" da sole.

Nel portable è la query `_SQL_PARTE_DERIVATA` in `db.py` (LEFT JOIN `codice`, JOIN `Elicotteri`), che espone anche il flag `reale` (part_num+ser_num valorizzati).

← [[SIEL]] · [[Registrazione Volo]] → [[cerca_motori]] · [[Tabella codice]] · [[Scadenze LIC LOF]]
