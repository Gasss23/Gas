# Diff sessione — 2026-07-19 (DOC: chiusura flag #1 R-hook-jq + debito Codespace)

> Fotografia della sessione corrente. Si riscrive a ogni sessione; la storia completa sta in git.

## File toccati

```
 reports/stato_progetto.md | 13 ++++++++-----
 1 file changed, 8 insertions(+), 5 deletions(-)
```

## Dettaglio per file

- **`reports/stato_progetto.md`** — 4 edit doc-only su branch `docs/stato-merge-pr25`:
  - (2a) Header "Ultimo aggiornamento": aggiunto "R-hook-jq CHIUSO, flag #1 per ispezione" per riflettere il completamento verificato via CI.
  - (2b) Riga hook suite: aggiunta conferma "confermato da CI run 29664233791 su main" per ancorare il verde locale a un artefatto CI reale.
  - (2c) Voce R-hook-jq CHIUSO: sostituita con blocco completo (Flag #1 CHIUSO per ispezione exit-status-based + merito coperto da CI reale + Flag #2 micro-finding di processo revisore degenere).
  - (2d) Voce "ℹ️ Debito Codespace": convertita in "✅ Debito Codespace CHIUSO — Codespace deprecato" a documentare la cancellazione dell'ambiente da parte dell'operatore.

## Task non in scope (STOP gate rispettato)

Nessun file fuori `reports/` toccato. CLAUDE.md, roadmap.md, ci.yml, motore: invariati.
