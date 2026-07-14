# diff_sessione — 2026-07-14 (R-crm-1b Fette 2+3)

> Fotografia dell'ultima sessione. La storia completa sta in git.

## File toccati

| File | Delta |
|------|-------|
| `modules/memory/store.py` | +141 righe — `normalizza_telefono`, `_is_phone`, `_append_sospetto`, modifica `rileva_duplicati_email`, nuovo `rileva_duplicati_telefono` |
| `gas.py` | +13 righe nette — `check_dups_cmd` aggiornato per email + telefono |
| `modules/memory/__init__.py` | +2 righe — esporta `normalizza_telefono` |
| `tests/test_unit_kernel.py` | +122 righe — T59 (3 test idempotenza) + T60 (6 test telefono) |

## Perché

**Fetta 2 (idempotenza):** `rileva_duplicati_email` ri-appendeva gli stessi sospetti ad ogni run. Con lo scheduler FASE 4.5 h24, il diario si sarebbe gonfiato di ripetizioni. Soluzione: helper `_append_sospetto` con tag `[ids:X,Y]` + check LIKE prima di scrivere.

**Fetta 3 (telefono):** il CRM rileva duplicati solo per email. Aggiunto trigger telefono: `normalizza_telefono` (pura, idempotente, gestisce forme +39/0039/locale), `rileva_duplicati_telefono` (speculare a email), integrazione in `check_dups_cmd`.

## Review revisore

Review #49 — APPROVATO CON RISERVE per entrambe le fette. Riserve applicate prima del commit.
