# DIFF SESSIONE — 2026-10-22 (chat Mani, fetta 11)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `_Estrattore.parse_starttag`/`parse_endtag` con `_controlla_tag` (tag riconfrontato con la regola del browser, `_taglia`); `_Contesto` con gli indici `_speciali` (punti più annotation-xml), `_confini`, `_formattanti` e la regola delle chiusure di blocco in scope (`_CHIUSURE_IN_SCOPE`, `_CONFINI_SCOPE`, `_FORMATTANTI`).
- `tests/test_unit_web_leggi.py` — tag con virgolette aperte, HTML valido in svg/math senza perdite, formattanti, test diretti di `_Contesto` (318 test).
- `.claude/agents/memoria_revisore.md` — righe #476, #477 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 11».
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
