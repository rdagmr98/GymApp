# AVES — Hub Principale
Hub per tutte e tre le app dell'ecosistema militare AVES. Leggi questo file all'inizio di ogni sessione AVES.

---

## App e Repository

| App | Repo | Dati | Path locale |
|-----|------|------|-------------|
| [[Piloti/AVES Piloti]] | `rdagmr98/piloti` | `rdagmr98/piloti-data` | `C:\Users\Gianmarco\piloti` |
| [[Corsi/Corsi EASA]] | `rdagmr98/corsi` | `rdagmr98/corsi-data` | `C:\Users\Gianmarco\corsi` |
| [[Tecnici/AVES Tecnici]] | `rdagmr98/AVES` | `rdagmr98/aves-data` | `C:\Users\Gianmarco\AVES` |

---

## Pattern architetturale condiviso — [[Shared/GhDbService]]

```dart
// Tutte e tre le app usano questo pattern identico
GhDbService.instance
  .read/write(token: READ_PAT, repo: '...', file: 'data.json')
  // AES-CBC encrypt PII prima di scrivere
  // SHA versioning — 409 conflict → retry 3x
  // Cache in-memoria per letture
```
- Token: `--dart-define=READ_PAT=...`
- Stack: Flutter + go_router + riverpod/provider

---

## AVES Piloti — `rdagmr98/piloti`

**Scopo**: Go/No-Go currency piloti militari AVES

**Logica Go/No-Go** (`_pilotOverallStatus()`):
- Medical fitness scaduta → **NO-GO** 🔴
- Ore semestre precedente < 6h → **NO-GO** 🔴
- Scadenza ≤ 60gg **oppure** ore < 6h → **WARNING** 🟡
- Altrimenti → **GO** 🟢

**File chiave**:
```
lib/screens/admin/admin_dashboard.dart
lib/screens/user/user_dashboard.dart
lib/services/user_service.dart
lib/services/flight_service.dart
lib/services/gh_db_service.dart
```
**DB**: `users.json`, `flights.json`, `capabilities.json`, `reference.json`

---

## Corsi EASA Part-66 — `rdagmr98/corsi`

**Scopo**: Gestione corsi B1/B2, presenze, voti, currency istruttori

**4 Ruoli**: admin, istruttore, allievo, osservatore
**4 Tipi corso**: teorico, pratico, esame, on-the-job

**Build deploy**:
```
flutter build web --release --base-href "/corsi/"
git push origin main   # GitHub Actions deploya automaticamente
```

**File chiave**:
```
lib/services/course_service.dart
lib/services/attendance_service.dart
lib/services/grade_service.dart
lib/services/gh_db_service.dart
lib/screens/schedule/schedule_screen.dart
```
**Corso attivo**: [[Corsi/Corso Attivo 3BTC]]

---

## AVES Tecnici — `rdagmr98/AVES` (app: `aves_currency`)

**Scopo**: Currency manutentori ed equipaggi, gestione PTA, qualifiche Part-66

**Schermate**:
```
screens/auth/          — login
screens/dashboard/     — home
screens/helicopters/   — my_fleet_screen, helicopter_detail_screen
screens/activities/    — my_activities_screen, add_activity_screen, pta_screen
screens/admin/         — gestione utenti
screens/profile/       — profilo
```

**Servizi chiave**:
```
currency_service.dart  — calcola currency
activity_service.dart  — CRUD attività
pta_service.dart       — Part Task Trainer
p66_service.dart       — qualifiche Part-66
```

---

## Flutter — Regole anti-overflow testo (OBBLIGATORIO)

**SEMPRE aggiungere `overflow: TextOverflow.ellipsis` nei seguenti contesti:**

1. `ListTile(title: Text(...))` — il title NON ha ellipsis di default, viene tagliato di netto
2. `Row(children: [..., Text(...)])` — qualsiasi Text in una Row non-Expanded viene tagliato. Usa `Flexible(child: Text(..., overflow: TextOverflow.ellipsis))`
3. `TableCell` / `DataCell` con `Text(...)` — stessa regola, aggiungi overflow
4. `_tCell()` helper o simili: aggiungere `overflow` dentro il Text

**Pattern corretto:**
```dart
// ListTile title
title: Text(u.fullName, overflow: TextOverflow.ellipsis, style: ...)

// Row con testo variabile
Flexible(child: Text(label, overflow: TextOverflow.ellipsis, style: ...))

// TableCell
Padding(..., child: Text(text, overflow: TextOverflow.ellipsis, style: ...))
```

**Cosa NON taglia mai:** `subtitle: Text(...)` su ListTile (è già wrapped); testo in Column a larghezza libera.

---

## Riferimenti documentali
→ [[Shared/Riferimenti Documentali]] — AER.P-66, Controlloistruttori.xlsx, Annesso AMC

---

