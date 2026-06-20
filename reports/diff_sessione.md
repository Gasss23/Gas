# DIFF DI SESSIONE — 2026-06-20 (backup off-machine + doctor rumoroso, review #26/#27)

> Fotografia dell'ULTIMA sessione (la storia completa sta in git). Riscritta a ogni sessione.

## Tema

Sessione continuata da un contesto precedente (compresso). Due TASK dal prompt originale:

- **TASK A** (review #26): backup off-machine del DB memoria su dir esterna configurabile.
- **TASK B** (review #27): doctor — fallimento silenzioso della memoria reso rumoroso + vector store visibility.

## File toccati (commit `56a6dc3`)

- **`modules/memory/store.py`** (+32, solo aggiunte): metodo `backup_offsite_auto()`.
- **`gas.py`** (+130, -11): costanti OFFSITE, `__init__` env vars, `_memoria_backup_auto()` esteso, nuova `backup_cmd()` SOLO-CLI, dispatch `gas backup` in `main()`, doctor sez.8 (check off-site + fallimento memoria rumoroso + vector store visibility + `mem=None` prima del blocco).
- **`tests/test_unit_kernel.py`** (+253): T33a-h (TASK A) + T34a-e (TASK B) + helper `_doctor_inproc`.
- **`.claude/agents/memoria_revisore.md`** (+2): lezioni #26 e #27.
- **`reports/`**: ultimo_report.md, stato_progetto.md, diff_sessione.md (questo file).

## Fix minori in sessione

- Alias `_dvp` importato ma inutilizzato a riga 1555 di gas.py (riserva R27-1 del revisore): rimosso prima del commit.
- T18f crash cp1252 (pre-esistente): la suite completa richiede `PYTHONUTF8=1` su Windows per il carattere `approx` nel dettaglio. Non un nuovo FAIL; sul VPS Linux gira identica.

## Esito

- Revisore #26: **APPROVATO CON RISERVE** (R26-1 exit-code best-effort off-site, R26-2 manca T33i).
- Revisore #27: **APPROVATO CON RISERVE** (R27-1 alias _dvp — corretta prima del commit; chiude R-crm-norm-2).
- Suite: **158 PASS, 8 FAIL** — tutti i FAIL pre-esistenti Windows. T33a-h + T34a-e tutti PASS.
- Commit motore: `56a6dc3`.
- R-crm-norm-2 **CHIUSA** (finding aperto dalla review #22).
