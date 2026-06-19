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
- `gym_app-1.0.2+20-arm64-v8a.apk` / `-armeabi-v7a.apk` / `-x86_64.apk`
- `gym_app-1.0.2+20.aab`

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
  - **Arricchimento visivo** (14 giu): hero con foto palestra di sfondo (`img/hero-bg.jpg`, web) + overlay scuro/ciano; nuova **fascia "Allena ogni muscolo"** = foto web (`img/band-bg.jpg`) + anatomia asset app (`img/muscle.png` dorso) con glow; icona header → app icon HD ufficiale (`img/icon.png` = gymapp-icon-512). Tema/pricing/JS invariati.
  - **Libreria esercizi** (15 giu): nuova sezione `#esercizi` con 8 **gif animate** dell'archivio (`img/ex/*.webp`, da `C:\Users\Gianmarco\assets\gif\`) in card bianche su fondo nero (bench-press, squat, deadlift, lat-pulldown, barbell-shoulder-press, barbell-curl, dip, dumbbell-lateral-raise). Nav aggiornata con voce "Esercizi". Le gif girano da sole (multi-frame webp 360px → usate come tile, non hero).
- **QR utente (DISTRIBUITO a molte persone)**: file `c:\Users\Gianmarco\Downloads\WhatsApp Image 2026-06-14 at 22.55.12.jpeg` → punta a `https://rdagmr98.github.io/gymapplogbook/download.html`
  - `download.html` fa **redirect automatico per piattaforma**: Android → Play Store `com.gianmarco.gym_app`, iOS → Web App `https://rdagmr98.github.io/GymApp/`. Desktop → fallback brandizzato con due pulsanti.
  - **CRITICO — sorgente canonica**: `C:\Users\Gianmarco\fix-ads\web\download.html` (nel repo, non in `C:\temp\`). Flutter copia tutto `web/` in `build/web/` ad ogni build → il file sopravvive ai rebuild. NON cancellare/rinominare. NON usare più `C:\temp\promo-assets\download.html` come sorgente.
  - **Pages type**: `legacy` (serve `gh-pages` diretto). Era "workflow" ma i push di peaceiris con `GITHUB_TOKEN` non innescanevano il CDN → cambiato a legacy. Per forzare deploy manuale: `gh api -X POST repos/rdagmr98/gymapplogbook/pages/builds`.
  - NON cambiare l'URL (il QR è già stampato/distribuito).
  - QR ripulito per stampa: `C:\temp\promo-assets\poster\qr_user.png` (1580x1580, da `magick -colorspace Gray -threshold`, verificato decode cv2)
- **Pricing UFFICIALE**: iPhone = a pagamento (**donazione 1€/mese**, Web App nel browser) · Android = **gratis** (Google Play). Usare ovunque, NON dire "tutto gratis".
- **15 Locandine A4 stampabili** (2480x3508 300dpi, solo QR utente, NESSUN link al sito) su Desktop:
  - Set 1-5 (design puro): `_1_Neon.png` (phone + QR), `_2_QR_Gigante.png` (QR enorme), `_3_Chiara.png` (sfondo bianco ink-friendly), `_4_Funzioni.png` (3 phone showcase), `_5_Motivational.png` ("INIZIA OGGI")
  - Set 6-10 (con asset app + foto web): `_6_Anatomia_asset.png` (SOLO asset: muscle.png petto + strip 5 muscoli), `_7_Brand_asset.png` (SOLO asset: app icon HD gigante + wordmark), `_8_Palestra_mista.png` (foto web deadlift sfondo + QR), `_9_Atleta_mista.png` (foto web sfondo + mockup app), `_10_Collage_mista.png` (foto web sfondo + anatomia dorso)
  - Set 11-15 (con **frame singoli delle gif esercizi**, da `C:\temp\promo-assets\ex\ex_*.png` = frame 0 delle webp animate): `_11_Libreria.png` (griglia 4×2 di 8 esercizi illustrati), `_12_Scheda_PushDay.png` (mimica card app: scheda Push Day con 4 esercizi + serie×reps), `_13_Push_Pull_Legs.png` (3 colonne PUSH/PULL/LEGS), `_14_Tecnica_mista.png` (MISTA: foto palestra `web/gym_dark.jpg` + 2 tile stacco/squat), `_15_TotalBody_mista.png` (MISTA: foto `web/dumbbell.jpg` + strip 4 tile petto/dorso/gambe/braccia)
  - Sorgenti: `C:\temp\promo-assets\ui\loc1..15.html` → render Chrome headless `--force-device-scale-factor=2 --window-size=1240,1754`
  - **Frame esercizi** per le locandine: estratti con `magick "C:/Users/Gianmarco/assets/gif/<nome>.webp[0]" C:/temp/promo-assets/ex/ex_<nome>.png` (frame 0, path Windows obbligatorio)
  - **Asset app** (in `C:\temp\promo-assets\`): `app_icon.png` (= `web/icons/gymapp-icon-512.png`), `muscle_*.png` (da `assets/muscle/*.webp` via magick, path Windows + `[0]`), `screen1..3.png` mockup
  - **Foto web** (Unsplash, in `C:\temp\promo-assets\web\`): `weights.jpg`/`barbell.jpg`/`gym_dark.jpg` (+ altri) — `curl -sL https://images.unsplash.com/photo-{id}?w=1400&q=80`
  - Backup pre-modifica: `C:\temp\promo-backup_20260614_232415\`
  - Vecchia `GymApp_QR.png` (Fase 1) SUPERATA (usava QR self + "100% gratis" sbagliato)
- **Mockup reali** (NON immagini AI): renderizzati da HTML/CSS @3x (1170x2532) — dashboard/workout/progress in `C:\temp\promo-assets\screen1..3.png`, sorgenti `ui/screenN.html` + `ui/ui.css`
- Sorgenti reel: `C:\temp\promo-assets\ui\` (intro/vscene1-3/end.html + scene.css) → PNG 1080x1920
- **Generazione immagini in locale DISPONIBILE**: MCP `comfyui` (ComfyUI locale, port 8188 — avviare se serve) e MCP `higgsfield`. Si possono usare per asset promo se servono immagini generate (finora preferiti mockup/design reali; vecchie immagini AI ComfyUI erano state bocciate dall'utente).

---

## STATO SESSIONE
_Aggiornare ad ogni push significativo_
- **GymApp web — root cause VERO del freeze iPhone trovato e risolto** (19 giu 2026): il fix del wasm stale (18 giu, vedi sotto) NON era la causa reale — l'utente ha confermato che dopo quel deploy il freeze persisteva identico ("ad ogni tocco risponde dopo mezzo minuto", solo su iPhone, mai su Android/Windows, mai su gymapplogbook/fix-ads che non ha questo problema).
  - **Causa reale**: leak di `Timer.periodic` nel countdown cardio (`_cardioCountdownTimer`, esclusivo di gym_app — fix-ads non ha la feature cardio). Veniva cancellato solo a fine countdown naturale o in `dispose()`, ma MAI quando si abbandonava l'esercizio cardio a metà (skip rest, cambio esercizio, fine round, fine workout, uscita anticipata). Ogni cardio abbandonato lasciava un timer orfano attivo nello stesso State, che continuava a fare `setState()` ogni secondo per tutta la sessione. Più cardio abbandonati = più timer accumulati = più `setState`/sec. Su Safari/CanvasKit (più lento di Chrome nel rendering) questo saturava il render thread fino a bloccare ogni tap per decine di secondi.
  - **Fix**: aggiunta `_stopCardioTimer()` (cancella + azzera `_cardioCountdownTimer`), richiamata in tutti i punti dove si esce dal cardio/si cambia esercizio: `_avviaTimerConTempo`, `_skipRest`, `_cambiaEsercizioMethod`, fine round superset, fine esercizio (2 varianti), uscita con conferma (2 varianti), tap manuale stop timer. Commit `89101fb` su `main`.
  - **Release**: `v1.0.2+20` — web ridepl. su `gh-pages` (deploy pulito, verificato `main.dart.wasm` 404 / `main.dart.js` 200), APK arm64/armeabi/x86_64 + AAB → GitHub Release `v1.0.2-20`.
  - **Lezione**: comparare sempre col comportamento di fix-ads quando un bug è "solo su una delle due app" — la feature assente nell'altra app è il primo sospetto, non l'ambiente/deploy.
- ~~**GymApp web — fix wasm stale su gh-pages**~~ (18 giu 2026, **INSUFFICIENTE**, vedi sopra per la causa reale): il deploy di domenica 14 giu (commit `4a5825d`) aveva aggiornato `flutter_bootstrap.js`/`main.dart.js` su `gh-pages` senza pulire la cartella prima — vecchi `main.dart.wasm`/`main.dart.mjs` restavano sepolti lì. Risolto comunque (deploy pulito, regola permanente: ogni deploy DEVE `rm -rf` la cartella gh-pages tranne `.git` prima di copiare `build/web/`, verificare `main.dart.wasm` → 404 post-deploy) ma non era la causa del freeze riportato dall'utente.
- **App Cliente `v1.0.5+3002` + QR fix** (17 giu 2026): portate le stesse fix di gym_app (progressPercent media delta%, sessioni rimossa da streak sharecard). CRITICO: il rebuild aveva cancellato `download.html` da `gh-pages` → QR in 404. Fix: `download.html` spostato in `web/download.html` nella sorgente (commit `b1ca316`), Pages portato a tipo "legacy". Ora sopravvive a ogni rebuild. Creato `fix-ads/CLAUDE.md` con regola permanente. APK aggiornati in releases e su GitHub.
- **GymApp trainer `v1.0.1+19`** (17 giu 2026): chip verde "prova X+2 reps" + chip ambra "↑ AUMENTA PESO" nella schermata ready allenamento (portati da app_cliente). Fix progressPercent sharecard (media delta% per esercizio). Fix numero sessioni streak sharecard rimosso. GitHub Release con APK arm64/armeabi + AAB.
- **Gif esercizi su sito + 5 locandine frame esercizi** (15 giu 2026):
  - **Sito gymappad**: nuova sezione `#esercizi` "Libreria esercizi" con 8 **gif animate** dell'archivio (`img/ex/*.webp`) in card bianche su fondo nero, nav con voce "Esercizi". Commit `50a8fbc`, push su main → Actions deploy.
  - **+5 locandine** (loc11-15) coi **frame singoli** delle gif (frame 0 → `promo-assets/ex/ex_*.png`): `_11_Libreria` (griglia 8), `_12_Scheda_PushDay` (mimica card app), `_13_Push_Pull_Legs` (3 colonne), `_14_Tecnica_mista` + `_15_TotalBody_mista` (foto web + tile esercizi). Totale **15 locandine** su Desktop, loc1-10 invariate. QR utente verificati (cv2 decode → download.html), pricing Android Gratis / iPhone 1€/mese, nessun link al sito.
- **Asset app + foto web su sito e locandine** (14 giu 2026):
  - Backup di sito + locandine in `C:\temp\promo-backup_20260614_232415\`.
  - **+5 locandine** (loc6-10): 2 solo-asset (Anatomia, Brand) + 3 miste foto web/asset (Palestra, Atleta, Collage). Totale **10 locandine** su Desktop, tutte con QR utente, nessun link al sito, QR verificati (cv2 decode → download.html).
  - **Sito gymappad arricchito**: hero con foto palestra di sfondo + fascia "Allena ogni muscolo" (foto web + anatomia asset) + icona header HD. Commit `4f745c9`, push su main → Actions deploy.
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
