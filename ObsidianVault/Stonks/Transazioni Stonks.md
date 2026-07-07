# Transazioni

Modello: `lib/models/transaction.dart` → `StTransaction`
Screen: `lib/screens/transactions/`

## Tipi
| Tipo | Icona | Colore | Effetto holding |
|------|-------|--------|-----------------|
| buy | arrow_down | kGreen | Aumenta shares + ricalcola avgCost |
| sell | arrow_up | kRed | Riduce shares, libera quota costo |
| dividend | payments | kYellow | Non tocca holding (solo record) |

## Flusso aggiunta
1. Form `AddTransactionScreen`: symbol, nome, qty, prezzo, fee, data, valuta, note
2. `PortfolioService.addTransaction()` → write `transactions.json`
3. `_recomputeHolding()` → ricalcola e aggiorna `portfolio.json`
4. Invalidate providers Riverpod → UI si aggiorna

## Flusso eliminazione
Swipe left su tile → confirm dialog → `deleteTransaction()` → `_recomputeHolding()`
