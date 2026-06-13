# AVES — Hub Principale
Tre app dello stesso ecosistema militare. Stessa architettura [[GhDbService]].

## App
- [[AVES Piloti]] — Go/No-Go currency piloti, `rdagmr98/piloti`
- [[Corsi EASA]] — Corsi Part-66 B1/B2, `rdagmr98/corsi`
- [[AVES Tecnici]] — Currency manutentori/equipaggi, `rdagmr98/AVES`

## Pattern condiviso
- [[GhDbService]] — GitHub REST API, AES-CBC PII, retry 3x su 409, SHA versioning
- DB dati separati: `rdagmr98/piloti-data`, `rdagmr98/corsi-data`, `rdagmr98/aves-data`
- Flutter + go_router + riverpod/provider
