# Stonks — Portfolio Tracker

Flutter app — Clone di getquin per tracciare azioni, ETF e crypto.
Repo app: `rdagmr98/stonks` | Repo dati: `rdagmr98/stonks-data`
Stack: go_router · flutter_riverpod · Yahoo Finance API

## Architettura
- **Backend**: GitHub JSON (`stonks-data`) — stesso pattern [[GhDbService]] degli altri progetti
- **Prezzi live**: Yahoo Finance API v8, cache 5 min
- **Auth**: SHA-256 password hash + SharedPreferences auto-login
- **Tema**: dark GitHub-inspired (kBg/kCard/kGreen/kRed)

## Funzionalità
→ [[Portfolio Holdings]] — posizioni con P&L e variazione giornaliera
→ [[Transazioni Stonks]] — buy/sell/dividend con ricalcolo automatico holding
→ [[Watchlist Stonks]] — lista simboli con target price e alert
→ [[GitHub JSON DB Stonks]] — struttura dati e file JSON

## Schermate (4 tab)
| Tab | Funzione |
|-----|----------|
| Home (Dashboard) | Valore totale, P&L oggi/totale, pie allocazione |
| Portfolio | Lista holdings ordinata per valore |
| Transazioni | Storia completa, swipe-to-delete |
| Watchlist | Prezzi live + target price |

## TODO
- [ ] Schermata dettaglio holding con grafico storico
- [ ] Dividend tracker dedicato
- [ ] Import CSV transazioni
- [ ] GitHub Actions per build APK automatica
