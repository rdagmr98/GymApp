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
flutter build apk --split-per-abi --release   # APK → Documents\releases\gym_app\
flutter build appbundle --release             # AAB → Documents\releases\gym_app\
flutter build web --release                   # Web → branch gh-pages (NO base-href)
```
> Web deploy: worktree su `C:\temp\gymapp-gh-pages` (NON in home, sarebbe dentro il repo)
**Releases locali**: `C:\Users\Gianmarco\Documents\releases\gym_app\`
- `GymApp-arm64-v8a.apk` (148 MB)
- `GymApp-armeabi-v7a.apk` (146 MB)
- `GymApp.aab` (174 MB)

> **REGOLA**: dopo ogni modifica a qualsiasi app → rebuild APK → copia in `Documents\releases\<app>\` → GitHub Release

---

## App Coach — `rdagmr98/gymapp-coach`

**Scopo**: interfaccia Personal Trainer — vede i propri clienti, schede, progressi

---

## App Cliente — branch `fix-ads`

**Scopo**: interfaccia cliente — schede, prenotazioni, progressi
**AdMob**: banner in fondo a ogni schermata principale
**Releases locali**: `C:\Users\Gianmarco\Documents\releases\app_cliente\`
- `GymLogbook-arm64-v8a.apk` (154 MB)
- `GymLogbook-armeabi-v7a.apk` (151 MB)
> Asset gif/muscle: copiare da `gym_app\assets\` (.webp, NON .gif)

**Build** (OBBLIGATORIO dopo ogni modifica — sempre con --split-per-abi):
```
cd C:\Users\Gianmarco\fix-ads
flutter build apk --split-per-abi --release
# copia arm64 e armeabi in Documents\releases\app_cliente\
# poi gh release upload v<tag> ... --clobber
```

> **"App non installata" come aggiornamento** = 2 cause possibili:
> 1. **versionCode in discesa** (più comune): `pubspec.yaml version: X.Y.Z+BUILD` — BUILD deve essere > di quello installato. Controllare con `aapt dump badging <apk>`.
> 2. **Firma diversa**: usare `signingConfigs.getByName("debug")` in `build.gradle.kts` (debug key di questa macchina = debug.keystore apr 2022).
> Versione corrente installata: `1.0.5+2006`
> Google Pixel / telefoni moderni → `GymLogbook-arm64-v8a.apk`
> Telefoni vecchi → `GymLogbook-armeabi-v7a.apk`

**Release**: https://github.com/rdagmr98/rdagmr98.github.io/releases
**Ultima release**: v1.0.1 — fix streak mezzanotte + asset .webp da gym_app (154MB) — firmato debug key originale per aggiornamento diretto
**Asset**: gif e muscle presi da `gym_app\assets\` come .webp (non .gif) — stessa sorgente di gym_app

---

## [[Shared Data]]
Dati condivisi tra le tre app via Firebase Firestore.

---

## Risorse promo
- **Sito vetrina + reel**: repo `rdagmr98/gymappad` → live https://rdagmr98.github.io/gymappad/
  - Build/sorgente locale: `C:\temp\gymappad-site\` (index.html single-page + promo.mp4 + img/)
  - Deploy: GitHub Actions Pages (`.github/workflows/pages.yml`), auto su push a `main`
  - **Tema brand** (= tema app): nero puro + ciano `#00F2FF` con glow, font Inter
  - **CTA corrette**: iPhone → Web App `https://rdagmr98.github.io/GymApp/` · Android → Play Store `com.gianmarco.gym_app` (NON più app cliente)
  - **Reel `promo.mp4`**: verticale 9:16 **1080x1920**, 16.2s, ffmpeg (Ken Burns zoompan + xfade), 5 scene brandizzate, muto (audio da aggiungere in TikTok/IG)
  - **Download facile**: sezione `#scarica` con due card (iPhone Web App 1€/mese · Android Google Play gratis), QR self-referente RIMOSSO, pulsanti hero con platform-detection JS
- **QR utente (DISTRIBUITO a molte persone)**: file `c:\Users\Gianmarco\Downloads\WhatsApp Image 2026-06-14 at 22.55.12.jpeg` → punta a `https://rdagmr98.github.io/gymapplogbook/download.html`
  - `download.html` (repo `rdagmr98/gymapplogbook`, deploy LEGACY branch `gh-pages` root) fa **redirect automatico per piattaforma**: Android → Play Store `com.gianmarco.gym_app`, iOS → Web App `https://rdagmr98.github.io/GymApp/`. Desktop → fallback brandizzato con due pulsanti. Sorgente: `C:\temp\promo-assets\download.html`. NON cambiare l'URL (il QR è già stampato/distribuito).
  - QR ripulito per stampa: `C:\temp\promo-assets\poster\qr_user.png` (1580x1580, da `magick -colorspace Gray -threshold`, verificato decode cv2)
