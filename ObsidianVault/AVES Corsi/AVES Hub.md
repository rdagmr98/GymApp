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

## Riferimenti documentali
→ [[Shared/Riferimenti Documentali]] — AER.P-66, Controlloistruttori.xlsx, Annesso AMC

---

## STATO SESSIONE
_Aggiornare ad ogni push significativo_
- **Piloti**: produzione, nessun TODO critico
- **Corsi**: produzione, deploy automatico via GitHub Actions
- **Tecnici**: sviluppo attivo
