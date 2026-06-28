# Diff sessione — 2026-06-28 (fix R-comp-1)

> Si riscrive a ogni sessione. La storia completa sta in git.

## Commit della sessione

```
cde4d94 fix(kernel): R-comp-1 — boundary al confine piegato nel summary (review #40)
```

## File toccati

```
gas.py                    | 37 ++++++++++++------------
tests/test_unit_kernel.py | 71 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
2 files changed, 91 insertions(+), 17 deletions(-)
```

## Cosa è cambiato e perché

### gas.py — `_compress_history_if_needed`

**Prima**: i messaggi di `recent` che precedevano il primo `user` venivano scartati
silenziosamente (drop R-comp-1). La logica trovava `start` = primo user in `recent`,
poi faceva `recent = recent[start:]`, perdendo `recent[:start]`.

**Dopo**: estratto `boundary = recent[:start]`; calcolato `to_compress = old + boundary`;
il loop di compressione ora itera `to_compress` (non più solo `old`). L'header del
riepilogo riflette il conteggio aggiornato. Zero drop silenzioso.

Aggiornati anche: docstring (rimosso "scartati … accettabile"), `logging.info`
(ora mostra `old + boundary → riepilogo` invece di `scartati al confine`).

### tests/test_unit_kernel.py — T53 e T54

**T53**: verifica il fix. Costruisce una history con 3 messaggi assistant (con marcatore
stringa) prima del primo user nella finestra `recent`. Asserisce che il marcatore compaia
nel summary (non droppato) e che l'header conti correttamente `old+boundary`.

**T54**: promuove il caso degenere (history di soli assistant, nessun user). Asserisce
che dopo la compressione `history[0]["role"]=="user"` e la window parta da user.

## Sessione precedente

`9d32e3e` docs report FASE 2.5 (2026-06-27) — la riserva R-comp-1 di review #39 era
stata lasciata aperta come non bloccante e chiusa in questa sessione.
