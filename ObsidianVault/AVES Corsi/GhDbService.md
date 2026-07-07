# GhDbService — Pattern Condiviso
SHA versioning · AES-CBC encryption PII · 3-attempt conflict retry
REST API GitHub · `READ_PAT` via `--dart-define`

## Due strategie di scrittura (progetto `corsi`)
- **Sincrona** (`_writeFile`): `saveAmc`/`saveReference` — attende davvero la PUT su GitHub prima di risolvere, imposta `saveError` e rilancia in caso di fallimento.
- **Coda ottimistica** (`_enqueueWrite`/`_drain`/`_putLatest`): cache aggiornata subito in memoria, la PUT reale parte in background con coalescing per file (salvataggi rapidi consecutivi → 1-2 PUT reali) + retry/backoff (`_putToGitHub`, fino a 6 tentativi, gestisce 409/403/429/5xx). Usata per i file ad alta frequenza: `schedules`, `records`, `grades`, `updates`, `notes`, `notifications`.

## Bug 2026-07-03: courses.json/users.json non persistevano prima del reload
`saveUsers`/`saveCourses` erano finite (in una sessione precedente non documentata) sulla coda ottimistica invece che sincrone, rompendo l'invariante storica "users/courses/reference/amc restano sincroni" (vedi sessione 11). Essendo a bassa frequenza (impostazioni corso, registrazione), il `Future` del chiamante si risolveva quasi subito, prima che la vera PUT arrivasse — un reload pagina poco dopo "Salva" richiamava `init()` (che svuota `_cache` e ricarica da GitHub) prima che la scrittura in background fosse arrivata, mostrando dati vecchi per un po'.

Sintomo riportato dall'utente: cancellando/aggiungendo un giorno tra i "giorni esclusi dalla pianificazione" (`schedule_tab.dart` → `_showExcludedDates()`) e premendo Salva, le modifiche non si vedevano nemmeno ricaricando la pagina, comparivano solo dopo molto tempo.

**Fix** (`gh_db_service.dart`, commit `1a714ee`): aggiunto `_awaitWrite(fileName)` — attende il `_drain` in corso per quel file e rilancia l'errore se la scrittura è ancora in `_pending` dopo il drain (stesso pattern di `flushPending()`, ma per un singolo file). Chiamato subito dopo `_enqueueWrite()` in `saveUsers` e `saveCourses`, ripristinando il contratto "risolve solo quando davvero persistito o fallito per sempre". Nessun caller esistente rotto (tutti già facevano `await`). Copre transitivamente ogni scrittura corsi/utenti: creazione/modifica/eliminazione corso, attivazione, completamento, giorni esclusi, creazione/modifica/eliminazione utente, auto-registrazione frequentatore da login.

Usato da: [[Pilot Services]] · [[Schedule]] · [[Currency Istruttori]] · [[Currency Tecnici]] · [[GitHub JSON DB Corsi]]
Condiviso tra: [[AVES Piloti]] · [[AVES Tecnici]] · [[Corsi EASA]]
