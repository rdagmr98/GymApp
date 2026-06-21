# Calcolo Buoni Pasto
Regola Tivoli: giorno lavorato ≥ 6h15m (375 min) → buono maturato. Valore: 4.13€ = 0.5h (`BUONO_EURO`/`BUONO_ORE`, analisi_tivoli.py:32-33).
Nel codice **non esistono** funzioni separate `calcola_ore()`/`calcola_buoni_pasto()` (nomi storici concettuali) — il conteggio `maturati` è inline in ognuno dei 4 parser ([[parse_new_format]] · [[parse_old_rev]] e gli altri 2 in [[detect_format]]); la conversione in €/h avviene dopo, via formule Excel in `create_worker_excel()`/`create_cumulative_excel()`.
Erogati già forniti estratti da PDF con regex `Buoni\s+Pasto\s+Salvo\s+Conguaglio\s+(\d+)`. Delta = maturati - erogati.
Altre sedi hanno soglie diverse — vedi [[Verona]] (385 min), [[Rieti]] (380 min), [[Padova]] (no soglia fissa).
← [[parse_new_format]] · [[parse_old_rev]]
→ [[Excel Worker]] · [[Cartellini PDF]] · [[RIEPILOGO XLSX]]
