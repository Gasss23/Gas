# DIFF SESSIONE — 2026-10-26 (chat Motore, chiusura di V-1/V-2 della verifica esterna #269)

Sessione dentro la PR #269 (ancora aperta): il diff dalla base comprende anche le fette del 25 ottobre.

- `brains/router.py`: `prefisso_forte` (spostata da gas.py), condivisa da terminale, Telegram e voce.
- `brains/claude_cli.py`: login scaduto riconosciuto (JSON e testo semplice, limite prima), clamp dei token; commento allineato al messaggio vero.
- `gas.py`: importa `prefisso_forte`; `/forte` nel terminale.
- `modules/telegram/bot.py`: `/forte <richiesta>` da Telegram, «/forte» nudo → istruzione d'uso.
- `modules/voice/server.py`: `/forte` dalla voce, «/forte» nudo → 400.
- `modules/notte/notte.py`: `cervello: forte` nel catalogo; chiave che somiglia a «cervello» → compito saltato; chiavi sconosciute → avviso.
- `tests/test_unit_claude_cli.py`, `tests/test_unit_kernel.py`, `tests/test_unit_notte.py`, `tests/test_unit_voice_server.py`: test di login, costo, `/forte`, catalogo, ripresa, Telegram, voce.
- `scripts/notte/catalogo_esempio.yaml`, `reports/r2_regole_abbonamento.md`: uso del forte e setup del Mac.
- `.claude/agents/memoria_revisore.md`: righe #511–#518 chat Motore.
- `reports/stato_progetto.md`: R-496-3 e le riserve di #269 chiuse.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md`: report di fine task.

Si riscrive a ogni sessione; la storia completa sta in git.
