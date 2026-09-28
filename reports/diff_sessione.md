# Diff sessione 2026-09-28 — Fetta 3a + 3a-bis (lezioni quarantena + fix pre-merge)

## File toccati

| File | Variazione |
|------|-----------|
| `modules/memory/store.py` | +120 righe: tabella `lezioni`, metodi lezioni, rifiuto \n/\r |
| `gas.py` | +231 righe: `_lezioni_pin()`, `lezioni_cmd()`, write_file esteso, lista testo completo+autore, R-lez-3 guard |
| `tests/test_unit_kernel.py` | +201 righe: T68a-T68n (Fetta 3a) + T68o-T68s (Fetta 3a-bis) |
| `reports/ultimo_report.md` | Riscritto: report Fetta 3a-bis |
| `reports/stato_progetto.md` | Aggiornato: review #107, suite 366 |
| `reports/handoff.md` | Aggiornato: dossier completo 3a+3a-bis |

## Cosa è cambiato e perché

- **Fetta 3a** (commit `0c816a9`): catalogo lezioni persistente, CLI umana, iniezione `<lezioni_dati>` nel system prompt.
- **Fix grammaticale R-lez-1** (commit `715af86`): "sono dati" → "è dati".
- **Fetta 3a-bis** (commit `427fcf0`): 4 fix pre-merge — lista testo completo+autore, rifiuto \n/\r, R-lez-3 chiusa, write_file esteso a file memoria kernel.

## Numeri chiave

- Commit fetta 3a-bis: `427fcf0`
- PR: #101 (aperta, non ancora mergiata)
- Suite: **366 PASS, 5 FAIL** (F-mac-1 invariati)
- Nuovi test: 20/20 PASS (T68a-T68n + T68o-T68s)
- Revisori: #106 + #107 — entrambi APPROVATO CON RISERVE
