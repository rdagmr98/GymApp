# Portfolio Holdings

Schermata portfolio + dashboard tile.
Modello: `lib/models/holding.dart`
Service: `lib/services/portfolio_service.dart`

## Dati visualizzati per ogni holding
- Simbolo + nome
- Numero quote
- Prezzo medio di carico (pm)
- Valore attuale (quote live Yahoo Finance)
- P&L totale (€ e %)
- Variazione giornaliera (%)

## Tipo asset → colore badge
| Tipo | Colore |
|------|--------|
| stock | kBlue |
| etf | kYellow |
| crypto | #F7931A (bitcoin orange) |

## Ordinamento
Portfolio screen: ordinato per valore attuale decrescente.
Dashboard: stessa lista (prime N).
