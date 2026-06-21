# AVES Piloti
Flutter app **web** HUD militare dark-theme (GitHub Pages `/piloti/`). Repo: `rdagmr98/piloti` · dati: `rdagmr98/piloti-data`.
→ [[Admin Dashboard]] → [[Go No-Go Logic]] → [[Pilot Services]] → [[GitHub JSON DB AVES]]
Pattern condiviso: [[GhDbService]]

## Sicurezza (allineata a corsi, 2026-06-14)
- **Token**: proxy opzionale via Cloudflare Worker (`proxy/worker.js`) — `PROXY_URL` dart-define tiene il token lato server. Senza proxy: Bearer `READ_PAT` diretto (attuale).
- **Password**: PBKDF2-HMAC-SHA256 + salt per-utente (`pbkdf2$iter$salt$hash`), retrocompatibile con SHA-256 legacy, migrazione trasparente al login.
- **PII**: AES-CBC con IV casuale per record (`ENC1:iv:ct`), legacy `ENC:` in sola lettura.
- **Robustezza**: `saveError` ValueNotifier + SnackBar globale su salvataggio fallito.
- Tutto retrocompatibile: dati e credenziali esistenti continuano a funzionare.

![[Grafi/AVES Piloti e Corsi]]
