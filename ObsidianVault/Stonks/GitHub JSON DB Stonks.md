# GitHub JSON DB — Stonks

Repo: `rdagmr98/stonks-data`
Pattern: [[GhDbService]] — stesso di AVES/piloti/corsi

## File

| File | Contenuto |
|------|-----------|
| `users.json` | Utenti con password hash SHA-256 e ruolo |
| `portfolio.json` | Posizioni aperte (symbol, shares, avgCost) — ricalcolato automaticamente |
| `transactions.json` | Storia buy/sell/dividend — fonte di verità |
| `watchlist.json` | Simboli in watchlist con target price opzionale |

## Schema portfolio.json
```json
{
  "id": "uuid",
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "type": "stock",        // stock | etf | crypto
  "currency": "USD",
  "shares": 10.5,
  "avg_cost": 150.00,
  "notes": ""
}
```

## Schema transactions.json
```json
{
  "id": "uuid",
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "type": "buy",          // buy | sell | dividend
  "date": "2024-01-15",
  "shares": 5.0,
  "price": 148.50,
  "fees": 1.99,
  "currency": "USD",
  "notes": ""
}
```

## Logica ricalcolo holding
Dopo ogni add/delete transaction, `PortfolioService._recomputeHolding()`:
1. Legge tutte le tx buy/sell per quel symbol
2. Calcola shares totali e costo medio pesato
3. Se shares ≤ 0 → rimuove holding; altrimenti → upsert
