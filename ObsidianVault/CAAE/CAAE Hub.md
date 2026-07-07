---
tags: [progetto, web, caae, aves]
---
# CAAE — Centro Addestrativo Aviazione dell'Esercito

Sito web istituzionale del CAAE di Viterbo. Statico, mobile-first, animato (AOS + CSS).

> [!info] Materiale didattico corsi (AER(EP).P-147)
> La generazione del materiale didattico per i corsi dell'MTO CAAE ha una nota dedicata: [[Materiale Didattico]] (engine PDF, regole cardine, mappa syllabus militare, stato).

## Info base
| Campo | Valore |
|-------|--------|
| URL pubblico | https://rdagmr98.github.io/caae/ |
| GitHub repo | `rdagmr98/caae` (privato/pubblico) |
| Path locale | `C:\Users\Gianmarco\caae` |
| Deploy | GitHub Actions → GitHub Pages (push su `main`) |
| Tech | HTML/CSS/JS puro, font Rajdhani+Inter, libreria AOS |

## Struttura pagine
```
index.html          ← homepage: hero stemma, motto, pulsanti Corsi/Flotta
storia.html         ← storia CAAE, timeline, contatore 946K ore di volo
bandiera.html       ← onorificenze e decorazioni
corsi/
  piloti.html       ← corso piloti
  medevac.html      ← corso MEDEVAC
  sere.html         ← corso SERE (Sopravvivenza Evasione Resistenza Evasione)
  specialisti.html  ← corso specialisti
flotta/
  luh196b.html      ← LUH-169B
  luh196d.html      ← LUH-169D
  ab205.html        ← AB-205
  ab206.html        ← AB-206
shared.css          ← stili condivisi tra tutte le pagine
imgs/               ← immagini (elicotteri, corsi, stemma CAAE HD)
generate_qr.py      ← genera QR code del sito
process_imgs.py     ← script preprocessing immagini
```

## Materiale sorgente
- `C:\Users\Gianmarco\Documents\sito\` — materiale originale: HTML salvato da sito S.A.I.O., foto elicotteri (169B/D, 205, 206), PDF ufficiali (Attività Formativa, Storia, Brochure)
- `C:\Users\Gianmarco\Downloads\sito\` — foto WhatsApp maggio 2026 (aggiornamenti recenti)

## Workflow aggiornamento
1. Modifica HTML/CSS/immagini in `C:\Users\Gianmarco\caae`
2. `git add` + `git commit` + `git push origin main`
3. GitHub Actions deploya automaticamente su GitHub Pages

## Stato
- Sito live e funzionante
- Ultima modifica: rimosso stemma dalla nav, foto elicotteri aggiornate da cartella sito + Wikimedia
- Note WhatsApp in `Downloads\sito\` potenzialmente da integrare (maggio 2026, non ancora usate)
