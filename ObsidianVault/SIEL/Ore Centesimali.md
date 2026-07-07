---
tags: [siel]
---
# Ore Centesimali
Convenzione AVES per le ore di volo: la parte decimale sono **minuti**, non centesimi.
`1.30 = 1h 30min`, `2.45 = 2h 45min`. Mai aritmetica decimale diretta (1.30+0.45 ≠ 1.75).

Funzioni base (VBA Access `funzioni_ore`, replicate nel portable `ore_utils.py` e in SQLite):
- `somma_ore(a, b)` — somma con riporto a 60 minuti
- `sottrai_ore(a, b)` — differenza con prestito
- `format_ore(x)` → `"h:mm"`, ritorna `–` se non numerico

Sono registrate come funzioni SQLite in `get_db()` così le query di derivazione girano identiche all'Access.

← [[SIEL]] → [[Registrazione Volo]] · [[Derivazione Ore Parte]] · [[Scadenze LIC LOF]]
