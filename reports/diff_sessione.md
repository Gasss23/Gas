# DIFF SESSIONE — 2026-10-21 (chat Mani, fetta 6)

> Si riscrive a ogni sessione; la storia completa sta in git.

- `modules/web/leggi.py` — `<title/>` apre il titolo nel parser e nel ripiego fuori da svg/math/script/style/iframe/noscript (`_TITOLO_VUOTO_IN`); modo XHTML con autochiusi vuoti; commenti: riga lunga a capo, SystemError su 3.11 con l'input preciso.
- `tests/test_unit_web_leggi.py` — chiusura in più dopo una coppia, `<title/>` dentro e fuori da svg/math, caso del ripiego che discrimina `<title/>` in template/object/canvas e noscript, XHTML (174 test).
- `.claude/agents/memoria_revisore.md` — righe #449-#452 (chat Mani).
- `reports/stato_progetto.md` — blocco «Mani — fetta 6», numeri della fetta 5 allineati.
- `reports/ultimo_report.md`, `reports/handoff.md`, `reports/diff_sessione.md` — report di fine sessione.
