# Watchlist

Modello: `lib/models/watchlist_item.dart`
Screen: `lib/screens/watchlist/watchlist_screen.dart`

## Funzionalità
- Aggiungi simbolo con nome e target price opzionale
- Prezzo live da Yahoo Finance (cache 5 min)
- Variazione % giornaliera colorata (green/red)
- Icona flag verde quando prezzo ≥ target
- Swipe left per rimuovere

## Bottom sheet aggiunta
Campi: simbolo, nome, target price
Salva in `watchlist.json` via `PortfolioService.addToWatchlist()`
