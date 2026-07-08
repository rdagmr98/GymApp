# Gym App — Hub Principale
Hub per le tre app dell'ecosistema palestra. Leggi questo file all'inizio di ogni sessione gym.

![[Grafi/Gym App]]

---

## App e Repository

| App | Repo | Path locale | Ruolo |
|-----|------|-------------|-------|
| [[gym_app]] | `rdagmr98/GymApp` | `C:\Users\Gianmarco` (root) | Trainer/Admin |
| [[app_coach]] | `rdagmr98/gymapp-coach` | — | Personal Trainer |
| [[app_cliente]] | `rdagmr98/gymapplogbook` | `C:\Users\Gianmarco\fix-ads` | Cliente finale |

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
flutter build apk --split-per-abi --release          # APK → Documents\releases\gym_app\
flutter build appbundle --release                    # AAB → Documents\releases\gym_app\
flutter build web --release --base-href "/GymApp/"   # Web → commit build/web/* su root di main
```
> **Deploy reale (verificato 19 giu 2026 via `gh api repos/rdagmr98/GymApp/pages`): Pages source = branch `main`, path `/`.** Niente Action, niente deploy su `gh-pages` per questo repo — si committano direttamente su `main` i file di build (`index.html`, `main.dart.js`, `flutter_bootstrap.js`, `flutter_service_worker.js`, `version.json`, `canvaskit/`, `assets/`, ecc. in root) e si fa push. Pages rebuilda in ~20-30s (verificare con `gh api repos/rdagmr98/GymApp/pages/builds/latest`, deve passare a `"status":"built"`). `index.html` ha `<base href="/GymApp/">` quindi il `--base-href` in build serve.
> Un branch `gh-pages` esiste ancora sul remote (vecchio, orfano) ma **non è la sorgente usata da Pages** — non confonderlo con il deploy reale. Riferimento storico SUPERATO: il worktree `C:\temp\gymapp-gh-pages` descritto in passato in questa nota non è il workflow attuale.

**Releases locali**: `C:\Users\Gianmarco\Documents\releases\gym_app\`
- `gym_app-1.0.2+28-arm64-v8a.apk` / `-armeabi-v7a.apk` / `-x86_64.apk`
- `gym_app-1.0.2+28.aab`

> ⚠️ **REGOLA OBBLIGATORIA — NON SALTARE MAI**: dopo ogni modifica al codice di qualsiasi app gym:
> 1. bump versione in `pubspec.yaml` (+1 build number)
> 2. `flutter build apk --split-per-abi --release` → copia arm64 + armeabi in `Documents\releases\<app>\gym_app-<ver>-*.apk`
> 3. `flutter build appbundle --release` → copia in `Documents\releases\<app>\gym_app-<ver>.aab`
> 4. `gh release create v<ver>` con APK + AAB
> 5. `flutter build web --release --base-href "/<repo>/"` → copia `build/web/*` in root → commit + push main
> **Non chiedere conferma. Non aspettare. Farlo sempre, anche per fix minimi.**

> 🚨 **GAP CRITICO SCOPERTO 07 lug 2026 — la pipeline sopra NON pubblica su Play Store**: gym_app Android si distribuisce ufficialmente via **Google Play Store** (`com.gianmarco.gym_app`, confermato da sito promo + QR utente), firmato con **chiave release vera** (`key.properties`, non debug — verificato in `build.gradle.kts`). La pipeline automatica (Claude) produce solo `gh release` con AAB scaricabile: **nessun fastlane, nessun service account Google Play, nessuna chiamata a Play Developer API esistono in questo repo/macchina**. Questo significa che ogni "release" fatta finora NON raggiunge gli utenti Play Store finché l'AAB non viene caricato manualmente su **Play Console** (console.play.google.com) — passo che va fatto a mano da Gianmarco, Claude non ha credenziali per farlo. Se un fix sembra "non funzionare" su un telefono con l'app da Play Store, verificare PRIMA se l'AAB è stato caricato su Play Console, prima di sospettare il codice. Gap reale e resta valido per ogni futura release — **ma non era la causa del bug S23 sotto**: test con sideload diretto (bypass Play Store) ha riprodotto lo stesso identico bug, escludendo la distribuzione. Vera causa e fix in STATO SESSIONE.
>
> 🚨 **SECONDO GAP COLLEGATO, SCOPERTO 08 lug 2026 — sideload su device con versione Play Store fallisce all'installazione**: upload AAB su Play Console richiede **Play App Signing** → Google ri-firma l'app con una chiave propria, diversa dalla keystore locale (`gymapp-keystore.jks`, fissa, verificata) usata per firmare gli APK che Claude builda. Se sul telefono è già installata la versione Play Store, un APK sideload va in conflitto di firma e Android rifiuta l'installazione ("app non installata", messaggio generico, senza dettagli) — **sempre**, indipendentemente dal fix nel codice. **Prima di ogni test sideload: disinstallare l'app esistente dal telefono.** Questo rimette in dubbio se il "test con sideload diretto" citato sopra (usato per escludere il gap Play Store durante il debug S23) sia mai realmente arrivato a installarsi — possibile causa dei risultati inconsistenti nei round di fix precedenti. Vedi memoria `feedback_apk_signature_mismatch`.

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
**Ultima release**: v1.0.1 — APK ri-caricato 07 lug 2026 con fix floor 64px popup salva serie S23, 4° tentativo (vedi STATO SESSIONE) — firmato debug key originale per aggiornamento diretto
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
_Aggiornare ad ogni push significativo. Solo ultime voci recenti: storico completo nella cronologia git di questa nota + `Sessioni/YYYY-MM-DD.md`._
- **Pulsante "Salva serie" invisibile su S23 — 3° fallimento, causa reale trovata: MediaQuery inset inaffidabile su Samsung One UI, fix floor 64px** (07 lug 2026): dopo il fix strutturale sotto (v1.0.2+27) l'utente ha mandato un TERZO screenshot con lo stesso identico bug. Causa: `MediaQuery.of(ctx).padding.bottom`/`viewPadding.bottom` sottostima l'inset nav bar su questo device anche in edge-to-edge (`WindowCompat.setDecorFitsSystemWindows(window, false)` in `MainActivity.kt:46`). Fix: si prende il massimo tra inset riportato dall'OS e una soglia fissa `64.0`. gym_app `lib/main.dart` commit `214bef5`, app_cliente `fix-ads/lib/main.dart` commit `5050ab4`. Release: gym_app **v1.0.2+28** (APK×3+AAB+web, live e verificato), app_cliente APK ricaricato su release `v1.0.1` esistente. `flutter analyze` pulito su entrambe. **Da verificare**: 4° tentativo complessivo su questo bug (1° MediaQuery dinamico, 2° distribuzione esclusa, 3° ristruttura layout, 4° floor hardcoded) — serve conferma utente su S23 reale. Se fallisce ancora, prossimo step: chiedere una misura reale dell'altezza nav bar (screenshot con "mostra limiti layout" da Developer Options) invece di continuare a indovinare valori.
- **Fix strutturale Row fissa fuori da scroll** (07 lug 2026, v1.0.2+27): Row Annulla/Salva spostata a sibling fisso FUORI dal `SingleChildScrollView`/`Flexible`, sempre a schermo indipendentemente da altezza contenuto/inset/scroll utente. Corretto come struttura ma insufficiente da solo (causa reale era il valore MediaQuery, vedi voce sopra).
- **App Coach**: sviluppo (nessuna modifica recente)
- **versionCode installato**: 3003 (fix-ads) — aggiorna sempre sopra questo