## STATO SESSIONE
_Aggiornare ad ogni push significativo_
- **Piloti**: produzione, nessun TODO critico
- **Corsi**: produzione, deploy automatico via GitHub Actions. 2026-06-16: ricostruzione lezioni/record BTC3 da Controlloistruttori.xlsx (script `reconstruct_btc3.py`, corsi-data 5fecbfc) + visibilità recuperi per tipo teoria/pratica nelle assenze frequentatore (corsi 47ca62c). Gap 2h modulo 6 colmato: 6.6 teoria 2025-11-07 slot 4-5, Palmieri Biagio. Poi (corsi d1eed86): ore da recuperare visibili a frequentatore e direttore — pratica 100% delle assenze, teoria solo le ore oltre il 10% del modulo (floor(ore/10)); campi `toRecover/toRecoverT/toRecoverP` in `computePerModuleStats`. 2026-06-17: titoli istruttori — campo `qualifications` (licenze categoria+aeromobile dai 'stato di servizio' 2026 ∪ reverse griglie AMC ∪ 4 lauree note) su 22 istruttori, griglie AMC rigenerate additive (661 add, 0 rimozioni) (corsi-data 27e2bc7). 2026-06-17 (s13): toggle **Solo GO/Tutti** in tabella AMC (corsi 13c9d98) + griglie AMC popolate dai **conferimenti ufficiali** (`Conferimenti_Istruttori.xlsx`, +170: 153 teoria/17 pratica, 0 rimozioni, corsi-data d355dbd). `qualifications` NON toccate (conferimento d'insegnamento ≠ licenza categoria+aeromobile). Caveat: codici rule-covered su istruttori senza qualifications verrebbero rimossi se un admin risalva l'istruttore (applyQualifications gira solo su save esplicito). **2026-06-18 (s14) — SUPERA s12 e s13(conferimenti)**: modello autoritativo utente = l'UNICO modo di assegnare moduli è la griglia AMC derivata dai **TITOLI**; i conferimenti (`Conferimenti_Istruttori.xlsx`) NON sono più validi. `qualifications` ricostruite SOLO dai titoli nei doc (licenza categoria+aeromobile, 4 lauree dal testo, corso Sicurezza Volo→`sv`, Istruttore Normativa Aeronautica→`nam`); niente più reverse-griglie né conferimenti. Griglie AMC rigenerate 100% dai titoli via amcRules (aggiunge/RIMUOVE): **+128 / −918** (corsi-data b4b8529). **Modulo 3 solo a chi ha `laurea_elettronica`** (Ardia, Principe, Carrino, Onofri); **Ciula e Mirizzi non insegnano più Modulo 3**. Regola **macchina→sotto-categoria B1** (UC-228/VC-180A→b1.1, elicotteri→b1.3) corregge il refuso B1.1→B1.3 di Balloi. 15 istruttori restano senza qualifiche (doc senza licenze su macchina). Script locale `build_quals_from_titoli.py` NON committato + `.gitignore` per blindare la KEY AES (corsi-data 27ee086). Doc: corsi 2644bb5. **2026-06-20 (s15) — admin CRUD tipi corso**: nuova richiesta utente (creare/modificare tipi corso con moduli+ore T/P+task pratica id/nome/durata, perché alcune durate attuali sono sbagliate). `reference.json` diventa scrivibile (`GhDbService.saveReference`, `ReferenceService.saveCourseTypes/nextTaskId/isCourseTypeInUse`); nuovo campo `PracticalTask.name`; nuova schermata `course_types_tab.dart` (5° tab admin). Nome task — prima scrivibile ma mai mostrato — ora visibile ovunque si referenzia un taskId (calendario direttore, dropdown _addLesson, agenda istruttore, oggi istruttore, agenda frequentatore) via `ReferenceService.taskName()`. Verificato (nessuna modifica necessaria): riepiloghi e controllo istruttori leggono già lezioni/reference.json live a ogni build(), nessuna cache da invalidare. Non testato in browser (nessun tool di controllo browser disponibile in sessione). Doc: corsi f4085af. **2026-06-20 (s16) — fix syllabus ufficiale + discrepanze BTC3**: estratti da PDF syllabus ufficiale (`02 - SYLLABUS_EI_B1_Combinato_(T+P)_Rev.1.pdf`) nomi/ore/ID task e ore teoria sottomoduli reali; corretto `reference.json` b1 (corsi-data b10b2fe) — fix teoria modulo 1 (1.1/1.2/1.3), ricostruiti `practicalTasks` 11A/11B con id/nome/ore corretti, invariante "somma ore task = ore pratica sottomodulo" verificata su tutto b1. Fix bug ricorrente label UI tagliata a metà bordo in `course_types_tab.dart` (corsi 4c05c3a) — vedi [[Shared/Riferimenti Documentali]] e memoria `feedback_flutter_label_cutoff`. **Confronto programma corretto vs Controllo istruttori (BTC3) — CORRETTO**: l'analisi iniziale (righe `3btc` con `Istruttore` nullo escluse, tutto il resto sommato) aveva riportato 3 false discrepanze (mod.3 pratica +3h, mod.8 teoria +9h, mod.9 teoria +4h). L'utente ha contestato il risultato con dati grezzi del registro e chiarito la semantica reale: colonna `Assenze` = frequentatore assente quell'ora (lezione regolare, conta comunque), colonna `Recuperi` = frequentatore per cui quell'ora è un recupero mirato → ora ADDIZIONALE da NON sommare al monte ore base. Metodo corretto: riga conta se Istruttore non nullo, poi split regolari (Recuperi vuoto) vs recupero (Recuperi popolato, separate). **Risultato: zero discrepanze reali** — moduli 1,2,3,4,5,6,8,9,10,16 match esatto col piano; 7,12,15 sotto piano (ancora in corso, normale); 11,17,18 a 0h (non iniziati). I 3 scostamenti iniziali erano interamente ore di recupero (es. modulo 9: 4 ore recupero Lorenzo Codina per assenze in 9.2/9.8) misclassificate come eccesso. Nota: l'assenza di Codina in 9.3 (15/10/2025) non ha ancora una riga di recupero — da verificare. Doc: corsi c08379b + fix successivo.
- **Tecnici**: sviluppo attivo
