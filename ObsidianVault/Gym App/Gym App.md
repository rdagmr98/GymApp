# Gym App — Hub Principale
Hub per le tre app dell'ecosistema palestra. Leggi questo file all'inizio di ogni sessione gym.

![[Grafi/Gym App]]

---

## App e Repository

| App | Repo | Path locale | Ruolo |
|-----|------|-------------|-------|
| [[Apps/Gym App Trainer]] | `rdagmr98/GymApp` | `C:\Users\Gianmarco` (root) | Trainer/Admin |
| [[Apps/App Coach]] | `rdagmr98/gymapp-coach` | — | Personal Trainer |
| [[Apps/App Cliente]] | `rdagmr98/fix-ads` branch | `C:\Users\Gianmarco\fix-ads` | Cliente finale |

---

## Stack comune
- Flutter + Provider/Riverpod
- Firebase (auth + Firestore)
- AdMob per monetizzazione (app cliente)

---

## Gym App Trainer — `rdagmr98/GymApp`

**Scopo**: gestione atleti, programmi, schede, pagamenti

**Build e Deploy**:
```
flutter build apk --release          # APK >100MB → GitHub Release (non committare)
flutter build web --release           # Web → git push origin main
```

---

## App Coach — `rdagmr98/gymapp-coach`

**Scopo**: interfaccia Personal Trainer — vede i propri clienti, schede, progressi

---

## App Cliente — branch `fix-ads`

**Scopo**: interfaccia cliente — schede, prenotazioni, progressi
**AdMob**: banner in fondo a ogni schermata principale
**Fix in corso**: `fix-ads` branch — crash banner AdMob

---

## [[Shared Data]]
Dati condivisi tra le tre app via Firebase Firestore.

---

## Risorse promo
- Immagine: `C:\Users\Gianmarco\ComfyUI\output\gymapp_user_00001_.png`
- Video promo: bloccato — Higgsfield 0.4 crediti rimasti (richiede piano basic)

---

## STATO SESSIONE
_Aggiornare ad ogni push significativo_
- **GymApp trainer**: produzione
- **App Coach**: sviluppo
- **App Cliente / fix-ads**: fix banner in corso
