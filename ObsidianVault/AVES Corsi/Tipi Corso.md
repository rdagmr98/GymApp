# Tipi Corso
Verificato da `corsi-data/db/reference.json`:
- B1mil: 138h (teoria 98 + pratica 40, 4 moduli) — verificato e corretto, dettaglio: [[Programma B1]]
- B2mil: 130h (teoria 90 + pratica 40, 5 moduli) — verificato e corretto, task pratici completi, dettaglio: [[Programma B2]]
- B1: 2074h (teoria 1680 + pratica 394, moduli 1-12 + 15-18, 16 tot.)
- B2: 1755h (teoria 1440 + pratica 315, moduli 1-10 + 13-14, 12 tot.)
- **B2-da-B1.3** (5° tipo corso, aggiunto sessione 20/2026-06-22, ex `deltaCourses`): 441h (teoria 378 + pratica 63, moduli 4,5,7,13,14,51,53,55, 8 tot.) — delta per chi ha già B1.3+estensione mil (M50/51/53/54) e deve arrivare a B2. Standalone come b1/b2 (non un'estensione come b1mil/b2mil). Dettaglio: [[Programma B2]].

`totalHours` è derivato a runtime dai moduli in reference.json, non hardcoded — questi numeri possono cambiare a ogni correzione syllabus (vedi STATO SESSIONE in [[AVES Hub]]).

## Bug 2026-07-04: task id progressivo globale invece di ripartire da 1 per tipo
Segnalato dall'utente: "l'id dei task è giusto solo per il tb1... i programmi addestrativi sono diversi". Causa: `PracticalTask.id` è una sequenza unica su tutto reference.json (b1: 1-112, b2_da_b1_3: 113-153, b1mil: 154-178, b2mil: 179-206, b2: 207-290, maml: 291-323) invece di ripartire da 1 per tipo come nei programmi ufficiali. `id` non è stato rinumerato (usato internamente da schedule/lookup, dati produzione b1mil/maml lo referenziano) — aggiunto invece `programTaskId` (= `id - min(id del tipo) + 1`, esatto perché ogni tipo ha id contigui) mostrato in UI ovunque, editabile nell'editor admin ([[course_types_tab]]). Dettaglio completo in `corsi/CLAUDE.md` sessione 25.
← [[4 Ruoli]] → [[Schedule]]
