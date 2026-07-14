# diff_sessione — 2026-07-14 (R-crm-1b Fetta 1)

> Fotografia dell'ultima sessione. La storia completa sta in git.

## File toccati

| File | Δ righe | Cosa è cambiato e perché |
|------|---------|--------------------------|
| `modules/memory/store.py` | +101 | Aggiunto `import json` e nuovo metodo `unisci_contatti_con_snapshot`: merge atomico con snapshot diario nella stessa transazione SQLite (rete di sicurezza R-crm-1b fetta 1) |
| `gas.py` | +112 / -1 | Aggiunto `_print_record` (helper display), `merge_contacts_cmd` (comando CLI umano con preview/conferma/fail-safe), routing `merge-contacts` in `main()`, fix hint `check_dups_cmd` da `_unisci_contatti` a `gas merge-contacts <da> <verso>` |
| `tests/test_unit_kernel.py` | +102 | Aggiunti T58a–T58f: test reali round-trip per il nuovo comando (merge riuscito, conflitto, diario snapshot, chiave inesistente, fail-safe diario degradato, fix hint) |
| `reports/ultimo_report.md` | aggiornato | Report canonico della fetta 1 |
| `reports/handoff.md` | aggiornato | Dossier di fine sessione |
| `reports/diff_sessione.md` | aggiornato | Questo file |

## Commit di sessione

```
04aa45e docs(crm-dup-detect): report fetta 1 — gas merge-contacts + fix hint
9515626 feat(crm-dup-detect): R-crm-1b Fetta 1 — comando CLI gas merge-contacts + fix hint
```
