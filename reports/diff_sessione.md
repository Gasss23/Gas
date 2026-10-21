# DIFF SESSIONE — 2026-10-21 (R-390-1, giro da Telegram R1, firma in parallelo 5.2, R7, cancello, chat Mani)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `sembra_delicato` (estensioni interne, invisibili); `_normalize_path` toglie i Cf; `libero_dopo_lettura` nega nomi grezzi che Cf/NFKC cambiano.
- `modules/notte/notte.py` — `esegui_notte(solo=...)`; marcatore `ultimo_avvio`.
- `gas.py` — `gas notte <nome>`; `_LOG_PATH` accanto a gas.py; `_percorso_vettori` per kernel, doctor e comandi dei vettori.
- `modules/telegram/bot.py` — `/notte`, `/compito <nome>`, log e avviso del giro; invio in parallelo di firme e notifiche.
- `tests/test_unit_gate.py`, `tests/test_unit_notte.py`, `tests/test_unit_kernel.py` — casi nuovi.
- `.claude/agents/memoria_revisore.md` — righe #391-#400 (caratteri invisibili scritti come `<U+…>`).
- `reports/lavoro_parallelo.md` — terza chat «Mani» e il suo compito.
- `reports/setup_notte.md` — come lanciare un giro a mano.
- `reports/da_mergiare.md`, `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
