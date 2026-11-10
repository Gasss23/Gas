# Diff di sessione — 2026-11-10 — R7 fetta 1 (chat M3)

File toccati (da `git diff --stat BASE..HEAD`, BASE = merge-base con origin/main):
- `modules/sottofondo/__init__.py` — ripresa automatica dopo un crash (`_riprendi` sotto lock, `_riprese_max`), progressi `<id>.passi` (`_segna_passo`, `_passi`, `_strumenti_noti`), nota nel prompt (`_nota_ripresa`), pulizia dei `.passi` vecchi, avviso «ripreso N volte»; avviso a ogni ripresa e `ferma()` (comando per fermare un compito senza ripresa, bot #364 V-1); niente ripresa oltre la durata dalla prima creazione (V-2).
- `gas.py` — l'evento `tool_res` porta anche il nome dello strumento (serve ai progressi); comando `gas.py sottofondo-ferma`.
- `tests/test_unit_sottofondo.py` — test della ripresa, della corsa fra due controlli, dei progressi; fixture che spegne le riprese nei test esistenti.
- `tests/test_unit_kernel.py` — T105a controlla il nome nell'evento `tool_res`.
- `reports/proposta_r7_direttore.md` — proposta R7 (opzioni e raccomandazione).
- `.claude/agents/memoria_revisore.md` — righe #736–#739, #743–#745 (più la riga #743-M4 arrivata dal merge di main).
- `reports/roadmap.md`, `reports/stato_progetto.md` — stato di R7 e riserve aperte.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine task.

Nota: questo file si riscrive a ogni sessione; la storia completa sta in git.
