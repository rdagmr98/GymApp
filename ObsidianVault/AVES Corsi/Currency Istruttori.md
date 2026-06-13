# Currency Istruttori

## Regole GO/NO GO
- ≥ 6h insegnamento/anno (rolling 365 giorni)
- ≥ 35h aggiornamento professionale/2 anni
- DAA non scaduta
- Override manuale possibile (`goOverride = true`)

## Calcolo in app
- `getTeachingHoursRollingYear(userId)` = lezioni confermate + registrazioni manuali
- `getProfessionalUpdateHoursLast2Years(userId)` = da updates.json
- Currency da lezioni: solo `confirmed = true`, `time_slot > 0`, ultimi 365gg

## Qualifiche AMC
Ogni istruttore ha `qualifications: List<String>` (codici qualifica).
Le griglie AMC in `amc.json` mappano sottomodulo → qualifiche abilitate.
→ [[Riferimenti Documentali]] per l'Annesso MTOE-P-3-1.docx (fonte T2/T3)

## Verifica currency reale
→ `C:\Users\Gianmarco\Documents\Controlloistruttori.xlsx`
- Foglio `istruttori nell'anno` — ore insegnamento per istruttore
- Foglio `istruttori nell'anno teoria` / `pratica` — split T/P
- Foglio `currency per modulo` — ore per modulo
- Foglio `currency 2 anni` — aggiornamento professionale

← [[4 Ruoli]] → [[GitHub JSON DB Corsi]] · [[Riferimenti Documentali]]
