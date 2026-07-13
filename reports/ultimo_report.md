# Report: doc-only — banca decisione Cerebras NO-GO (2026-07-13)

## File toccati

- `reports/stato_progetto.md` — aggiornata riga "Ultimo aggiornamento"; aggiunto blocco verbatim Cerebras NO-GO nella sezione Finding/note, prima di "Prossimi passi".
- `reports/roadmap.md` — item `**a) DECISO — Cerebras zai-glm-4.7**` → `~~DECISO~~ -> SCARTATO/NO-GO` con rimando a stato_progetto.md e data 2026-07-13.

## git diff --stat reale

```
reports/roadmap.md        |  8 ++------
reports/stato_progetto.md | 22 +++++++++++++++++++++-
2 files changed, 23 insertions(+), 7 deletions(-)
```

## STOP GATE 1 verificato

Nessun file del motore (gas.py, brains/, modules/, tests/) è stato toccato. Doc-only confermato. Gate revisore non applicabile.

## STOP GATE 2 verificato

Branch `docs/cerebras-no-go`, nessun push su main. PR aperta per merge solo a CI verde.

## Esito

COMPLETATO. La decisione Cerebras NO-GO è ora bankizzata in entrambe le fonti canoniche: stato_progetto.md (dettaglio integrale verbatim) e roadmap.md (voce aggiornata con rimando).
