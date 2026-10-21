# DIFF SESSIONE — 2026-10-21 (R-390-1, giro da Telegram R1, firma in parallelo 5.2, chat Mani)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/gate/gate.py` — `sembra_delicato`: chiavi/database tra le estensioni interne, via le ambigue, plist/desktop tenuti, caratteri invisibili tolti.
- `modules/notte/notte.py` — `esegui_notte(solo=...)`: un solo compito per nome; marcatore `ultimo_avvio`.
- `gas.py` — `gas notte <nome>`.
- `modules/telegram/bot.py` — `/notte`, `/compito <nome>`: lancio in un processo a parte, log dell'uscita, avviso se muore prima di partire; invio in parallelo di firme e notifiche.
- `tests/test_unit_gate.py`, `tests/test_unit_notte.py`, `tests/test_unit_kernel.py` — casi nuovi.
- `.claude/agents/memoria_revisore.md` — righe #391-#396.
- `reports/lavoro_parallelo.md` — terza chat «Mani» e il suo compito.
- `reports/setup_notte.md` — come lanciare un giro a mano.
- `reports/da_mergiare.md`, `reports/stato_progetto.md`, `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report.
