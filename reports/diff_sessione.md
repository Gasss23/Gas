# Diff di sessione — 2026-11-10 — terminale opzione A (chat M2)

File toccati (rispetto a origin/main):
- `gas.py` — strumento `manutenzione` nella lista strumenti; DENY prima del cancello nei turni a voce/effimeri/sottofondo/notte e nella finestra notte.
- `modules/gate/gate.py` — livello dell'azione: sola lettura libera, azioni che cambiano Gas IRREVERSIBILI (firma), fuori lista negate.
- `modules/manutenzione/__init__.py` — modulo nuovo: azioni fisse, comandi senza shell con tempo massimo e output tagliato, finestra notte controllata anche all'esecuzione firmata.
- `tests/test_unit_manutenzione.py` — test del modulo, del cancello e del divieto in run_turn.
- `.github/workflows/ci.yml` — passo «manutenzione suite».
- `reports/proposta_terminale_A.md` — proposta (decisione dell'operatore via M1).
- `.claude/agents/memoria_revisore.md` — righe #736, #738, #739, #743-M2.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`, `reports/stato_progetto.md` — report di fine task; in stato_progetto la voce del terminale A con le riserve aperte.

Questo file si riscrive a ogni sessione; la storia completa sta in git.
