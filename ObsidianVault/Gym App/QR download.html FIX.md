---
title: QR download.html — Fix & Regola
data: 2026-06-17
tags: [gym, qr, github-pages, deploy, fix]
---

# 📲 QR GymApp — `download.html` (regola permanente)

> [!important] Regola d'oro
> Il QR dato a **migliaia di persone** punta a
> **`https://rdagmr98.github.io/gymapplogbook/download.html`**.
> Questo file **non deve mai dare 404**. L'URL è immutabile (contiene il nome repo `gymapplogbook`):
> non si può rinominare la repo senza rifare il QR.

## Com'è fatto
`download.html` è una landing che reindirizza in base al dispositivo:
- **Android** → Google Play (`com.gianmarco.gym_app`)
- **iPhone/iPad** → Web App `https://rdagmr98.github.io/GymApp/`
- **Desktop** → mostra i due pulsanti

## Architettura deploy (repo `rdagmr98/gymapplogbook`)
- Branch **`main`** = sorgente Flutter + workflow `.github/workflows/web-deploy.yml`.
- Push su `main` → `flutter build web --base-href "/gymapplogbook/"` → deploy `build/web` su **`gh-pages`** → live.
- Ogni deploy **rigenera `gh-pages` da zero**.

## ✅ Fix applicato (2026-06-17)
- **Causa:** il rebuild dell'app (commit `ef2490a`, v1.0.5+3002) ha rigenerato `gh-pages`
  e cancellato `download.html`, che era stato aggiunto **a mano solo su `gh-pages`** (non in sorgente).
- **Soluzione definitiva:** spostato `download.html` in **`gymapplogbook/web/download.html`** (commit `11737d9`).
  Ora Flutter lo include in ogni build → il QR non si rompe più.

## ⚠️ Da ricordare per il futuro
- I file statici extra del sito (come `download.html`) vanno SEMPRE in `web/`, **mai** aggiunti a mano su `gh-pages`.
- Dopo ogni deploy, verifica: apri `https://rdagmr98.github.io/gymapplogbook/download.html` → deve dare 200.
- GitHub Pages della repo è ora su build type **`legacy`** (prima "workflow"): col tipo "workflow" i push di
  peaceiris fatti con `GITHUB_TOKEN` non pubblicavano sul CDN e i deploy restavano bloccati. Con `legacy` si
  pubblica in automatico a ogni push su `gh-pages`. Forzatura manuale: `gh api -X POST repos/rdagmr98/gymapplogbook/pages/builds`.

Vedi anche: nota di lavoro originale in `Downloads/GymApp-QR-FIX/` (file `download.html` + `LEGGIMI-FIX-QR.md`).
