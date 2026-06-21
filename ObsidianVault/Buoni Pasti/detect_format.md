# detect_format()
Riconosce formato PDF da marcatori testuali — 4 varianti, non solo 2 (analisi_tivoli.py:208):
- `OLD` — "AZIENDA USL RMG" + "Cartellino contratto"
- `NEW` — "Cartellino Orario" → [[parse_new_format]]
- `CART` — "STAMPA CARTELLINO" (parser non ancora documentato in nota propria)
- `OLD_REV` — testo RTL invertito → [[parse_old_rev]]
← [[Pipeline]]
→ [[parse_new_format]] · [[parse_old_rev]]