- **Pricing UFFICIALE**: iPhone = a pagamento (**donazione 1€/mese**, Web App nel browser) · Android = **gratis** (Google Play). Usare ovunque, NON dire "tutto gratis".
- **5 Locandine A4 stampabili** (2480x3508 300dpi, solo QR utente, NESSUN link al sito) su Desktop:
  - `GymApp_Locandina_1_Neon.png` (phone + QR, nero/ciano), `_2_QR_Gigante.png` (QR enorme centrato), `_3_Chiara.png` (sfondo bianco, ink-friendly), `_4_Funzioni.png` (3 phone showcase), `_5_Motivational.png` ("INIZIA OGGI")
  - Sorgenti: `C:\temp\promo-assets\ui\loc1..5.html` → render Chrome headless `--force-device-scale-factor=2 --window-size=1240,1754`
  - Vecchia `GymApp_QR.png` (Fase 1) SUPERATA (usava QR self + "100% gratis" sbagliato)
- **Mockup reali** (NON immagini AI): renderizzati da HTML/CSS @3x (1170x2532) — dashboard/workout/progress in `C:\temp\promo-assets\screen1..3.png`, sorgenti `ui/screenN.html` + `ui/ui.css`
- Sorgenti reel: `C:\temp\promo-assets\ui\` (intro/vscene1-3/end.html + scene.css) → PNG 1080x1920
- **Generazione immagini in locale DISPONIBILE**: MCP `comfyui` (ComfyUI locale, port 8188 — avviare se serve) e MCP `higgsfield`. Si possono usare per asset promo se servono immagini generate (finora preferiti mockup/design reali; vecchie immagini AI ComfyUI erano state bocciate dall'utente).

---

## STATO SESSIONE
_Aggiornare ad ogni push significativo_
- **Promo QR + 5 locandine + download** (14 giu 2026):
  - Creato `download.html` su `gymapplogbook` (gh-pages) = target del QR già distribuito: **redirect automatico** Android→Play Store / iOS→Web App, desktop fallback. Verificato live 200.
  - Sito gymappad: rimosso QR self-referente, sezione download rifatta con 2 card (pricing corretto iPhone 1€/mese · Android gratis), platform-detection sui pulsanti hero. Pushed.
  - **5 locandine A4** diverse su Desktop (`GymApp_Locandina_1..5_*.png`), tutte con SOLO il QR utente, nessun link al sito, pricing corretto.
  - Generazione immagini locale (ComfyUI/Higgsfield MCP) annotata come disponibile.
- **Promo redesign** (14 giu 2026): rifatto sito gymappad nel tema app (nero + ciano `#00F2FF`), immagini AI sostituite con mockup reali, link corretti (iPhone→Web App GymApp, Android→Play Store), nuovo reel verticale 1080x1920 16.2s. Deploy Actions OK, live verificato (asset 200, link confermati).
- **Promo + cleanup** (14 giu 2026): sito vetrina + video promo deployati su `rdagmr98/gymappad` → https://rdagmr98.github.io/gymappad/ · git gc su home repo: `.git` 8.1GB→150MB (erano 7.64GB di loose objects, nessuna riscrittura storia, main==origin/main)
- **GymApp trainer** `v1.0.1+18`: badge zoom 1.18x, streak alarm Pixel fix (canScheduleExactAlarms), timer chip 22px/20-10, chip peso/reps 17px, streak notifica IMPORTANCE_HIGH tutti device, niente emoji nel titolo
- **App Coach**: sviluppo (nessuna modifica recente)
- **App Cliente** `v1.0.4+5` (fix-ads): stesse fix di trainer + base-href `/gymapplogbook/` per web, emoji 💪 rimossa da streak notification
- **Web**: GymApp → gh-pages (`C:\temp\gymapp-gh-pages`), AppCliente → gh-pages (`/tmp/gymapplogbook-gh-pages`)
- **Pixel fix streak**: `canScheduleExactAlarms()` applicato sia a scheduleTimerFinishedNotification che scheduleStreakReminderNotification in entrambe le app (il repeat giornaliero usa setAndAllowWhileIdle RTC_WAKEUP — non mostra come sveglia in Clock)
- **versionCode installato**: 3001 (fix-ads) — aggiorna sempre sopra questo
