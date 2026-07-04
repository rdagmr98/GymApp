# Schedule
`generateRemainingSchedule()` — 6 slot Lun-Gio, 3 slot Ven. 27h/settimana.
Recupero assenze >10%.
← [[Tipi Corso]] → [[GitHub JSON DB Corsi]]
Usa: [[GhDbService]]

## Bug 2026-07-04: modifiche visibili solo cambiando tab (`schedule_tab.dart`, commit `647b640`)
Seguito del bug [[GhDbService]] del 2026-07-03 (persistenza): risolta la latenza di scrittura, restava un problema di **refresh UI**. `_load()` ricaricava `_courses` ma riassegnava `_selected` solo se `_selected == null` — dopo un salvataggio (giorni esclusi, corso, utenti) la UI continuava a leggere il vecchio oggetto `Course` in memoria, anche se il dato su GitHub era già aggiornato. Cambiare tab ricrea lo `State` Flutter (`initState` → `_selected = null`) e forza il repick, da cui l'illusione "serve navigare via e tornare per vedere le modifiche".
**Fix**: `_load()` ora risincronizza sempre `_selected` cercandolo per id dentro `_courses` appena ricaricato, non solo quando è null. Punto unico condiviso da tutte le chiamate post-salvataggio del file.
